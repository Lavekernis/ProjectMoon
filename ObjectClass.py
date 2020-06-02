import variables
import numpy as np
import random

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
    
    def __init__(self, x = 0, y = 0):
        self._radius = variables.R_sun
        self._x = x
        self._y = y
        SpaceObject.__init__(self, mass = variables.M_sun)

    @property
    def position(self):
        return (self._x,self._y)
    
    @property
    def radius(self):
        return self._radius

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
    
    def __init__(self, radius, mass, orbit_radius, orbit_object, angular_velocity):
        self._radius = radius
        self._orbit_radius = orbit_radius
        self._orbit_object = orbit_object
        self._angular_velocity = angular_velocity
        self._angle = random.random()*2*np.pi
        SpaceObject.__init__(self, mass)
    
    def move(self, t):
        self._angle += self.angular_velocity*t
    
    @property
    def position(self):
        X , Y = self.orbit_object.position
        x = self._orbit_radius*np.cos(self._angle) + X
        y = self._orbit_radius*np.sin(self._angle) + Y
        return (x,y)

    @property
    def radius(self):
        return self._radius

    @property
    def angle(self):
        return self._angle

class Asteroid(SpaceObject):
  	
    """
    Masywny punkt, na który działają siły grawitacji od innych obiektów - 'asteroida'.
    Atrybuty:
    	mass - masa asteroidy
        x - współrzędna x asteroidy
        y - współrzędna y asteroidy
        velocity_x - prędkość asteroidy w kierunku x
        velocity_y - prędkość asteroidy w kierunku y
        crashed - wartość logiczna, True - asteroida uderzyła w jakieś inne ciało, False - nie stało się to
        crash_site - ciało, w które uderzyła asteroida
    """
    
    def __init__(self, distance):
        
        #Pozycja
        self._x = distance
        self._y = random.randint(-50,50)
        
        #Prędkość
        theta = random.randint()*2*np.pi
        self._velocity_x = variables.av_velocity * np.cos(theta)
        self._velocity_y = velocity_y * np.sin(theta)
        

        SpaceObject.__init__(self, mass = 1)
        self._crashed = False

    def action(self, planet_list, t):
        
        if self._crashed == False:
            #----------Oddziaływania-----------------------
            acceleration_net = np.array([0,0])
            for planet in planet_list:
                planet_cord = planet.position	
                dx, dy = planet_cord[0] - self.x, planet_cord[1] - self.y
                distance = np.sqrt(dx**2 + dy**2)
                acceleration_magnitude = planet.mass * variables.G * (distance)**(-3)
                acceleration_net += acceleration_magnitude * np.array([dx,dy])
    
            self._velocity_x += acceleration_net[0]*t     
            self._velocity_y += acceleration_net[1]*t
    
            self._x += self._velocity_x*t
            self._y += self._velocity_y*t
            #-----------------------------------------------
            
            #-----------Obsługa-kolizji---------------------
            for planet in planet_list:
                planet_cord = planet.position	
                dx, dy = planet_cord[0] - self.x, planet_cord[1] - self.y
                distance = np.sqrt(dx**2 + dy**2)
                if distance < planet.radius:
                    self._crashed = True
                    self._crash_site = planet
                    if isinstance(planet, Planet):
                        self._crash_angle = planet.angle + np.arctan(self._velocity_x/self._velocity_y)
                    break
            #-----------------------------------------------
    
    @property
    def is_crashed(self):
        return self._crashed
    
    @property
    def crash_site(self):
        return self._crash_site
    
    @property
    def crash_angle(self):
        return self._crash_angle