from ObjectClass import *
from variables import *
import random
import math

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
        for asteroid in self._asteroid_list:
            asteroid.action(self.planet_list, t)

space = Space(d_mars)
for i in range(10000):
    x_e, y_e = space.planet_list[1].position
    x_s, y_s = space.planet_list[0].position
    r = ((x_e-x_s)**2+(y_e-y_s)**2)**0.5
    print(r)
    space.action(1)
    x_e, y_e = space.planet_list[1].position
    x_s, y_s = space.planet_list[0].position
    r = ((x_e-x_s)**2+(y_e-y_s)**2)**0.5
    print(r)
 