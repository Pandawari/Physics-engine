from .vector import Vector


class Rigid_body:
    def __init__(self, mass, position, velocity, radius, is_fixed=False, is_touched=False):
        self.mass = mass
        self.radius = radius
        self.position = position  # Vector
        self.velocity = velocity  # Vector
        self.acceleration = Vector(0, 0)
        self.net_force = Vector(0, 0)
        self.is_fixed = is_fixed
        self.is_touched = is_touched
        self.connections = []
        self.kinetic_energy = self.find_kinetic_energy()
        self.potential_energy = self.find_potential_energy()
        self.total_energy = self.kinetic_energy + self.potential_energy
        

    def apply_force(self, force):  # force must be vector
        self.net_force += force

    def add_connection(self, other):
        self.connections.append(other)
    
    
            

    def new_integration(self, dt):
        if self.is_touched:
            return

        elif not self.is_fixed:
            self.acceleration = self.net_force / self.mass
            temp = self.velocity
            self.velocity += self.acceleration*dt

            self.position += (self.velocity + temp)*dt/2
            
    def find_kinetic_energy(self):
        velocity_squared = self.velocity.dot_product(self.velocity)
        return self.mass*velocity_squared*(0.5)
    
    def find_potential_energy(self):
        g = 400
        return -self.position.y*self.mass*g
    
    def update_energies(self):
        self.kinetic_energy = self.find_kinetic_energy()
        self.potential_energy = self.find_potential_energy()
        self.total_energy = self.kinetic_energy + self.potential_energy
        
    def update(self, dt):

        self.new_integration(dt)
        self.update_energies()

    def reset_net_force(self):
        self.net_force = Vector(0, 0)
