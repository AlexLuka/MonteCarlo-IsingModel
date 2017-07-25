import numpy as np


def test1():
    i_x = np.random.randint(0, 20, size=10000)
    i_y = np.random.randint(0, 20, size=10000)

    import matplotlib.pyplot as plt
    plt.plot(i_x, i_y, 'o')
    plt.show()


def main():
    test1()


if __name__ == '__main__':
    main()
