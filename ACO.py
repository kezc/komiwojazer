import sys
import timeit
from multiprocessing import Pool
from random import random, randrange

from generator import generate


class AntColonyOptimization:
    # cost of traveling from one vertex to another
    costs_matrix = []

    # amounts of pheromones on edge
    pheromones_matrix = []

    iterations = 200

    max_single_iteration_time = 0

    passed_time = 0

    best = ([], sys.maxsize)

    # def __init__(self, points):
    def __init__(self, points, evaporation_rate=0.5, alpha=3, beta=5, ants_amount=20, Q=1, max_time=60):
        # how quickly pheromones disappear
        self.Q = Q
        self.evaporation_rate = evaporation_rate
        # influence of pheromone
        self.alpha = alpha
        # influence of trail level
        self.beta = beta
        # self.ants_amount = ants_amount
        self.ants_amount = ants_amount
        self.max_time = max_time
        self.vertex_amount = len(points)
        self.init_matrices(points)

    def init_matrices(self, points):
        from greedy import greedy
        result, total_distance = greedy(points)
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
                    # # initialize pheromones with 1 / distance between path
                    # current_vertex_pheromones.append(self.vertex_amount / total_distance)
                    current_vertex_pheromones.append(self.Q / distance)
                    # current_vertex_pheromones.append(0.0001)
            self.costs_matrix.append(current_vertex_costs)
            self.pheromones_matrix.append(current_vertex_pheromones)

    best_in_iterations = []

    def do_iterations(self):
        itstart = timeit.default_timer()
        with Pool(8) as p:
            i = 0
            for i in range(self.iterations):
                # while True:
                start = timeit.default_timer()
                print(i, end=" ", flush=True)
                i += 1
                # print(self.pheromones_matrix)
                solutions = p.map(self.single_solution,
                                  [(self.costs_matrix, self.pheromones_matrix) for _ in range(self.ants_amount)])
                _best = min(solutions, key=lambda x: x[1])
                self.best_in_iterations.insert(len(self.best_in_iterations), (i, _best[1]))
                if _best[1] < self.best[1]:
                    self.best = _best
                self.update_pheromones(solutions)
                time = timeit.default_timer() - start
                self.passed_time += time
                self.max_single_iteration_time = max(self.max_single_iteration_time, time)
                if self.passed_time + self.max_single_iteration_time > self.max_time:
                    break
            print()
        itstop = timeit.default_timer()
        print('Time: ', itstop - itstart)
        return list(map(lambda x: x + 1, self.best[0])), self.best[1]

    def single_solution(self, args):
        self.costs_matrix, self.pheromones_matrix = args  # windows hack to share memory
        current_vertex = randrange(self.vertex_amount)
        visited_vertices = [False for _ in range(self.vertex_amount)]
        path_length = 0
        path = [current_vertex]
        while len(path) < self.vertex_amount:
            visited_vertices[current_vertex] = True
            probabilities = self.calculate_probabilities(current_vertex, visited_vertices)
            # print(probabilities)
            # print(self.costs_matrix[current_vertex])
            # print()
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
        return (path, path_length)

    def calculate_probabilities(self, current_vertex, visited_edges, calculate_beta=True):
        pheromones = self.pheromones_matrix[current_vertex]
        costs = self.costs_matrix[current_vertex]
        numerators = []
        denominator = 0
        for pheromone, cost, visited in zip(pheromones, costs, visited_edges):
            if visited or cost == 0:
                value = 0
            else:  # not visited
                # calculate with formula
                value = (self.Q / cost) ** self.beta
                if calculate_beta:
                    value *= pheromone ** self.alpha
            numerators.append(value)
            denominator += value
        if denominator > 0:
            result = list(map(lambda numerator: numerator / denominator, numerators))
        else:
            result = self.calculate_probabilities(current_vertex, visited_edges, False)
        return result

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
