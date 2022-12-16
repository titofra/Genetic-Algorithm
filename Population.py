import numpy as np
import random as rd
from Dot import Dot

class Population():
    def __init__(self, size, T, screen, goal, mutation_rate = 1/100):
        self.gen = 1
        self.T = T
        self.screen = screen
        self.goal = goal
        self.mutation_rate = mutation_rate
        self.dots = np.array([Dot(self.T, self.screen, self.goal) for i in range(size)])
        self.fitness_sum = -1
        
    def show(self, surf):
        for i in range(self.dots.shape[0]):
            self.dots[i].show(surf)
            
    def are_all_dots_dead(self):
        '''returns whether all the dots are either dead or have reached the goal'''
        for i in range(self.dots.shape[0]):
            if not self.dots[i].is_dead and not self.dots[i].has_reached_goal:
                return False
        return True
        
    def update(self, surf):
        for i in range(self.dots.shape[0]):
            self.dots[i].update(surf)
            
    def calculate_fitness(self):
        for i in range(self.dots.shape[0]):
            self.dots[i].calculate_fitness()
    
    def natural_selection(self):
        '''gets the next generation of dots'''
        new_dots = np.array([Dot(self.T, self.screen, self.goal) for i in range(self.dots.shape[0])])
        
        #find the best dot
        best_dot = 0
        for i in range(1, self.dots.shape[0]):
            if self.dots[i].fitness > self.dots[best_dot].fitness:
                best_dot = i
          
        #calculate the sum of fitnesses
        fitness_sum = 0
        for i in range(1, self.dots.shape[0]):
            fitness_sum += self.dots[i].fitness
        self.fitness_sum = fitness_sum
        
        #best dot lives on
        new_dots[0] = self.dots[best_dot].give_birth()
        
        #select parent and get babies (chooses dot from the population to return randomly(considering fitness))
        #This works by randomly choosing a value between 0 and the sum of all the fitnesses then go through all the dots and add their fitness to a running sum and if that sum is greater than the random value generated that dot is chosen since dots with a higher fitness function add more to the running sum then they have a higher chance of being chosen
        for i in range(1, self.dots.shape[0]):
            parent = self.select_fitness()
            new_dots[i] = parent.give_birth()
        
        #New gen !!!
        self.dots = new_dots
        self.gen += 1
        
    def select_fitness(self):
        #choose a random number in [0,fitness_sum)
        rand = rd.random()*self.fitness_sum
        
        running_sum = 0
        for i in range(self.dots.shape[0]):
            running_sum += self.dots[i].fitness
            if running_sum > rand:
                return self.dots[i]
        
        return None #impossible
        
        
    def mutation(self):
        '''mutates all the brains of the babies'''
        for i in range(self.dots.shape[0]):
            self.dots[i].brain.mutate(self.mutation_rate)