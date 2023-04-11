from random import random
from utils import disturb, evaluate


def hill_climbing(max_it, max_same):
    x = random()
    value = evaluate(x)
    t = 1
    same = 1

    # while t < max_it:
    while t < max_it and same < max_same:
        x_ = disturb(x)
        value_ = evaluate(x_)
        if value < value_:
            x = x_
            value = value_
            same = 1
        else:
            same += 1
        t += 1
    return x


def main():
    result = hill_climbing(10e10, 10e5)
    print('result:', result)


if __name__ == '__main__':
    main()
