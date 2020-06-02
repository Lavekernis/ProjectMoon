from ObjectClass import *
from variables import *
import random
import math

class Space():

    planet_list = []


    def __init__(distance):
        sun = Sun()
        earth = Planet(radius = R_earth, mass = M_earth, orbit_radius = d_earth, orbit_object = sun, angular_velocity = 2*math.pi/T_earth)
        moon = Planet(radius = R_moon, mass = M_moon, orbit_radius = d_moon, orbit_object = earth, angular_velocity = 2*math.pi/T_moon)
        planet_list.append(sun, earth, moon)
        asteroid_list = [Asteroid(distance = distance) for i in range(0,100)]
