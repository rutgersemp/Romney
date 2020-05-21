import serial
ser = serial.Serial('COM5')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
fig = plt.figure()
ax1 = plt.subplot(121, polar=True)
ax2 = plt.subplot(122)
ax3 = ax2.twinx()

import math

import collections
import statistics
stdevSamples = 20
q = collections.deque(maxlen=stdevSamples)
graphLength = 60
avq = collections.deque(maxlen=graphLength)
stq = collections.deque(maxlen=graphLength)
iq = collections.deque(maxlen=graphLength)



ax2.set_title(f'Running statistics of last {stdevSamples} samples\n(degrees)')
ax2.tick_params(
    axis = 'y',
    left = True,
    right = False,
    labelleft = True,
    labelright = False,
    labelcolor = 'tab:red'
)
ax2.set_ylabel('Mean')
ax2.ticklabel_format(useOffset=False)
ax2.margins(y=0.8)
AvLine, = ax2.plot([], [], color='tab:red')

ax3.clear()
ax3.tick_params(
    axis = 'y',
    left = False,
    right = True,
    labelleft = False,
    labelright = True,
    labelcolor = 'tab:blue'
)
ax3.set_ylabel('St. Dev.')
DevLine, = ax3.plot([], [], color='tab:blue')

def compute_angle(theta):
    # augment angle using y=mx+b+k*sin(o*x+t)
    m = 0.972302516
    b = -0.464987044
    k = -0.404373247
    o = 2.022130769
    t = 3.297326598


    lin = m*theta+b
    s = k*math.sin(o*theta + t)
    return lin+s

def getteslas():
    _uT = ser.read_until()[:-2] # defaults to newline, strip last two characters \r\n
    _uT = _uT.decode('utf-8') # implicit bytes to string conversion
    uT = tuple(float(axis) for axis in _uT.split(',')) # delimit and convert to float

    return uT


def animate(i):
    iq.append(i)

    uT = getteslas()
    # normalise between -1 and 1
    sum = abs(uT[0]) + abs(uT[1])
    uT_norm = (uT[0]/sum, uT[1]/sum)

    # plot live values
    ax1.clear()
    plt.ylim(0,1)
    plt.setp(ax1.get_yticklabels(), visible=False)

    if uT_norm[0] < 0:
        ax1.bar(x=math.pi, height=abs(uT_norm[0]),width=0.05)
    else:
        ax1.bar(x=0, height=uT_norm[0], width=0.05)

    if uT_norm[1] < 0:
        ax1.bar(x=1.5*math.pi, height=abs(uT_norm[1]),width=0.05)
    else:
        ax1.bar(x=math.pi/2, height=uT_norm[1], width=0.05)

    theta = math.atan2(uT_norm[1], uT_norm[0])
    if theta < 0:
        theta += 2*math.pi

    # adjust for magnetic varianc
    theta = compute_angle(theta)

    ax1.bar(x=theta, height=1, width=0.05)

    # calculate and display some statistics
    q.append(math.degrees(theta))
    st = 0
    av = 0
    if len(q) > 1:
        st = statistics.stdev(q)
        av = statistics.mean(q)
    stq.append(st)
    avq.append(av)
    
    
    # ax2.clear()
    # ax2.set_title(f'Running statistics of last {stdevSamples} samples\n(degrees)')
    # ax2.tick_params(
    #     axis = 'y',
    #     left = True,
    #     right = False,
    #     labelleft = True,
    #     labelright = False,
    #     labelcolor = 'tab:red'
    # )
    # ax2.set_ylabel('Average')
    # ax2.plot(iq, avq, color='tab:red')


    AvLine.set_data(iq, avq)
    ax2.relim()
    ax2.autoscale_view()

    DevLine.set_data(iq, stq)
    ax3.relim()
    ax3.autoscale_view()

    
    plt.pause(0.01)

ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()