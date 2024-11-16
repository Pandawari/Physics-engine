import pygame
from rigid_body import *
from vector import *
from simulation import * 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
fps = 240
dt = 1/ fps




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

