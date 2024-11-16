from rigid_body import *
from vector import *

class Simulation:
    
    def __init__(self):
        self.rigid_bodies = [] # list of all rigid bodies in my simulation
        self.lines = []
        self.circles = []

    def add_a_rigid_body(self,rigid_body):
        self.rigid_bodies.append(rigid_body)
    def add_a_line(self,line):
        self.lines.append(line)
    def remove_a_rigid_body(self,rigid_body,line):
        self.rigid_bodies.remove(rigid_body)
        self.lines.remove(line)
    def add_a_circle(self,circle):
        self.circles.append(circle)

    def collision_detection_to_line(self,rb,dt):
            for line in self.lines:
                penetration = rb.radius - line.distance_between_point_to_line(rb.position)
                if line.distance_between_point_to_line(rb.position) <= rb.radius:
                    
                    self.collision_line_acting_normal_force(rb,line,dt,penetration)
                    

        
    def collision_line_acting_normal_force(self,rb,line,dt,penetration):
        line_normal = line.calculate_normal_vector()
        moving_towards = rb.velocity.dot_product(line_normal) 

        #checking if the ball is moving towards or away from the line to not detect incorrect collisions.

        if moving_towards < 0:
             
        
            e = 0.5
            impulse = line_normal*(-e-1)*(rb.velocity.dot_product(line_normal))*rb.mass
            impulse_force = impulse/dt
            

        
            force_normal = line_normal*rb.net_force.dot_product(line_normal)*(-1)
            N_total = impulse_force + force_normal
            rb.apply_force(N_total)
            
            
            

    def collision_detection_between_rb(self,rb):
        
            for other_rb in self.rigid_bodies:
                if rb == other_rb:
                    continue
                distance_vector = rb.position - other_rb.position
                distance_size = distance_vector.scalar_size()
                overlap = (rb.radius + other_rb.radius) - distance_size
                if distance_size <= rb.radius + other_rb.radius + 0.001:
                    
                    self.collision_rb(rb,other_rb)
                    
                    correction = distance_vector.normalize_vector()*overlap/2
                    rb.position += correction
                    other_rb.position -= correction

    
    def collision_rb(self,rb1,rb2):
        v1 = rb1.velocity
        x1 = rb1.position
        m1 = rb1.mass

        v2 = rb2.velocity
        m2 = rb2.mass
        x2 = rb2.position

        k1 = 2*m2/(m1+m2)
        k2 = 2*m1/(m1+m2)
        
        dots1 = ((Vector.dot_product(v1-v2 ,x1-x2)) / (Vector.scalar_size((x1-x2)))**2)
        dots2 = ((Vector.dot_product(v2-v1 ,x2-x1)) / (Vector.scalar_size((x2-x1)))**2)
        rb1.velocity = v1 - (x1-x2)*k1*dots1
        rb2.velocity = v2 - (x2-x1)*k2*dots2
       

    def collision_rb_to_circle(self,rb):
        for circle in self.circles:
            distance_to_center =  (rb.position -  circle.position).scalar_size() + rb.radius
            
            if distance_to_center >= circle.radius + circle.border_width:
                self.collision_solve_rb_to_circle(rb,circle)
    
    def collision_solve_rb_to_circle(self,rb,circle):
        distance_to_center = rb.position - circle.position
        normal = distance_to_center.normalize_vector()
        rb_velocity_procted = rb.velocity.dot_product(normal)
        rb.velocity -= normal*rb_velocity_procted*2
    

    def update(self,dt):
          
            for rb in self.rigid_bodies:
            
                Rigid_body.gravity(rb)
                
                self.collision_detection_between_rb(rb)
                self.collision_detection_to_line(rb,dt)
                self.collision_rb_to_circle(rb)
                rb.spring_force_between_connected_rb()
              

                Rigid_body.update(rb,dt)
                Rigid_body.reset_net_force(rb)

my_simulation = Simulation()

rb1 = Rigid_body(mass=50,position=Vector(700,70),velocity =Vector(0,0),radius=30,is_fixed=False)
rb2 = Rigid_body(mass=50,position=Vector(170,400),velocity =Vector(0,0),radius=30,is_fixed=False)
rb3 = Rigid_body(mass=50,position=Vector(200,220),velocity =Vector(50,0),radius=30,is_fixed=False)
rb4 = Rigid_body(mass=50,position=Vector(250,430),velocity =Vector(-20,0),radius=30,is_fixed=False)
rb5 = Rigid_body(mass=50,position=Vector(300,290),velocity =Vector(-80,0),radius=30,is_fixed=True)
rb6 = Rigid_body(mass=50,position=Vector(150,120),velocity =Vector(0,0),radius=30,is_fixed=True)


l1 = Line(start_point=Vector(0,500),end_point=Vector(1280,500),oriantation=-1)
l2 = Line(start_point=Vector(0,0),end_point=Vector(1280,0),oriantation=1)
l3= Line(start_point=Vector(0,0),end_point=Vector(0,720),oriantation=1)
l4= Line(start_point=Vector(1280,0),end_point=Vector(1280,720),oriantation=-1)
l5= Line(start_point=Vector(0,1280),end_point=Vector(1280,720),oriantation=1)

c1 = Circle(500,Vector(600,200),2)

my_simulation.add_a_line(l1)
my_simulation.add_a_line(l2)
my_simulation.add_a_line(l3)
my_simulation.add_a_line(l4)
my_simulation.add_a_line(l5)


my_simulation.add_a_rigid_body(rb1)
my_simulation.add_a_rigid_body(rb2)
rb1.add_connection(rb2)
                
                
                

