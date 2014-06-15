import numpy as np

N = 10000000

Mtd1 = 2
Mtd2 = 2
Mtbl = 4

Tfix1 = 6.
Tfix2 = 4.
Tfix3 = 4.

d1 = np.ones((N))
d2 = np.ones((N))
bl = np.ones((N))

p1 = 1./Mtd1
p2 = 1./Mtd2
p3 = 1./Mtbl

d1 = np.sort(np.random.geometric(p1,N))
d2 = np.sort(np.random.geometric(p2,N))
bl = np.sort(np.random.geometric(p3,N))

print sum(d1)/float(N), d1[int(N/2.)]
print sum(d2)/float(N), d2[int(N/2.)]
print sum(bl)/float(N), bl[int(N/2.)]


