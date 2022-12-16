import random as rd
import numpy as np

class Brain():
    '''le cerveau des points'''
    def __init__(self, size):
        self.step = 0
        self.directions = np.array([np.array([rd.uniform(-1000000,1000000), rd.uniform(-1000000,1000000)]) for i in range(size)])   #randomly filled, numbers can be changed: they only impact the accceleration of the dot (be careful to be in accordance with the framerate: a too fast dot can be "teleported" over obstacles for example)
        
    def clone(self):
        clone = Brain(self.directions.shape[0])
        for i in range(self.directions.shape[0]): 
            clone.directions[i] = self.directions[i].copy()
        return clone
        
    def mutate(self, mutation_rate):
        '''mutates the brain by setting some of the directions to random vectors'''
        for i in range(self.directions.shape[0]):
            rand = rd.random()
            if rand < mutation_rate:
                #there is mutation ie random direction
                self.directions[i] = np.array([rd.uniform(-100,100), rd.uniform(-100,100)])