import pygame
from .vector import *
from .simulation import Simulation
from .rigid_body import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
fps = 240
dt = 1/ fps

# initialize simulation and add objects
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



colors = ["red","blue","green","yellow","pink","orange"]
run  = True

while run:
    x,y = pygame.mouse.get_pos()
    mouse = Vector(x,y)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False 

        if event.type == pygame.MOUSEBUTTONDOWN:
            for rb in my_simulation.rigid_bodies:

                if is_point_inside(x,y,rb):
                    rb.is_touched = True
                    rb.velocity = Vector(0,0)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                my_simulation.add_a_rigid_body(Rigid_body(mass=50,position=mouse,velocity =Vector(0,0),radius=30,is_fixed=False))

        if event.type == pygame.MOUSEBUTTONUP:

            for rb in my_simulation.rigid_bodies:

                rb.is_touched = False
                
    for rb in my_simulation.rigid_bodies:

        if rb.is_touched:
            rb.position = mouse
     
    #clear screen from last frame
    screen.fill("black")

    
    #main update
    my_simulation.update(dt)
    
 
   
    #drawing
    for rb in  my_simulation.rigid_bodies:
        pygame.draw.circle(screen, "white",rb.position.tuple(), rb.radius)
    for c in my_simulation.circles:
        pygame.draw.circle(screen, "white",c.tuple(), c.radius,c.border_width)
    
    
    for line in my_simulation.lines:
        pygame.draw.line(screen,"red",start_pos=line.start_point.tuple(),end_pos=line.end_point.tuple())

    pygame.draw.line(screen,"red",start_pos=rb1.position.tuple(),end_pos=rb2.position.tuple())

    
            

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

