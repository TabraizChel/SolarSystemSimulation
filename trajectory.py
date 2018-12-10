import math
import time
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
radius_earth = 6371000
mass_earth = 5.972*(10**24)
G = 6.67*(10**-11)
time_step = 0.01
class particle ():
    def __init__(self,mass, x, y,x_velocity, y_velocity):

        self.vector_x = [x,x_velocity]
        self.vector_y = [y,y_velocity]
        self.distance = math.sqrt(y**2 + x**2)
        self.mass = mass



    def get_mass(self):
        return self.mass

    def get_distance(self):
        return self.distance

    def get_vector_x(self):
        return self.vector_x

    def get_vector_y(self):
        return self.vector_y

    def euler(self,time_step,planet):

        g = planet.calc_acceleration(self)
        # g = planet.acceleration_through_planet(self)
        if self.vector_y[0] > 0:
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
            self.vector_y[1] = self.vector_y[1] + g*time_step
        elif self.vector_y[0] < 0:
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
            self.vector_y[1] = self.vector_y[1] - g*time_step



        self.vector_x[0] = self.vector_x[0] + self.vector_x[1]*time_step
        # self.vector_x[1] = self.vector_x[1] + g*time_step

        self.update_distance()


    def update_distance(self):
        self.distance = math.sqrt(self.vector_x[0]**2 + self.vector_y[0]**2)




class grav_field():
    def __init__(self,mass, radius):
        self.mass = mass
        self.radius = radius


    def get_radius(self):
        return self.radius

    def set_radius(self,radius):
        self.radius = radius

    def calc_acceleration(self,particle):
        g = -(G*self.mass)/((particle.vector_y[0]**2 + particle.vector_x[0]**2))
        return g

    def acceleration_through_planet(self, particle):
        g = -(G*self.mass*particle.distance)/(self.radius**3)

        return g



earth = grav_field(mass_earth, radius_earth)
start_velocity = float(input('How fast should the projectile be ? (in m/s):  '))
start_height = float(input('What should the start height be ? (in m):  '))
projectile = particle(0,0,radius_earth + start_height,start_velocity,0)

time = 0
x_data = []
y_data = []
planet_x = []
planet_y = []
while projectile.get_distance() > earth.get_radius():
    projectile.euler(time_step, earth)
    x_data.append(projectile.get_vector_x()[0])
    y_data.append(projectile.get_vector_y()[0])
    try:
        planet_y.append(math.sqrt(earth.get_radius()**2 - projectile.get_vector_x()[0]**2))
        planet_x.append(projectile.get_vector_x()[0])
    except ValueError:
        break


plt.plot(x_data,y_data, label = 'particle trajectory')
plt.plot(planet_x,planet_y, label = 'planet')
plt.xlim(0,x_data[-1])
plt.legend()
plt.show()
