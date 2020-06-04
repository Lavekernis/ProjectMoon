from ObjectClass import *
from variables import *
import random
import math
import matplotlib.pyplot as plt
import time

class Space():

    def __init__(self, distance):
        sun = Sun()
        earth = Planet(radius = R_earth, mass = M_earth, orbit_radius = d_earth, orbit_object = sun, orbit_period = T_earth)
        moon = Planet(radius = R_moon, mass = M_moon, orbit_radius = d_moon, orbit_object = earth, orbit_period = T_moon)
        self.planet_list = [sun, earth, moon]
        self._asteroid_list = [Asteroid(distance = distance) for i in range(0,100)]

    def action(self, t):
        self.planet_list[1].action(self.planet_list, t)
        self.planet_list[2].action(self.planet_list, t)
        #for asteroid in self._asteroid_list:
         #   asteroid.action(self.planet_list, t)

space = Space(d_mars)
X_E = []
Y_E = []
X_M = []
Y_M = []
t1 = time.time()
for i in range(100):
    x_e, y_e = space.planet_list[1].position
    x_m, y_m = space.planet_list[2].position
    X_E.append(x_e)
    Y_E.append(y_e)
    X_M.append(x_m)
    Y_M.append(y_m)
    space.action(1)
print(time.time()-t1)    

fig, ax = plt.subplots()
ax.plot(X_E,Y_E)
ax.plot(X_M,Y_M)
plt.show()
