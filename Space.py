from ObjectClass import *
from variables import *
import random
import math

class Space():

    


    def __init__(distance):
        sun = Sun()
        earth = Planet(radius = R_earth, mass = M_earth, orbit_radius = d_earth, orbit_object = sun, orbit_period = T_earth)
        moon = Planet(radius = R_moon, mass = M_moon, orbit_radius = d_moon, orbit_object = earth, orbit_period = T_moon)
        self._planet_list = [sun, earth, moon]
        self._asteroid_list = [Asteroid(distance = distance) for i in range(0,100)]

    def action(self, t):
        self._planet_list[1].action(planet_list, t)
        self._planet_list[2].action(planet_list, t)
        for asteroid in selasteroid_list:
            asteroid.action(planet_list, t)

