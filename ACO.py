from random import randrange, random

from generator import generate, read_from_file, save_to_file


class AntColonyOptimization:
    # cost of traveling from one vertex to another
    costs_matrix = []

    # amounts of pheromones on edge
    pheromones_matrix = []

    vertex_amount = 0

    # how quickly pheromones disappear
    evaporation_rate = 0.5

    # influence of pheromone
    alpha = 1

    # influence of trail level
    beta = 5

    ants_amount = 5

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

    def construct_ant_solutions(self):
        results = []
        for _ in range(self.ants_amount):
            current_vertex = 0
            visited_vertices = [False for _ in range(self.vertex_amount)]
            path_length = 0
            path = [current_vertex]
            while len(path) < self.vertex_amount:
                visited_vertices[current_vertex] = True
                probabilities = self.calculate_probabilities(current_vertex, visited_vertices)
                # generate random number in range <0, probability_denominator>
                random_number = random()
                probabilities_sum = 0
                for vertex, probability in enumerate(probabilities):
                    probabilities_sum += probability
                    if random_number <= probabilities_sum and probability != 0:
                        path_length += self.costs_matrix[current_vertex][vertex]
                        path.append(vertex)
                        current_vertex = vertex
                        break
            path.append(path[0])
            path_length += self.costs_matrix[current_vertex][-1]
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

    def update_pheromones(self):
        pass


if __name__ == '__main__':
    points = generate(500)
    # save_to_file("pawel", points)
    # points = read_from_file('pawel')
    print(points)
    aco = AntColonyOptimization(points)
    print(aco.construct_ant_solutions())
