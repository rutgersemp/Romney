import tenma

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import collections
graphLength = 60
maq = collections.deque(maxlen=graphLength) # current values
gq = collections.deque(maxlen=graphLength) # gram values
iq = collections.deque(maxlen=graphLength) # x values

fig = plt.figure()
style.use('ggplot')

ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel('n')
ax1.set_ylabel('mA')
ax1.set_ylim([0,1500])
maLine, = ax1.plot([],[], color = 'green', label = 'current')


ax2 = ax1.twinx()
ax2.set_ylabel('g')
ax2.set_ylim([0,200])
gLine, = ax2.plot([],[], color = 'blue', label = 'weight')




psu = tenma.TENMA('COM9')
f = psu.safeDelay

def animate(i):
    iq.append(i)

    ma = psu.getIout(1)*1000
    maq.append(ma)

    g = (0.217*ma) + 25 
    gq.append(g)

    maLine.set_data(iq,maq)
    ax1.relim()
    ax1.autoscale_view()

    gLine.set_data(iq,gq)
    ax2.relim()
    ax2.autoscale_view()

    plt.pause(0.01)

ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()