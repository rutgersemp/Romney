import serial
ser = serial.Serial('COM5')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
fig = plt.figure()
ax1 = plt.subplot(221, polar=True)
ax2 = plt.subplot(222)
ax3 = ax2.twinx()
ax4 = plt.subplot(223)
ax5 = plt.subplot(224)

def setup(ax):
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 1)
    ax.patch.set_alpha(0.0)

import math

import collections
import statistics
stdevSamples = 20
q = collections.deque(maxlen=stdevSamples)
graphLength = 60
avq = collections.deque(maxlen=graphLength)
stq = collections.deque(maxlen=graphLength)
iq = collections.deque(maxlen=graphLength)

offset = 15 # degrees
offset = math.radians(offset)

ax1.set_ylim(0,1)
aBar = ax1.bar(x=0, height=1, width=0.05)

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

ax3.tick_params(
    axis = 'y',
    left = False,
    right = True,
    labelleft = False,
    labelright = True,
    labelcolor = 'tab:blue'
)
ax3.set_ylabel('St. Dev.')
ax3.set_ylim(0,0.5)
DevLine, = ax3.plot([], [], color='tab:blue')

setup(ax4)
ax4.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax4.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
Zline, = ax4.plot(4,0,'|', ms = 30, mfc = 'r')

ax5.set_ylim(-1,1)
tBars = ax5.bar(['x','y','z'],[1,-1,1])


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
    sum = abs(uT[0]) + abs(uT[1]) + abs(uT[2])
    uT_norm = (uT[0]/sum, uT[1]/sum, uT[2]/sum)
    
    plt.setp(ax1.get_yticklabels(), visible=False)

    theta = math.atan2(uT_norm[1], uT_norm[0])
    if theta < 0:
        theta += 2*math.pi
    # adjust for magnetic variance and mechanical angle offset
    theta = compute_angle(theta)# - offset

    aBar[0].set_x(theta)

    # calculate and display some statistics
    q.append(math.degrees(theta))
    st = 0
    av = 0
    if len(q) > 1:
        st = statistics.stdev(q)
        av = statistics.mean(q)
    stq.append(st)
    avq.append(av)
    
    AvLine.set_data(iq, avq)
    # autoscale to values
    ax2.relim()
    ax2.autoscale_view()

    DevLine.set_data(iq, stq)

    Zline.set_data(uT_norm[2], 0)

    # bars don't have a proper set_data method but we make do
    for rect, uT in zip(tBars, uT_norm):
        rect.set_height(uT)

    plt.pause(0.01)

ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()