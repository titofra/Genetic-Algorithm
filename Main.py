import time
import numpy as np
import pygame
from pygame import gfxdraw
from Population import Population

#init screen
pygame.init()
screen = pygame.display.set_mode((1000,700))
screen.fill((255, 0, 0))

goal = np.array([screen.get_size()[0]//2, 10])
T = 0.001    #framerate = 1/T
pop = Population(5000, T, screen, goal)

try:
    while True:
        print("Generation", pop.gen)
        
        #while there is a dot alive
        while not pop.are_all_dots_dead():
            beg_tic = time.process_time()

            #draw goal
            surf = pygame.Surface(screen.get_size())
            pygame.gfxdraw.filled_circle(surf, goal[0], goal[1], 2, (255,0,0))
            
            #draw obstacles
            pygame.draw.line(surf, (0,255,0), (0, 400), (800, 150), 20)
            pygame.draw.line(surf, (0,255,0), (850, 500), (600, 700), 20)
            
            #update & show dots
            pop.update(surf)
            pop.show(surf)
            
            #update display
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            
            #wait if needed, to get a perfect framerate (indeed it's useless)
            end_tic = time.process_time()
            time.sleep(max(0, T - (end_tic - beg_tic)))
         
        #let's create the new generation
        pop.calculate_fitness()
        pop.natural_selection()
        pop.mutation()
finally:
    pygame.quit()