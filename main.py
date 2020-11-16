import matplotlib.pyplot as plt

from generator import *
from greedy import *

# save_to_file("pawel.txt", points)
# points = generate(4)
points = read_from_file('pawel.txt')
print(points)
result = greedy(points)
print(result)
ns = list(map(lambda x: x[0], result))
print(ns)

xs = list(map(lambda x: x[1], result))
ys = list(map(lambda x: x[2], result))
plt.plot(xs + [xs[0]], ys + [ys[0]], linestyle='--', marker='o', color='b')
for n, x, y in zip(ns, xs, ys):
    plt.annotate(n,
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')
plt.show()
