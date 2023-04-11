from random import random
import numpy as np
from utils import disturb, evaluate


def stochastic_hill_climbing(max_it, max_same, t_prob):
    x = random()
    value = evaluate(x)
    t = 1
    same = 1

    # while t < max_it:
    while t < max_it and same < max_same:
        x_ = disturb(x)
        value_ = evaluate(x_)

        prob = (1 / (1 + np.exp((value - value_) / t_prob)))
        rand = random()

        print('Prob:', prob, ' - rand:', rand)
        print('value:', value, ' - value_:', value_)

        if rand < prob:
            x = x_
            value = value_
            same = 1
        else:
            same += 1
        t += 1

    return x


def main():
    result = stochastic_hill_climbing(10e5, 10e3, 0.0001)
    print('result:', result)


if __name__ == '__main__':
    main()
