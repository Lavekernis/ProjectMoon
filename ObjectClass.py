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
        orbit_object - obiekt przy którym pojawia się planeta
        orbit_radius - początkowa odległość planety od orbitowanego obiektu
        angular_velocity - początkowa prędkość kątowa planety
    """
    
    def __init__(self, radius, mass, orbit_radius, orbit_object, orbit_period):
        self._radius = radius
        #obliczanie początkowych pozycji i prędkości na podstawie przybliżenia kolistej orbity,
        #możliwe że niewystarczająca dokładność
        angle = random.random()*2*np.pi
        x, y = orbit_object.position
        x += orbit_radius*np.cos(angle)
        y += orbit_radius*np.sin(angle)
        self._x = x
        self._y = y
        angular_velocity = 2*np.pi/orbit_period
        v_x = -angular_velocity*orbit_radius*np.sin(angle)
        v_y = angular_velocity*orbit_radius*np.cos(angle)
        self._velocity_x = v_x
        self._velocity_y = v_y
        self._orbit_object = orbit_object
        SpaceObject.__init__(self, mass)
    
    def action(self, planet_list, t):
        acceleration_net = np.array([0,0])
        for planet in planet_list:
            if planet != self:
                planet_cord = planet.position	
                dx, dy = planet_cord[0] - self._x, planet_cord[1] - self._y
                distance = np.sqrt(dx**2 + dy**2)
                acceleration_magnitude = planet.mass * variables.G * (distance)**(-3)
                acceleration_net = acceleration_net + acceleration_magnitude * np.array([dx,dy])
    
        self._velocity_x += acceleration_net[0]*t     
        self._velocity_y += acceleration_net[1]*t
        
        self._x += self._velocity_x*t
        self._y += self._velocity_y*t
        
    @property
    def position(self):
        return (self._x,self._y)

    @property
    def radius(self):
        return self._radius
    
    @property
    def orbit_object(self):
        return self._orbit_object

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
        phi = random.random()*2*np.pi
        self._x = distance * np.cos(phi)
        self._y = distance * np.cos(phi)
        
        #Prędkość
        theta = random.random()*2*np.pi
        self._velocity_x = variables.av_velocity * np.cos(theta)
        self._velocity_y = variables.av_velocity * np.sin(theta)
        

        SpaceObject.__init__(self, mass = 1)
        self._crashed = False

    def action(self, planet_list, t):
        
        if self._crashed == False:
            #----------Oddziaływania-----------------------
            acceleration_net = np.array([0,0])
            for planet in planet_list:
                planet_cord = planet.position	
                dx, dy = planet_cord[0] - self._x, planet_cord[1] - self._y
                distance = np.sqrt(dx**2 + dy**2)
                acceleration_magnitude = planet.mass * variables.G * (distance)**(-3)
                acceleration_net = acceleration_net + acceleration_magnitude * np.array([dx,dy])
    
            self._velocity_x += acceleration_net[0]*t     
            self._velocity_y += acceleration_net[1]*t
    
            self._x += self._velocity_x*t
            self._y += self._velocity_y*t
            #-----------------------------------------------
            
            #-----------Obsługa-kolizji---------------------
            for planet in planet_list:
                planet_coord = planet.position	
                dx, dy = planet_coord[0] - self._x, planet_coord[1] - self._y
                distance = np.sqrt(dx**2 + dy**2)
                if distance < planet.radius:
                    self._crashed = True
                    self._crash_site = planet
                    #słaby sposób sprawdzania czy planeta jest Księżycem, można by wymyślić lepszy
                    if planet.radius == variables.R_moon:
                        #liczę kąt uderzenia z twierdzenia cosinusów
                        earth_coord = planet.orbit_object.position
                        d2x, d2y =  planet_coord[0] - earth_coord[0], planet_coord[1] - earth_coord[1]
                        earth_to_moon = d2x**2 + d2y**2
                        d3x, d3y = earth_coord[0] - self._x, earth_coord[1] - self._y
                        earth_to_asteroid = d3x**2 + d3y**2
                        cos = (-earth_to_asteroid+earth_to_moon+distance**2)/2*earth_to_moon*distance
                        self._crash_angle = np.arccos(cos)
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