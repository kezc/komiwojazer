import random


def generate(n, top=10, right=10, bottom=0, left=0):
    if (top - bottom + 1) * (right - left + 1) < n or top < bottom or right < left:
        raise ValueError("Wrong arguments")
    points = []
    for _ in range(n):
        x = random.randrange(left, right + 1)
        y = random.randrange(bottom, top + 1)
        while (x, y) in points:
            x = random.randrange(left, right + 1)
            y = random.randrange(bottom, top + 1)
        points.append((x, y))
    return points
