import tenma

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


x = []
currents = []
grams = []

fig = plt.figure()
style.use('ggplot')

ax1 = fig.add_subplot(1,1,1)
ax2 = ax1.twinx()



psu = tenma.TENMA('COM9')
f = psu.safeDelay

waitdelay = 3
viewrange = 200

def animate(i):
    ma = psu.getIout(1)*1000
    g = (0.226*ma) + 22

    currents.append(ma)
    grams.append(g)
    x.append(i)


    ax1.clear()
    ax1.plot(x, currents, color = 'green', label = 'current')
    ax1.set_xlabel('n')
    ax1.set_ylabel('mA')
    ax1.set_ylim([0,1500])

    ax2.clear()
    ax2.set_ylabel('g')
    ax2.set_ylim([0,200])
    ax2.plot(x, grams, color = 'blue', label = 'weight')

    ax1.set_xlim([i-viewrange, i+3])

    plt.pause(0.01)

ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()