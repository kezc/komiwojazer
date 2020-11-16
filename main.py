import matplotlib.pyplot as plt

from generator import *
from greedy import *

# save_to_file("pawel.txt", points)
# points = generate(4)
points = read_from_file('pawel.txt')
print(points)
result, total_distance = greedy(points)
print(result)
print(f'dystans {total_distance:.2f}')
ns = list(map(lambda x: x[0], result))
print(ns)

xs = list(map(lambda x: x[1], result))
ys = list(map(lambda x: x[2], result))
plt.plot(xs, ys, linestyle='--', marker='o', color='b')
for n, x, y in zip(ns[:-1], xs[:-1], ys[:-1]):
    plt.annotate(n,
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')
plt.show()
