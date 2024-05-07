import itertools
import numpy as np
import random

class Two_opt:
    def __init__(self, distance_matrix, initial_route=None):
        """Initialize the Solver class with a distance matrix and an optional initial route."""
        self.distance_matrix = distance_matrix
        self.num_cities = len(self.distance_matrix)
        self.initial_route = initial_route or self.generate_random_route()
        self.best_route = self.initial_route
        self.best_distance = self.calculate_path_dist(self.best_route)
        self.distances = []  # Stores distances during optimization iterations

    def generate_random_route(self):
        """Generate a random initial route."""
        route = list(range(self.num_cities))
        random.shuffle(route[1:])  # Keep city 0 as the starting point
        return route

    def update(self, new_route, new_distance):
        """Update the best known route and distance."""
        self.best_distance = new_distance
        self.best_route = new_route
        self.distances.append(new_distance)
        return self.best_distance, self.best_route

    def two_opt(self, improvement_threshold=0.01, max_restarts=5):
        """Apply the 2-opt optimization technique to improve the route."""
        improvement_factor = 1
        restarts = 0

        while improvement_factor > improvement_threshold and restarts < max_restarts:
            previous_best = self.best_distance

            # Attempt all possible swaps of non-adjacent cities
            for i in range(1, self.num_cities - 1):
                for j in range(i + 1, self.num_cities):
                    # Swap segment between city i and city j
                    new_route = self.swap(self.best_route, i, j)
                    new_distance = self.calculate_path_dist(new_route)

                    if new_distance < self.best_distance:
                        self.update(new_route, new_distance)

            improvement_factor = 1 - self.best_distance / previous_best
            if improvement_factor < improvement_threshold:
                # Random restart to escape local minima
                self.best_route = self.generate_random_route()
                restarts += 1

        return self.best_route, self.best_distance, self.distances

    def calculate_path_dist(self, route):
        """Calculate the total distance of a given route using the distance matrix."""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        return round(total_distance, 2)

    def swap(self, route, i, j):
        """Swap and reverse the segment between indices i and j."""
        swapped_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
        return swapped_route


# Distance matrix based on given example
distance_matrix = [
    [0, 2800, 800, 1800, 2500],   # LA distances
    [2800, 0, 2000, 1000, 300],   # NYC distances
    [800, 2000, 0, 1000, 1800],   # Chicago distances
    [1800, 1000, 1000, 0, 800],   # Las Vegas distances
    [2500, 300, 1800, 800, 0]     # Seattle distances
]

cities = ['LA', 'NYC', 'Chicago', 'Las Vegas', 'Seattle']

solver = Two_opt(distance_matrix)
best_route, best_distance, distances = solver.two_opt()

# Convert best route to city names
best_route_named = [cities[i] for i in best_route]

print("Best Distance:", best_distance)
print("Best Route:", best_route_named)
