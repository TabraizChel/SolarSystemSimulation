import math
import time
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt



radius_earth = 6371000
mass_earth = 5.972*(10**24)
G = 6.67*(10**-11)
time_step = 100



class particle ():
    def __init__(self,name,mass, radius, x, y,x_velocity, y_velocity):
        self.name = name
        self.vector_x = [x,x_velocity]
        self.vector_y = [y,y_velocity]
        self.distance = math.sqrt(y**2 + x**2)
        self.grav_field = grav_field(mass,radius)



    def get_mass(self):
        return self.grav_field.get_mass()

    def get_grav_field(self):
        return self.grav_field

    def get_distance(self):
        return self.distance

    def get_vector_x(self):
        return self.vector_x

    def get_vector_y(self):
        return self.vector_y

    def get_radius(self):
        return self.grav_field.get_radius()

    def euler(self,time_step, g):


        if self.vector_y[0] > 0:
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
            self.vector_y[1] = self.vector_y[1] + g*time_step
        elif self.vector_y[0] < 0:
            self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
            self.vector_y[1] = self.vector_y[1] - g*time_step



        self.vector_x[0] = self.vector_x[0] + self.vector_x[1]*time_step
        # self.vector_x[1] = self.vector_x[1] + g*time_step

        self.update_distance()

    def euler_cramer(self,time_step , gx,gy):

        # g = planet.acceleration_through_planet(self)


        self.vector_y[1] = self.vector_y[1] + gy*time_step
        self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step



        self.vector_x[1] = self.vector_x[1] + gx*time_step
        # print(self.vector_x[1],gx)
        self.vector_x[0] = self.vector_x[0] + self.vector_x[1]*time_step


        self.update_distance()





    def update_distance(self):
        self.distance = math.sqrt(self.vector_x[0]**2 + self.vector_y[0]**2)




class grav_field():
    def __init__(self,mass, radius):
        self.mass = mass
        self.radius = radius


    def get_mass(self):
        return self.mass
    def get_radius(self):
        return self.radius

    def set_radius(self,radius):
        self.radius = radius

    # can be removed
    # def calc_acceleration(self,particles):
    #     total_g = 0
    #     for particle in particles:
    #         distance = (((particle.get_vector_y()[0]-self.get_vector_y()[0])**2 +(particle.get_vector_x()[0]- self.get_vector_x()[0])**2))
    #         total_g += -(G*particle.get_mass())/distance
    #     return total_g

    def acceleration_through_planet(self, particle):
        g = -(G*self.mass*particle.distance)/(self.radius**3)
        return g

def acceleration(position_x, position_y, particles):
    total_gx = 0
    total_gy = 0
    for particle in particles:
        distance_squared = (((particle.get_vector_y()[0]-position_y)**2 +(particle.get_vector_x()[0]- position_x)**2))
        if position_x >= particle.get_vector_x()[0]:
            total_gx -= ((G*particle.get_mass())/distance_squared)*(abs(particle.get_vector_x()[0]- position_x)/math.sqrt(distance_squared))
        elif position_x <= particle.get_vector_x()[0]:
            total_gx += ((G*particle.get_mass())/distance_squared)*(abs(particle.get_vector_x()[0]- position_x)/math.sqrt(distance_squared))

        if position_y >= particle.get_vector_y()[0]:
            total_gy -= ((G*particle.get_mass())/distance_squared)*(abs(particle.get_vector_y()[0]- position_y)/math.sqrt(distance_squared))
        elif position_y < particle.get_vector_y()[0]:
            total_gy += ((G*particle.get_mass())/distance_squared)*(abs(particle.get_vector_y()[0]- position_y)/math.sqrt(distance_squared))

    return total_gx,total_gy


def run_sim(time_step,run_time,planets,planet_draw_data):
    start_time = 0
    while start_time < run_time:
        start_time += time_step
        for planet in planets:
            current_planet_index = planets.index(planet)
            remaining_planets = planets[:current_planet_index] + planets[current_planet_index + 1:]
            gx,gy = acceleration(planet.get_vector_x()[0], planet.get_vector_y()[0],remaining_planets)
            planet.euler_cramer(time_step, gx,gy)
            planet_draw_data[planet][0].append(planet.get_vector_x()[0])
            planet_draw_data[planet][1].append(planet.get_vector_y()[0])


def draw_planets(planets, planet_draw_data):
    for planet in planets:
        plt.plot(planet_draw_data[planet][0],planet_draw_data[planet][1], label = planet.name)

    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.legend()
    plt.show()

# planets defined here
Earth = particle('Earth',mass_earth , radius_earth , 149.6e9 , 1,0,30000)
Sun = particle('Sun',2e30, radius_earth , 1 , 1,0,0)
test = particle('test',0.5*mass_earth, radius_earth , 4*149.6e9 , 1,-2000,-9000)
test1 = particle('test1',0.5*mass_earth, radius_earth , 5*149.6e9 , 1,-2000,-9000)
test2 = particle('test2',0.5*mass_earth, radius_earth , 6*149.6e9 , 1,-7000,-15000)
test3 = particle('test3',0.5*mass_earth, radius_earth , 7*149.6e9 , 1,-9000,-8000)

# add planets to planets to planets array and planet_draw_data
planets = [Earth,Sun,test,test1,test2,test3]
planet_draw_data = {Earth:([],[]), Sun:([],[]),test:([],[]),test1:([],[]),test2:([],[]),test3:([],[])}

# define runtime in seconds

run_time = 31536000
run_sim(time_step,run_time,planets,planet_draw_data)
draw_planets(planets, planet_draw_data)
