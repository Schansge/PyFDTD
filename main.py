import math
import numpy
import numpy.ma
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import fdtd

fig = plt.figure(1)

# create listen ports
portlist = []

# add source port
def f(t):
    x = t - 300e-12
    if x < 0.0:
        return math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    elif x < 600e-12:
        return math.cos(2.0*math.pi*40e9*x)
    else:
        return math.exp(-(x-600e-12)**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    
portlist.append(fdtd.port( (0.1, 0.1), f))

# create solver
solver = fdtd.solver(fdtd.field(0.20, 0.20, 0.0005, 0.0005), ports=portlist)

# add material
layer = solver.material.empty_layer()

for i in range(0, 20, 1):
    for j in range(0, 20, 1):
        layer['epsilon'][40+i, 360+j] = 8.0

solver.material.add_layer(layer)

# iterate
ims = []

history = solver.iterate(1.0e-12, 2000e-12, safeHistory=True, historyInterval=5e-12)

for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-0.05, 0.05))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)


plt.show()
