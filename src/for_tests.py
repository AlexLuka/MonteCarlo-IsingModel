import numpy as np


def test1():
    i_x = np.random.randint(0, 20, size=10000)
    i_y = np.random.randint(0, 20, size=10000)

    import matplotlib.pyplot as plt
    plt.plot(i_x, i_y, 'o')
    plt.show()


def test2():
    import itertools

    list1 = range(0, 10)
    list2 = range(0, 5)

    for a, b in itertools.product(list1, list2):
        print a, b



def main():
    test2()


if __name__ == '__main__':
    main()
