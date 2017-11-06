
#===============================================================================
# # DESCRIPTION:
# #    Traveling salesman genetic solver.
#===============================================================================

#=========================================================================
# # IMPORTS
#=========================================================================
from random import randrange
from random import shuffle
from math import (sqrt, pow)
from pprint import pprint
from numba import jit  # for speed

#=========================================================================
# # GLOBALS
#=========================================================================

_PRINT_INTERVAL = 100

#=========================================================================
# # FUNCTIONS
#=========================================================================

def generate_destinations(destination_count=20, range_min=0, range_max=100):
    
    '''
    Generates destination_count pseudo-random destinations within range_min to range_max.
    '''
    
    return [(float(randrange(range_min, range_max)),
             float(randrange(range_min, range_max)))
            for x in range(destination_count)]


def generate_destination_populations(destinations, population_size=100):
    
    '''
    Generations population_size pseudo-randomized list of destinations.
    '''
    
    populations = []
    for n in range(population_size):
        dest_copy = destinations[:]
        shuffle(dest_copy)  # shuffle mutates input in-place
        populations.append(dest_copy)
    return populations


@jit
def compute_total_destination_distance(destinations):
    
    '''
    Computes the total distance around a set of destinations.
    '''
    
    total_distance = 0
    previous_dest = destinations[0]
    shifted_dest = destinations[1:]
    shifted_dest.append(destinations[0])
    for dest in shifted_dest:
        total_distance += sqrt(
                (dest[0] - previous_dest[0]) ** 2 + (dest[1] - previous_dest[1]) ** 2 
            ) 

        previous_dest = dest
    return total_distance


def get_random_subset(list_, subset_size=3):
    
    ''' 
    Gets a random subset of size subset_size of a list.
    Start index is also random.
    '''
    
    index = randrange(0, len(list_) - subset_size - 1)
    new_list = [None] * len(list_)
    new_list[index:index + subset_size] = list_[index: index + subset_size]
    return new_list


def mutate_list(list_):
    
    '''
    "Mutates" a list by randomly swapping the value of two indices.
    '''
    
    index0 = 0
    index1 = 0
    while index0 == index1:
        index0 = randrange(0, len(list_) - 1)
        index1 = randrange(0, len(list_) - 1)
    new_list = list_[:]
    new_list[index0], new_list[index1] = new_list[index1], new_list[index0]
    return new_list

def traveling_salesman(generations=5000, population_size=100):
    
    '''
    Main traveling salesman genetic algorithm driver.
    '''

    destinations = generate_destinations(destination_count=population_size)
    population = generate_destination_populations(destinations, population_size)
    
    for n in range(generations):

        population = sorted(
            population,
            key=lambda x: compute_total_destination_distance(x)
        )

        parent1 = population[0]
        parent2 = population[1]

        p1_subset = get_random_subset(parent1, subset_size=int(population_size / 4))
        p2_subset = [x for x in parent2 if x not in p1_subset]
        
        child = []
        for x in p1_subset:
            if x is None:
                child.append(p2_subset.pop())
            else:
                child.append(x)
                
        child1 = mutate_list(child)
        child2 = mutate_list(child)
        
        population[-1] = child1
        population[-2] = child2
    
        if not n % _PRINT_INTERVAL:
            print('Generation %i, distance %f' % (n, compute_total_destination_distance(population[0])))
    
    print('FINISHED: Generation %i, distance %f' % (n, compute_total_destination_distance(population[0])))
    print('RESULT')
    pprint(population[0])
    
if __name__ == "__main__":
    traveling_salesman()

