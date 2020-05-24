import tenma
import collections
from numpy import mean

psu = tenma.TENMA('COM9')
q = collections.deque(maxlen=10)

while 1:
    q.append(psu.getIout(1)*1000)
    print(mean(q))