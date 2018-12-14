import math
import time
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation



radius_earth = 6371000
mass_earth = 5.972*(10**24)
G = 6.67*(10**-11)
time_step = 0.1


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

    def euler_cramer(self,time_step,planet,a_x = 0):
        g = planet.calc_acceleration(self)
        # g = planet.acceleration_through_planet(self)
        a_x,a_y = planet.calc_acceleration_air_resistance(self)
        print(a_x, self.vector_x[1])
        if self.vector_y[0] > 0:
            self.vector_y[1] = self.vector_y[1] + (g+a_y)*time_step
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
        elif self.vector_y[0] < 0:
            self.vector_y[1] = self.vector_y[1] - (g+a_y)*time_step
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step


        self.vector_x[1] = self.vector_x[1] + a_x*time_step
        self.vector_x[0] = self.vector_x[0] + self.vector_x[1]*time_step



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

    #function in testing
    def calc_acceleration_air_resistance(self,particle):
        drag_coefficient = 0.04
        air_density = 1.2
        area_human = 1.9
        mass = 70
        a_x = ((0.5)*(drag_coefficient)*(air_density)*(area_human)*((particle.get_vector_x()[1])**2))/mass
        a_y = ((0.5)*(drag_coefficient)*(air_density)*(area_human)*((particle.get_vector_y()[1])**2))/mass

        if particle.get_vector_x()[1] > 0:
            a_x = -1*a_x
        if particle.get_vector_y()[1] > 0:
            a_y = -1*a_y


        return (a_x , a_y)



    def acceleration_through_planet(self, particle):
        g = -(G*self.mass*particle.distance)/(self.radius**3)
        return g



earth = grav_field(mass_earth, radius_earth)
start_velocity = float(input('How fast should the projectile be ? (in m/s):  '))
start_height = float(input('What should the start height be ? (in m):  '))
projectile = particle(0,0,radius_earth + start_height,start_velocity,0)

runtime = 0
x_data = []
y_data = []
planet_x = []
planet_y = []


plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    ax1.clear()
    ax1.plot(x_data,y_data, label = 'particle trajectory')
    ax1.plot(planet_x,planet_y, label = 'planet' )
    plt.xlabel('Distance (m)')
    plt.ylabel('Height above Earth surface (m)')
    plt.legend()
    
while runtime < 10000:
    runtime += time_step
    projectile.euler_cramer(time_step, earth)
    x_data.append(projectile.get_vector_x()[0])
    y_data.append(projectile.get_vector_y()[0] - earth.get_radius())

    ani = animation.FuncAnimation(fig,animate,interval=100000)
    plt.draw()
    plt.pause(0.0001)



    if projectile.get_distance() < earth.get_radius():
        print(runtime)
        break
    try:
        planet_y.append(math.sqrt(earth.get_radius()**2 - projectile.get_vector_x()[0]**2) - earth.get_radius())
        planet_x.append(projectile.get_vector_x()[0])
    except ValueError:
        continue



plt.plot(x_data,y_data, label = 'particle trajectory')
plt.plot(planet_x,planet_y, label = 'planet')
plt.xlabel('Distance (m)')
plt.ylabel('Height above Earth surface (m)')
plt.legend()
plt.show()
