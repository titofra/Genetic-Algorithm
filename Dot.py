import numpy as np
import random as rd
import pygame
from pygame import gfxdraw
from Brain import Brain

class Dot():
    '''Un point'''
    
    def __init__(self, T, screen, goal):
        self.brain = Brain(1000)    #new brain with 1000 instructions
        
        self.fitness = -1
        
        self.pos = np.array([screen.get_size()[0]/2, screen.get_size()[1] - 10], dtype=float)
        self.vel = np.array([0,0], dtype=float)
        self.acc = np.array([0,0], dtype=float)
        self.goal = goal
        self.T = T
        self.screen = screen
        self.is_dead = False
        self.has_reached_goal = False
    
    def show(self, surf):
        #s = pygame.Surface(self.screen.get_size())
        pygame.gfxdraw.filled_circle(surf, int(self.pos[0]), int(self.pos[1]), 1, (255,255,255))
        #self.screen.blit(s, (0, 0))
        
    def move(self):
        if self.brain.step < self.brain.directions.shape[0]:
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            is_dead = True  #if at the end of the directions array then the dot is dead
    
        #apply the acceleration and move the dot
        self.vel += self.acc * self.T
        self.pos += self.vel* self.T
            
    def update(self, surf):
        '''calls the move function and check for collisions and stuff'''
        if not self.is_dead and not self.has_reached_goal:
            self.move()
            
            #borders
            if self.pos[0] > self.screen.get_size()[0]:
                self.pos[0] = self.screen.get_size()[0]
                self.is_dead = True
            if self.pos[1] > self.screen.get_size()[1]:
                self.pos[1] = self.screen.get_size()[1]
                self.is_dead = True
            if self.pos[0] < 0:
                self.pos[0] = 0
                self.is_dead = True
            if self.pos[1] < 0:
                self.pos[1] = 0
                self.is_dead = True
            #obstacles (we must first verify if it is not already dead)
            if not self.is_dead and surf.get_at((int(self.pos[0]), int(self.pos[1])))[:3] == (0,255,0):
                self.is_dead = True
            #goal
            if np.sqrt((self.pos[0]-self.goal[0])**2 + (self.pos[1]-self.goal[1])**2) <= 2:
                self.has_reached_goal = True
            
    def calculate_fitness(self):
        if self.has_reached_goal:
            self.fitness = 1.0/16.0 + 10000.0/(self.brain.step**2)
        else:
            self.fitness = 1.0/np.sqrt((self.pos[0]-self.goal[0])**2 + (self.pos[1]-self.goal[1])**2)
           
    def give_birth(self):
        baby = Dot(self.T, self.screen, self.goal)
        baby.brain = self.brain.clone()
        return baby