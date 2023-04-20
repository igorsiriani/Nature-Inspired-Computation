from random import random

import numpy

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
    result_list = []

    for i in range(0, 200):
        result = hill_climbing(10e5, 400)
        result_list.append(result)

    print('Solução máxima: ', max(result_list))
    print('Solução mínima: ', min(result_list))
    print('Solução média: ', numpy.mean(result_list))
    print('Solução padrão: ', numpy.std(result_list))


if __name__ == '__main__':
    main()
