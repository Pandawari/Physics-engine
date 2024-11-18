from .vector import Vector


class Simulation:

    def __init__(self):
        self.rigid_bodies = []  # list of all rigid bodies in my simulation
        self.lines = []
        self.circles = []

    def add_a_rigid_body(self, rigid_body):
        self.rigid_bodies.append(rigid_body)

    def add_a_line(self, line):
        self.lines.append(line)
        
    def add_a_circle(self, circle):
        self.circles.append(circle)

    def remove_a_rigid_body(self, rigid_body):
        self.rigid_bodies.remove(rigid_body)
        
    
    def remove_a_line(self,line):
        self.lines.remove(line)
    
    def remove_a_circle(self,circle):
        self.circles.remove(circle)
    

    def apply_gravity(self, rb, gravity=Vector(0, 400)):
        if not rb.is_fixed:
            rb.apply_force(gravity * rb.mass)

    def spring_force_between_connected_rb(self, rb, k=5000, L=10, damp=200):

        for connection in rb.connections:

            distance_vector = rb.position - connection.position

            distance = distance_vector.scalar_size()

            if distance == 0:
                continue

            offset = distance - L

            force = distance_vector.normalize_vector()*(-k)*offset
            v_rel = rb.velocity - connection.velocity
           
            rb.apply_force(force - v_rel*damp)
            connection.apply_force(force*(-1) + v_rel*damp)

    def collision_detection_to_line(self, rb, dt):
        for line in self.lines:
            if line.distance_between_point_to_line(rb.position) <= rb.radius:
                
                self.collision_line_acting_normal_force(
                    rb, line, dt)

    def collision_line_acting_normal_force(self, rb, line, dt,e=1):
        line_normal = line.calculate_normal_vector()
        moving_towards = rb.velocity.dot_product(line_normal)

        # checking if the ball is moving towards or away from the line to not detect incorrect collisions.

        if moving_towards <= 0:
            
            
            impulse = line_normal * (-e-1)*(rb.velocity.dot_product(line_normal))*rb.mass
            impulse_force = impulse/dt
            
            force_normal = line_normal * rb.net_force.dot_product(line_normal)*(-1)
            
            
            N_total = impulse_force + force_normal
            
            rb.apply_force(N_total)
            

    def collision_detection_between_rb(self, rb,dt):

        for other_rb in self.rigid_bodies:
            if rb == other_rb:
                continue
            distance_vector = rb.position - other_rb.position
            distance_size = distance_vector.scalar_size()
            overlap = (rb.radius + other_rb.radius) - distance_size
            if distance_size <= rb.radius + other_rb.radius + 0.001:

                self.collision_rb_force(rb,other_rb,dt)

                correction = distance_vector.normalize_vector()*overlap/2
                rb.position += correction
                other_rb.position -= correction
                

    
        
    def collision_rb_force(self,rb1,rb2,dt,e=1):
        
        relative_velocity = rb2.velocity - rb1.velocity
        normal_between_rb = (rb2.position - rb1.position).normalize_vector()
        
        
        if relative_velocity.dot_product(normal_between_rb) > 0:
            return
        
        impulse_scalar = (-1-e)*relative_velocity.dot_product(normal_between_rb) / ((1/rb1.mass) + (1/rb2.mass))
        impulse_vector = normal_between_rb*impulse_scalar
        force = impulse_vector/dt
        
        rb1.apply_force(force*(-1))
        rb2.apply_force(force)
    
        

    def collision_rb_to_circle(self, rb):
        for circle in self.circles:
            distance_to_center = (
                rb.position - circle.position).scalar_size() + rb.radius

            if distance_to_center >= circle.radius + circle.border_width:
                self.collision_solve_rb_to_circle(rb, circle)
                

    def collision_solve_rb_to_circle(self, rb, circle):
        distance_to_center = rb.position - circle.position
        normal = distance_to_center.normalize_vector()
        rb_velocity_projected = rb.velocity.dot_product(normal)
        rb.velocity -= normal*rb_velocity_projected*2
        
    

    def update(self, dt):

        for rb in self.rigid_bodies:

            self.apply_gravity(rb)
            self.collision_detection_between_rb(rb,dt)
            self.collision_detection_to_line(rb, dt)
            self.collision_rb_to_circle(rb)
            self.spring_force_between_connected_rb(rb)
        
            rb.update(dt)
        
         
            rb.reset_net_force()
