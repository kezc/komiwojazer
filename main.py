import matplotlib.pyplot as plt

from generator import *
from greedy import *

points = generate(9, 2,2)
# save_to_file("1.txt", points)
# points = read_from_file('tsp1000.txt')
print(points)
result, total_distance = greedy(points)
print(result)
print(f'dystans {total_distance:.2f}')
ns = list(map(lambda x: x[0], result))
print(ns)

xs = list(map(lambda x: x[1], result))
ys = list(map(lambda x: x[2], result))
plt.plot(xs, ys, linestyle='--', marker='o', color='b')
for n, x, y in result[:-1]:
    plt.annotate(n,
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')
plt.show()
