import sys
from random import random, randrange

from generator import generate


class AntColonyOptimization:
    # cost of traveling from one vertex to another
    costs_matrix = []

    # amounts of pheromones on edge
    pheromones_matrix = []

    vertex_amount = 0

    # how quickly pheromones disappear
    evaporation_rate = 0.1

    # influence of pheromone
    alpha = 15

    # influence of trail level
    beta = 200

    ants_amount = 100

    iterations = 100

    best = ([], sys.maxsize)

    def __init__(self, points):
        self.vertex_amount = len(points)
        self.init_matrices(points)

    def init_matrices(self, points):
        for id1, x1, y1 in points:
            current_vertex_costs = []
            current_vertex_pheromones = []
            for id2, x2, y2 in points:
                # distance from vertex to itself is zero
                # we avoid dividing by zero
                if id1 == id2:
                    current_vertex_costs.append(0)
                    current_vertex_pheromones.append(0)
                else:
                    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
                    current_vertex_costs.append(distance)
                    # initialize pheromones with 1 / distance between path
                    current_vertex_pheromones.append(1 / distance)
            self.costs_matrix.append(current_vertex_costs)
            self.pheromones_matrix.append(current_vertex_pheromones)

    def do_iterations(self):
        for i in range(self.iterations):
            print(i, end=" ")
            solutions = self.construct_ant_solutions()
            _best = min(solutions, key=lambda x: x[1])
            if _best[1] < self.best[1]:
                self.best = _best
            self.update_pheromones(solutions)
        print()
        return list(map(lambda x: x + 1, self.best[0])), self.best[1]

    def construct_ant_solutions(self):
        results = []
        for i in range(self.ants_amount):
            current_vertex = randrange(self.vertex_amount)
            visited_vertices = [False for _ in range(self.vertex_amount)]
            path_length = 0
            path = [current_vertex]
            while len(path) < self.vertex_amount:
                visited_vertices[current_vertex] = True
                probabilities = self.calculate_probabilities(current_vertex, visited_vertices)
                random_number = random()  # generate random number in range <0, 1)
                probabilities_sum = 0
                for vertex, probability in enumerate(probabilities):
                    probabilities_sum += probability
                    if random_number <= probabilities_sum and probability != 0:
                        path_length += self.costs_matrix[current_vertex][vertex]
                        # print(self.costs_matrix[current_vertex][vertex])
                        path.append(vertex)
                        current_vertex = vertex
                        break
            path.append(path[0])
            path_length += self.costs_matrix[current_vertex][path[-1]]
            results.append((path, path_length))
        return results

    def calculate_probabilities(self, current_vertex, visited_edges):
        pheromones = self.pheromones_matrix[current_vertex]
        costs = self.costs_matrix[current_vertex]
        numerators = []
        denominator = 0
        for pheromone, cost, visited in zip(pheromones, costs, visited_edges):
            if visited or cost == 0:
                value = 0
            else:  # not visited
                # calculate with formula
                value = pheromone ** self.alpha + (1 / cost) ** self.beta
            numerators.append(value)
            denominator += value
        return list(map(lambda numerator: numerator / denominator, numerators))

    def update_pheromones(self, solutions):
        for i in range(self.vertex_amount):
            for j in range(self.vertex_amount):
                self.pheromones_matrix[i][j] *= (1 - self.evaporation_rate)
        for path, path_length in solutions:
            delta_pheromone = 1 / path_length
            for i in range(len(path) - 1):
                vertex1 = path[i]
                vertex2 = path[i + 1]
                self.pheromones_matrix[vertex1][vertex2] += delta_pheromone
                self.pheromones_matrix[vertex2][vertex1] += delta_pheromone
        # for line in self.pheromones_matrix:
        #     print(line)


if __name__ == '__main__':
    points = generate(50)
    # save_to_file("pawel", points)
    # points = read_from_file('pawel')
    print(points)
    aco = AntColonyOptimization(points)
    aco.do_iterations()
