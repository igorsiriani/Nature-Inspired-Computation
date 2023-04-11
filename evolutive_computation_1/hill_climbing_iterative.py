from random import random
from hill_climbing import hill_climbing, evaluate


def iterative_hill(n_start, max_it, max_same):
    t = 0
    x = random()
    print('initial:', x)
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
    result = iterative_hill(10e3, 10e3, 10e2)
    print('result:', result)


if __name__ == '__main__':
    main()
