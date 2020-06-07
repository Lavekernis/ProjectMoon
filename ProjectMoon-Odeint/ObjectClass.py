import variables
import numpy as np
import random

class SpaceObject():
    
    """
    Dowolny masywny obiekt w kosmosie.
    Atrybuty:
        mass - masa obiektu
        x - współrzędna x obiektu
        y - współrzędna y obiektu
    """
    
    def __init__(self, mass ,x , y):
        self._mass = mass
        self._x = x
        self._y = y

    @property
    def position(self):
        return (self._x,self._y)

    @property
    def mass(self):
        return self._mass

class Sun(SpaceObject):
    
    """
    Kulisty, nieruchomy obiekt w kosmosie.
    Atrybuty:
        radius - promień obiektu
        mass - masa obiektu
        x - współrzędna x obiektu
        y - współrzędna y obiektu
    """
    
    def __init__(self,   x = 0, y = 0):
        self._radius = variables.R_sun
        SpaceObject.__init__(self, variables.M_sun, x, y)
    
    @property
    def radius(self):
        return self._radius

class Planet(SpaceObject):
    
    """
    Kulisty obiekt który porusza się w kosmosie - 'planeta'.
    Atrybuty:
        radius - promień planety
        mass - masa planety
        orbit_object - obiekt przy którym pojawia się planeta
        x - współrzędna x planety
        y - współrzędna y planety
    """
    
    def __init__(self, radius, mass, orbit_radius, orbit_object, orbit_period):
        self._radius = radius
        # Obliczanie początkowych pozycji i prędkości na podstawie 
        # przybliżenia kolistej orbity.
        
        # Położenie
        angle = random.random()*2*np.pi
        x, y = orbit_object.position
        x += orbit_radius*np.cos(angle)
        y += orbit_radius*np.sin(angle)
        SpaceObject.__init__(self, mass, x, y)
        
        # Prędkość
        angular_velocity = 2*np.pi/orbit_period
        v_x = -angular_velocity*orbit_radius*np.sin(angle)
        v_y = angular_velocity*orbit_radius*np.cos(angle)
        # Trochę niezręczny sposób sprawdzania, czy obiekt orbituje wokół Słońca.
        if orbit_object.mass != variables.M_sun:
            v_x += orbit_object._velocity_x
            v_y += orbit_object._velocity_y
        self._velocity_x = v_x
        self._velocity_y = v_y
        
        self._orbit_object = orbit_object

    @property
    def velocity(self):
        return self._velocity_x,self._velocity_y

    @property
    def radius(self):
        return self._radius
    
    @property
    def orbit_object(self):
        return self._orbit_object


class Asteroid(SpaceObject):
  	
    """
    Masywny punkt, który może poruszać się w kosmosie - 'asteroida'.
    Atrybuty:
    	mass - masa asteroidy
        x - współrzędna x asteroidy
        y - współrzędna y asteroidy
        velocity_x - prędkość asteroidy w kierunku x
        velocity_y - prędkość asteroidy w kierunku y
        crash_site - ciało, w które uderzyła asteroida
        crash_angle - kąt, pod którym asteroida uderzyła w ciało
    """
    
    def __init__(self, distance):
        
        # Pozycja
        phi = random.random()*2*np.pi
        x = distance * np.cos(phi)
        y = distance * np.sin(phi)
        SpaceObject.__init__(self, 1, x, y)

        # Prędkość
        theta = random.random()*2*np.pi
        self._velocity_x = variables.av_velocity * np.cos(theta)
        self._velocity_y = variables.av_velocity * np.sin(theta)
        
        # Obsługa zderzeń
        self._crashed_side = None 
        self._crash_angle = 0

    @property
    def velocity(self):
        return self._velocity_x,self._velocity_y

    @property
    def crashed_site(self):
        return self._crashed_side

    @property
    def crash_angle(self):
        return self._crash_angle
    
    @crashed_site.setter
    def crashed_site(self,x):
        self._crashed_side = x

    @crash_angle.setter
    def crash_angle(self,x):
        self._crash_angle = x