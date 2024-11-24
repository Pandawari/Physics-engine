import pygame
import physics


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
fps = 240
dt = 1 / fps
font = pygame.font.SysFont("Arial", 18)
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text
button_rect = pygame.Rect(1500,100,200,30)

# initialize simulation and add objects
my_simulation = physics.Simulation()

rb1 = physics.Rigid_body(mass=50, position=physics.Vector(
    700, 160), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb2 = physics.Rigid_body(mass=50, position=physics.Vector(
    450, 450), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb3 = physics.Rigid_body(mass=50, position=physics.Vector(
    400, 400), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb4 = physics.Rigid_body(mass=50, position=physics.Vector(
    350, 350), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb5 = physics.Rigid_body(mass=50, position=physics.Vector(
    300, 300), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb6 = physics.Rigid_body(mass=50, position=physics.Vector(
    250, 250), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb7 = physics.Rigid_body(mass=50, position=physics.Vector(
    650, 250), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb8 = physics.Rigid_body(mass=50, position=physics.Vector(
    950, 560), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb9 = physics.Rigid_body(mass=50, position=physics.Vector(
    960, 660), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)
rb10 = physics.Rigid_body(mass=50, position=physics.Vector(
    250, 160), velocity=physics.Vector(0, 0), radius=30, is_fixed=False)



l2 = physics.Line(start_point=physics.Vector(
    0, 0), end_point=physics.Vector(1280, 0), orientation=1)
l3 = physics.Line(start_point=physics.Vector(
    0, 0), end_point=physics.Vector(0, 720), orientation=1)
l4 = physics.Line(start_point=physics.Vector(1280, 0),
                  end_point=physics.Vector(1280, 720), orientation=-1)
l5 = physics.Line(start_point=physics.Vector(0, 720),
                  end_point=physics.Vector(1280, 720), orientation=-1)

c1 = physics.Circle(500, physics.Vector(600, 200), 2)

my_simulation.add_a_line(l2)
my_simulation.add_a_line(l3)
my_simulation.add_a_line(l4)
my_simulation.add_a_line(l5)


my_simulation.add_a_rigid_body(rb1)
my_simulation.add_a_rigid_body(rb2)
my_simulation.add_a_rigid_body(rb3)
my_simulation.add_a_rigid_body(rb4)
my_simulation.add_a_rigid_body(rb5)
my_simulation.add_a_rigid_body(rb6)
my_simulation.add_a_rigid_body(rb7)
my_simulation.add_a_rigid_body(rb8)
my_simulation.add_a_rigid_body(rb9)
my_simulation.add_a_rigid_body(rb10)


"""for i in my_simulation.rigid_bodies:
    for j in my_simulation.rigid_bodies:
        if i == j:
            continue
        elif j not in i.connections:
            i.add_connection(j)
"""

"""for i in range(len(my_simulation.rigid_bodies)):
    if i != len(my_simulation.rigid_bodies) - 1:
        my_simulation.rigid_bodies[i].add_connection(my_simulation.rigid_bodies[i+1])"""


show_velocity = False
show_force = False
run = True
while run:
    x, y = pygame.mouse.get_pos()
    mouse = physics.Vector(x, y)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for rb in my_simulation.rigid_bodies:

                if physics.is_point_inside(x, y, rb):
                    rb.is_touched = True
                    rb.velocity = physics.Vector(0, 0)
                    
            if button_rect.collidepoint((x,y)):
                show_velocity = not show_velocity

               
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                my_simulation.add_a_rigid_body(physics.Rigid_body(mass=50, position=mouse, velocity=physics.Vector(0, 0), radius=30, is_fixed=False))

        if event.type == pygame.MOUSEBUTTONUP:

            for rb in my_simulation.rigid_bodies:

                rb.is_touched = False

    for rb in my_simulation.rigid_bodies:

        if rb.is_touched:
            rb.position = mouse

    # clear screen from last frame
    screen.fill("black")
    pygame.draw.rect(screen, "gray", button_rect)

    screen.blit(font.render("Velocity", 1, "white"), (1500,100))

    screen.blit(update_fps(), (10,0))
    if show_velocity:
        for rb in my_simulation.rigid_bodies:
            start_position = rb.position + (rb.velocity.normalize_vector()*rb.radius)
            end_position = (rb.position + rb.velocity/5)
            pygame.draw.line(screen, "blue", start_pos=start_position.tuple(), end_pos=end_position.tuple())
    if show_force:
        for rb in my_simulation.rigid_bodies:
            start_position = rb.position + (rb.net_force.normalize_vector()*rb.radius)
            end_position = (rb.position + rb.net_force)
            pygame.draw.line(screen, "red", start_pos=start_position.tuple(), end_pos=end_position.tuple())
    # main update
    my_simulation.update(dt)


    # drawing
    for rb in my_simulation.rigid_bodies:
        if not len(rb.connections) == 0:
            for connection in rb.connections:
                
                pygame.draw.line(screen, "red", start_pos=rb.position.tuple(),end_pos=connection.position.tuple())
        
              
        pygame.draw.circle(screen, "white", rb.position.tuple(), rb.radius)
        text_surface = font.render(str(rb.mass), True, "red")
        text_rect = text_surface.get_rect(center=(rb.position.tuple()))
        screen.blit(text_surface, text_rect)
    for c in my_simulation.circles:
        pygame.draw.circle(screen, "white", c.tuple(),c.radius, c.border_width)

    for line in my_simulation.lines:
        pygame.draw.line(screen, "red", start_pos=line.start_point.tuple(), end_pos=line.end_point.tuple())

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()
