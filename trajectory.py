import math

radius_earth = 6371000
mass_earth = 5.924*(10**24)
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

        g = planet.calc_acceleration(self.vector_x,self.vector_y)

        self.vector_y[0] = self.vector_y[0] + self.vector_y[1]*time_step
        self.vector_y[1] = self.vector_y[1] - g*time_step

        self.vector_x[0] = self.vector_x[0] + self.vector_x[1]*time_step
        self.vector_x[1] = self.vector_x[1] + g*time_step

        self.update_distance()


    def update_distance(self):
        self.distance = math.sqrt(self.vector_x[0]**2 + self.vector_y[0]**2)




class grav_field():
    def __init__(self,mass):
        self.mass = mass

    def calc_acceleration(self,vector_x,vector_y):
        g = (G*self.mass)//((vector_y[0]**2 + vector_x[0]**2))
        return g

earth = grav_field(mass_earth)

projectile = particle(0,0,radius_earth+100,1000,0)


while projectile.distance > radius_earth:
    projectile.euler(time_step, earth)
print(projectile.vector_x[0],projectile.vector_y[0])
