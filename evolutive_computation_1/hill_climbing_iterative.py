from random import random

import numpy

from hill_climbing import hill_climbing, evaluate


def iterative_hill(n_start, max_it, max_same):
    t = 0
    x = random()
    value = evaluate(x)

    while t < n_start:
        x_ = hill_climbing(max_it, max_same)
        value_ = evaluate(x_)
        if value < value_:
            value = value_
            x = x_
        t += 1
    return x


def main():
    result_list = []

    for i in range(0, 200):
        result = iterative_hill(10e2, 10e3, 400)
        result_list.append(result)

    print('Solução máxima: ', max(result_list))
    print('Solução mínima: ', min(result_list))
    print('Solução média: ', numpy.mean(result_list))
    print('Solução padrão: ', numpy.std(result_list))


if __name__ == '__main__':
    main()
