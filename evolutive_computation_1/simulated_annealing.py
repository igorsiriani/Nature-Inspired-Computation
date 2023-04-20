from random import random

import numpy
import numpy as np
from utils import disturb, evaluate


def simulated_annealing(max_it, temperature, k_max, max_same):
    x = 0
    x_best = x
    t = 1
    temp = temperature
    same = 0

    while t < max_it:
        x = random()
        value = evaluate(x)
        x_ = looping(x, value, k_max, temp)
        value_ = evaluate(x_)

        if evaluate(x_best) < value_:
            x_best = x_
            same = 0
        else:
            same += 1
            if same > max_same:
                return x_best

        if temp < 0.0001:
            temp = temperature
        else:
            temp = temp * 0.9
        t += 1
    return x_best


def looping(x, value, k_max, temp):
    k = 1

    while k < k_max:
        x_ = disturb(x)
        value_ = evaluate(x_)

        prob = np.exp((value_ - value) / temp)
        rand = random()

        if value > value_:
            x = x_
            value = value_
        elif rand < prob:
            x = x_
            value = value_
        k += 1

    return x


def main():
    result_list = []

    for i in range(0, 200):
        result = simulated_annealing(10e3, 10, 10e2, 400)
        result_list.append(result)

    print('Solução máxima: ', max(result_list))
    print('Solução mínima: ', min(result_list))
    print('Solução média: ', numpy.mean(result_list))
    print('Solução padrão: ', numpy.std(result_list))


if __name__ == '__main__':
    main()
