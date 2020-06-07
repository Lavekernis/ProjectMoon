from scipy.integrate import odeint
from ObjectClass import *
from variables import *
import matplotlib.pyplot as plt
import numpy as np



#------ Dostosowane do funkcji odeint przedstawienie równań różniczkowych -----

def model(z, t, planet_list, asteroid_list):
    dzdt = []
    
    #--------------------------- Równania dla planet --------------------------

    for index, planet in enumerate(planet_list[1:]):
        dvxdt = 0
        dvydt = 0

        # Nie uwzględniamy oddziaływań od asteroid na planety.
        for jndex, body in enumerate(planet_list[1:]):
            if planet != body:
                distance = ( (z[jndex*4+2]-z[index*4+2])**2 + (z[jndex*4+3]-z[index*4+3])**2 )**0.5
                dvxdt += G*body.mass*(z[jndex*4+2] - z[index*4+2])/(distance)**3
                dvydt += G*body.mass*(z[jndex*4+3] - z[index*4+3])/(distance)**3
        
        distance = ((z[index*4+2])**2+(z[index*4+3])**2)**0.5
        # Siłę od Słońca dodajemy oddzielnie, ponieważ w naszym modelu
        # nie rozwiązujemy równań ruchu dla Słońca - jest nieruchome w (0,0).
        dvxdt += -G*M_sun*(z[index*4+2])/(distance)**3
        dvydt += -G*M_sun*(z[index*4+3])/(distance)**3 

        dxdt = z[index*4]
        dydt = z[index*4+1] 

        dzdt.append(dvxdt)
        dzdt.append(dvydt) 
        dzdt.append(dxdt)
        dzdt.append(dydt)
    
    #----------------------- Równania dla asteroid ----------------------------

    for index, asteroid in enumerate(asteroid_list):
        dvxdt = 0
        dvydt = 0

        # Nie uwzględniamy oddziaływań pomiędzy asteroidami.
        for jndex, body in enumerate(planet_list[1:]):
            distance = ((z[jndex*4+2]-z[index*4+2+8])**2 + (z[jndex*4+3]-z[index*4+3+8])**2)**0.5
            dvxdt += G*body.mass*(z[jndex*4+2] - z[index*4+2+8])/(distance)**3
            dvydt += G*body.mass*(z[jndex*4+3] - z[index*4+3+8])/(distance)**3
    
        distance = ((z[index*4+2+8])**2+(z[index*4+3+8])**2)**0.5
        dvxdt += -G*M_sun*(z[index*4+2+8])/(distance)**3
        dvydt += -G*M_sun*(z[index*4+3+8])/(distance)**3 

        dxdt = z[index*4+8]
        dydt = z[index*4+1+8] 

        dzdt.append(dvxdt)
        dzdt.append(dvydt) 
        dzdt.append(dxdt)
        dzdt.append(dydt)

    return dzdt

#------------------------------------------------------------------------------

    
#----------------------- Symulacja układu z asteroidami -----------------------

def Simulate(asteroid_number = 5, end = 1000  , frequency = 1000):
    """
    Funkcja przerpowadzająca symulację układu ziemia-słońce-księżyc-asteroidy.
    Argumenty:
    asteroid_number - liczba asteroid wykorzystywanych do przeprowadzenia symulacji
    end - końcowy krok symulacji
    frequecy - ilość próbek
    Zwraca:
    Listę kątów, pod którymi uderzyly w księzyc asteroidy.
    """
    #------------------------ Obiekty w układzie ------------------------------    

    sun = Sun()
    earth = Planet(radius = R_earth, mass = M_earth, orbit_radius = d_earth, orbit_object = sun, orbit_period = T_earth)
    moon = Planet(radius = R_moon, mass = M_moon, orbit_radius = d_moon, orbit_object = earth, orbit_period = T_moon)
    planet_list = [sun, earth, moon]
    asteroid_list = [Asteroid(d_mars) for i in range(asteroid_number)]
    
    #-------------------------- Warunki początkowe ----------------------------

    z0 = [ ]
    for planet in planet_list[1:]+asteroid_list:
        velocity = planet.velocity
        position = planet.position
        z0.append(velocity[0])
        z0.append(velocity[1])
        z0.append(position[0])
        z0.append(position[1])

    #------------------------- Rozwiązywanie równań ---------------------------

    sol = odeint(model, z0 , args = (planet_list, asteroid_list), t = np.linspace(0, end, frequency))
    
    #--------------------------- Obsługa kolizji ------------------------------

    for index,asteroid in enumerate(asteroid_list):
        # Sprawdzamy w każdej obliczonej chwili czy asteroida znalazła się
        # wewnątrz jakiegoś ciała.
        for time in sol:
            if ((time[index*4+2+8])**2 + (time[index*4+3+8])**2)**0.5 < sun.radius:
                asteroid.crashed_site = sun
            for jndex,planet in enumerate(planet_list[1:]):
                distance = ((time[jndex*4+2]-time[index*4+2+8])**2 + (time[jndex*4+3]-time[index*4+3+8])**2)**0.5
                if distance < planet.radius:
                    asteroid.crashed_site = planet
                    break
            #Obliczamy kąt uderzenia z twierdzenia cosinusów (zobacz README).
            if asteroid.crashed_site == moon:
                distance = ((time[6]-time[index*4+2+8])**2 + (time[7]-time[index*4+3+8])**2)**0.5
                e_m = ((time[2]-time[6])**2 + (time[3]-time[7])**2)**0.5
                e_a = ((time[2]-time[index*4+2+8])**2 + (time[3]-time[index*4+3+8])**2)**0.5
                cos = (distance**2+e_m**2-e_a**2)/(2*distance*e_m)
                asteroid.crash_angle = np.arccos(cos)
            if asteroid.crashed_site is not None:
                break
    
    #-------------------------- Lista kątów uderzeń ---------------------------
    
    angle_list = []
    for asteroid in asteroid_list:
        if asteroid.crashed_site == moon:
            angle_list.append(asteroid.crash_angle)

    return angle_list

#------------------------------------------------------------------------------

#Narzędzie do rysowania wykresów trajektorii wersja złożona

# for i in range(0,16,4):
#     x,y = [],[]
#     for j in sol:
#         x.append(j[i+2])
#         y.append(j[i+3])
#         ax.plot(x,y)

#Narzędzie do rysowania wykresów trajektorii wersja podstawowa
#  x_e = []
#  y_e = []
#  x_m = []
#  y_m = []
#  x_a = []
#  y_a = []
#  x_a_2 = []
#  y_a_2 = []
#  for i in sol:
#      x_e.append(i[2])
#      y_e.append(i[3])
#      x_m.append(i[6])
#      y_m.append(i[7])
#     x_a.append(i[10])
#     y_a.append(i[11])
#      x_a_2.append(i[14])
#      y_a_2.append(i[15])
#  #print(sol)
#  fig, ax = plt.subplots()
#  ax.plot(x_e,y_e, 'b-')
#  ax.plot(x_m,y_m, 'r-')
#  ax.plot(x_a,y_a, 'y-')
#  ax.plot(x_a_2,y_a_2, 'm-')
#  plt.show()