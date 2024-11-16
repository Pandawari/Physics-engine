from .vector import Vector

class Rigid_body:
    def __init__(self,mass,position,velocity,radius,mouse_force= Vector(0,0),is_fixed=False,is_touched=False):
        self.mass = mass
        self.position = position #Vector
        self.previous_position = position
        self.velocity = velocity #Vector
        self.acceleration = Vector(0,0)
        self.net_force = Vector(0,0)
        self.is_fixed = is_fixed
        self.is_touched = is_touched
        self.mouse_force = mouse_force
        
        self.connections = []
        self.radius = radius
        
    
    def apply_force(self,force): # force must be vector
        self.net_force += force

    def gravity(self):
        gravity = Vector(0,400)*self.mass
        self.net_force += gravity

    def add_connection(self,other):
        self.connections.append(other)


    def new_integration(self,dt):
        if self.is_touched:
            
            self.acceleration = self.mouse_force / self.mass
            temp = self.velocity
            self.velocity += self.acceleration*dt
            self.position += (self.velocity + temp)*dt/2

        elif not self.is_fixed :
            self.acceleration = self.net_force / self.mass
            temp = self.velocity
            self.velocity += self.acceleration*dt
            
            self.position += (self.velocity + temp)*dt/2
 

    def spring_force_between_connected_rb(self,k=1000):
        
            for connection in self.connections:
                
                L = 300
                
                distance_vector = self.position - connection.position
                
                distance = distance_vector.scalar_size()
                
                damp = 200
                if distance == 0:
                    continue
                offset = distance - L
                force = distance_vector.normalize_vector()*(-k)*offset
                v_rel = self.velocity - connection.velocity
                
                self.apply_force(force - v_rel*damp)
                connection.apply_force(force*(-1) + v_rel*damp)

    def force_between_mouse_and_rb(self,mouse,k=100):
                
                
                distance_vector = self.position - mouse
                
                distance = distance_vector.scalar_size()
                
               
                force = distance_vector.normalize_vector()*(-k)*distance
                return force
        
     
 
   
                    
    def update(self,dt):
    
        
        self.new_integration(dt)
        
        

    def reset_net_force(self):
        self.net_force = Vector(0,0)

    

class Line:
    def __init__(self,start_point,end_point,oriantation=1):
        self.start_point = start_point
        self.end_point = end_point
        self.slope = self.calculate_slope()
        self.oriantation = oriantation
        self.normal_vector = self.calculate_normal_vector()
        self.a = self.find_y_axis_intersection()
        
        
    def calculate_slope(self):
        if self.end_point.x == self.start_point.x:
            return float('inf')
        
        return (self.end_point.y - self.start_point.y) / (self.end_point.x - self.start_point.x)
    
    def calculate_normal_vector(self):
        if self.slope == float('inf'):
            return Vector(self.oriantation,0) # Keep in mind there is 2 possible normal vectors 1,0 and -1,0
        
        return Vector(-self.slope ,1).normalize_vector()*self.oriantation
    def distance_between_point_to_line(self,point):
        numerator = abs((self.end_point.y -self.start_point.y)*point.x - (self.end_point.x - self. start_point.x)*point.y + self.end_point.x*self.start_point.y - self.end_point.y*self.start_point.x)
        denominator = ((self.end_point.y-self.start_point.y)**2  + (self.end_point.x - self.start_point.x)**2)**(0.5)
        return numerator/denominator
    def find_y_axis_intersection(self):
        return self.start_point.y  - self.slope*self.start_point.x
    def calculate_length(self):
        
        sqrd_len  = abs(((self.end_point.y - self.start_point.y)**2 + (self.end_point.x - self.start_point.x)**2))
        return sqrd_len**(0.5)
    

class Circle:
    def __init__(self,radius,position,border_width):
        self.radius = radius
        self.position = position
        self.border_width = border_width
    