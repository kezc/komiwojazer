from generator import *
from greedy import *

points = generate(4)
print(points)
save_to_file("pawel.txt", points)
print(greedy(points))

# instacnce = read_from_file('pawel.txt')
# print(instacnce)
