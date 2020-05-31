import variables
import numpy as np

class SpaceObject():
    
    """
    Dowolny masywny obiekt w kosmosie.
    Atrybuty:
        mass - masa obiektu
    """
    
    def __init__(self, mass):
        self._mass = mass
    
    @property
    def mass(self):
        return self.mass

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

class Asteroid(SpaceObject):
  	
    """
    Masywny punkt, na który działają siły grawitacji od innych obiektów - 'asteroida'.
    Atrybuty:
    		mass - masa asteroidy
        x - współrzędna x asteroidy
        y - współrzędna y asteroidy
        velocity_x - prędkość asteroidy w kierunku x
        velocity_y - prędkość asteroidy w kierunku y
    """
    
    def __init__(self, radius, mass, orbit_radius, orbit_object, velocity, angle):
        self._x = x
        self._y = y
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y
        SpaceObject.__init__(self, mass)

    def action(self, planet_list, t):
        net = np.array([0,0])
        
        for planet in planet_list:
            planet_cord = planet.position	
            dx, dy = planet_cord[0]-self.x, planet_cord[1]-self.y
            distance = np.sqrt(dx**2 + dy**2)
            force_mag = planet.mass*variables.G*(distance)**(-2)
            net += (force_mag/distance)*np.array([dx,dy])

        self._velocity_x += net[0]*t     
        self._velocity_y += net[1]*t

        self._x += self._velocity_x*t
        self._y += self._velocity_y*t


