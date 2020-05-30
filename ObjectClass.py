import variables
import numpy as np

class SpaceObject():
    
    """
    Dowolny masywny obiekt w kosmosie.
    Atrybuty:
        mass - masa obiektu
    """
    
    def __init__(self, mass):
        self.mass = mass

class Sun(SpaceObject):
    
    """
    Kulisty, nieruchomy obiekt w kosmosie.
    Atrybuty:
        radius - promień obiektu
        mass - masa obiektu
        x - współrzędna x obiektu
        y - współrzędna y obiektu
    """
    
    def __init__(self, radius, mass, x, y):
        self._radius = radius
        self._x = x
        self._y = y
        SpaceObject.__init__(self, mass)

    @property
    def position(self):
        return (self.x,self.y)
    

class Planet(SpaceObject):
    
    """
    Kulisty obiekt który porusza się wokół innego obiektu po kolistej orbicie - 'planeta'.
    Atrybuty:
        radius - promień planety
        mass - masa planety
        angle - kąt
        orbit_radius - promień orbity po której porusza się planeta
        orbit_object - obiekt wokół którego porusza się planeta
        angular_velocity - prędkość kątowa planety
    """
    
    def __init__(self, radius, mass, orbit_radius, orbit_object, velocity, angle):
        self._orbit_radius = orbit_radius
        self._orbit_object = orbit_object
        self._angular_velocity = angular_velocity
        self._angle = angle
        SpaceObject.__init__(self, mass)
    
    def move(t):
        self._angle += self.angular_velocity*t
    
    @property
    def position(self):
        X , Y = self.orbit_object.position
        x = self._orbit_radius*np.cos(self._angle) + X
        y = self._orbit_radius*np.sin(self._angle) + Y
        return (x,y)