import random


def generate(n, top=750, right=750, bottom=0, left=0):
    if (top - bottom + 1) * (right - left + 1) < n or top < bottom or right < left:
        raise ValueError("Wrong arguments")
    points = []
    for i in range(n):
        x = random.randrange(left, right + 1)
        y = random.randrange(bottom, top + 1)
        while (x, y) in list(map(lambda p: (p[1], p[2]), points)):
            x = random.randrange(left, right + 1)
            y = random.randrange(bottom, top + 1)
        points.append((i + 1, x, y))
    return points


def save_to_file(file_name, instance):
    with open(file_name, 'w') as file:
        file.write(f'{len(instance)}\n')
        for line in instance:
            file.write(f'{line[0]} {line[1]} {line[2]}\n')


def read_from_file(file_name):
    instance = []
    with open(file_name, 'r') as file:
        lines = file.read().splitlines()
        n = int(lines[0])
        for i in range(n):
            instance.append(list(map(lambda x: int(x), lines[i + 1].strip().split())))
    return instance
