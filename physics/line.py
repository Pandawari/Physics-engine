from .vector import Vector


class Line:
    def __init__(self, start_point, end_point, oriantation=1):
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
            # Keep in mind there is 2 possible normal vectors 1,0 and -1,0
            return Vector(self.oriantation, 0)

        return Vector(-self.slope, 1).normalize_vector()*self.oriantation

    def distance_between_point_to_line(self, point):
        numerator = abs((self.end_point.y - self.start_point.y)*point.x - (self.end_point.x - self. start_point.x)
                        * point.y + self.end_point.x*self.start_point.y - self.end_point.y*self.start_point.x)
        denominator = ((self.end_point.y-self.start_point.y) **
                       2 + (self.end_point.x - self.start_point.x)**2)**(0.5)
        return numerator/denominator

    def find_y_axis_intersection(self):
        return self.start_point.y - self.slope*self.start_point.x

    def calculate_length(self):

        sqrd_len = abs(((self.end_point.y - self.start_point.y)
                       ** 2 + (self.end_point.x - self.start_point.x)**2))
        return sqrd_len**(0.5)
