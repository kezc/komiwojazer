import matplotlib.pyplot as plt

from ACO import AntColonyOptimization
from generator import *
from greedy import *

if __name__ == '__main__':
    # points = generate(4, 15, 15)
    # save_to_file("1.txt", points)
    points = read_from_file('tsp1000.txt')
    print(points)
    result, total_distance = greedy(points)
    ns = list(map(lambda x: x[0], result))
    # print("greedy:", result)
    print("greedy:", ns)

    print(f'dystans {total_distance:.2f}')
    # for i in range(2, 5):
    #     for _ in range(5):
    aco = AntColonyOptimization(points)
    resultAco, total_distance_aco = aco.do_iterations()
    # print("aco", resultAco)
    print(f'beta  dystans {total_distance_aco:.2f}')

    xs = list(map(lambda x: x[0], aco.best_in_iterations))
    ys = list(map(lambda x: x[1], aco.best_in_iterations))
    print()
    # exit()
    # print("xs", xs)
    # print("ys", ys)
    plt.plot(xs, ys)
    plt.show()
    plt.savefig("wojtek.png")

    # fig, axs = plt.subplots(2)
    # fig.set_figheight(8)
    # fig.set_figwidth(4)
    #
    # xs = list(map(lambda x: x[1], result))
    # ys = list(map(lambda x: x[2], result))
    # axs[0].plot(xs, ys, linestyle='--', marker='o', color='b')
    # axs[0].set_title("Greedy")
    # for n, x, y in result[:-1]:
    #     axs[0].annotate(n,
    #                  (x, y),
    #                  textcoords="offset points",
    #                  xytext=(0, 10),
    #                  ha='center')
    #
    # xs = list(map(lambda x: points[x - 1][1], resultAco))
    # ys = list(map(lambda x: points[x - 1][2], resultAco))
    # axs[1].plot(xs, ys, linestyle='--', marker='o', color='b')
    # axs[1].set_title("ACO")
    # for n, x, y in zip(resultAco, xs, ys):
    #     axs[1].annotate(n,
    #                  (x, y),
    #                  textcoords="offset points",
    #                  xytext=(0, 10),
    #                  ha='center')
    # plt.show()
