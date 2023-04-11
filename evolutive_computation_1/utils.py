import math
import numpy as np


def evaluate(x):
    result = 2 ** (-2 * ((x - 0.1) / 0.9) ** 2) * (math.sin(5 * math.pi * x)) ** 6
    return result


def disturb(x):
    result = np.random.normal(0, 0.0001)
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
