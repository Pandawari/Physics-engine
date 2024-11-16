class Vector():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'x = {self.x:.3f}, y = {self.y:.3f}'

    def __add__(self,other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self,scalar):
        return Vector(self.x*scalar, self.y*scalar)
    
    def __truediv__(self,scalar):
        
        return Vector(self.x/scalar, self.y/scalar)
    
    def dot_product(self,other):
        return (self.x*other.x + self.y*other.y)
    
    def scalar_cross_product(self,other):
        return (self.x*other.y - self.y*other.x)
    def scalar_size(self):
        return (
            ((self.x)**2 + (self.y)**2)**(1/2)
        )
    def distance_between_two_points(self,other):
        L = abs(((self.x- other.x)**2 - (self.y -other.y)**2))
        distance = L**(1/2)
        return distance
    
    def normalize_vector(self):
        r = (self.x**2 + self.y**2)**(0.5)
        if r == 0:
            return Vector(0,0)
        normalized_vector = Vector(self.x/r,self.y/r)
        return normalized_vector
        

    def cross_product(self):
        return
    def tuple(self):
        return self.x,self.y
    
    def projection(self,other):
        if self.scalar_size() == 0:
            return 0
        proj = self.dot_product(other) / (self.scalar_size())
        return proj

# some math functions
def quadratic_solver(a,b,c): # assumes ax^2 + bx + c = 0 and assumes root exist in real plane
    x1 = (-b + (b**2 - 4*a*c)**(0.5) )/ (2*a)
    x2 = (-b - (b**2 - 4*a*c)**(0.5) )/ (2*a)
    return [x1,x2]

def is_point_inside(x,y,circle):
  
    r = circle.radius
    circle_center_x = circle.position.x
    cirlce_center_y = circle.position.y

    if r**2 >= (x - circle_center_x)**2 + (y - cirlce_center_y)**2:
        return True
    else:
        return False