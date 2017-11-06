# Traveling Salesman Genetic Algorithm

With the goal of exploring genetic algorithms, this is a Python-based implementation of the Traveling Salesman problem.

# Design

The script generates a random set of destinations, then shuffles the order of the destinations to produce a population. The genetic algorithm then computes the travel distance of each individual in the population and uses that value as the sorting key. The two shortest routes are used as "parents". A random subset of destinations from one parent is "crossed" with the remainder in the other parent to produce a child. The child is mutated twice using random index swapping to produce two offspring which replace the longest two individuals in the population. The process repeats for the specified number of generations.

# Dependencies

The only dependency is Numba (pip install numba), which provides JIT compiling to the distance compute algorithm, and a 100x speed-up to the algorithm.
