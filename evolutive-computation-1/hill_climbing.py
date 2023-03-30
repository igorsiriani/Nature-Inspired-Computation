import math
from random import random
import numpy as np
import matplotlib.pyplot as plt


def hill_climbing(max_it, max_same):
    x = random()
    value = evaluate(x)
    t = 1
    same = 1

    while t < max_it and same < max_same:
    # while t < max_it:
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


def evaluate(x):
    result = 2 ** (-2 * ((x - 0.1) / 0.9) ** 2) * (math.sin(5 * math.pi * x)) ** 6
    return result


def disturb(x):
    result = np.random.normal(0, 0.000001)
    return result + x


def test_calc():
    x = 0
    value = evaluate(x)
    x_list = []
    v_list = []

    while x <= 1:
        x_list.append(x)
        v_list.append(value)

        x += 0.001
        value = evaluate(x)

    return x_list, v_list


def main():
    result = hill_climbing(10e10, 10e5)
    print('result:', result)

    # x_list, v_list = test_calc()
    # plt.plot(x_list, v_list)
    # plt.show()


if __name__ == '__main__':
    main()
