
# assumes ax^2 + bx + c = 0 and assumes root exist in real plane
def quadratic_solver(a, b, c):
    x1 = (-b + (b**2 - 4*a*c)**(0.5)) / (2*a)
    x2 = (-b - (b**2 - 4*a*c)**(0.5)) / (2*a)
    return [x1, x2]


def is_point_inside(x, y, circle):

    r = circle.radius
    circle_center_x = circle.position.x
    circle_center_y = circle.position.y

    if r**2 >= (x - circle_center_x)**2 + (y - circle_center_y)**2:
        return True
    else:
        return False
