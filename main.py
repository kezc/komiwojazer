import matplotlib.pyplot as plt

from ACO import AntColonyOptimization
from generator import *
from greedy import *

# points = generate(500)
# save_to_file("1.txt", points)
points = read_from_file('1.txt')
print(points)
result, total_distance = greedy(points)
ns = list(map(lambda x: x[0], result))
# print("greedy:", result)
print("greedy:", ns)

print(f'dystans {total_distance:.2f}')

aco = AntColonyOptimization(points)
resultAco, total_distance_aco = aco.do_iterations()
print("aco", resultAco)
print(f'dystans {total_distance_aco:.2f}')


fig, axs = plt.subplots(2)
fig.set_figheight(8)
fig.set_figwidth(4)

xs = list(map(lambda x: x[1], result))
ys = list(map(lambda x: x[2], result))
axs[0].plot(xs, ys, linestyle='--', marker='o', color='b')
axs[0].set_title("Greedy")
for n, x, y in result[:-1]:
    axs[0].annotate(n,
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')

xs = list(map(lambda x: points[x - 1][1], resultAco))
ys = list(map(lambda x: points[x - 1][2], resultAco))
axs[1].plot(xs, ys, linestyle='--', marker='o', color='b')
axs[1].set_title("ACO")
for n, x, y in zip(resultAco, xs, ys):
    axs[1].annotate(n,
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')
plt.show()
