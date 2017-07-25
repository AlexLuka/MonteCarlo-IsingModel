import math
import numpy as np
from src.settings import Settings


class Model:

    """
        Here we work not with temperature but with beta = inverse_temperature!

    """

    J = 1

    def __init__(self):
        # default size of the system
        self.grid_x = 20
        self.grid_y = 20

        # initial state. later add options: INITIAL_RANDOM, INITIAL_ALL_ONES, INITIAL_ALL_ZEROS
        self.mapping = np.random.randint(low=0, high=2, size=(self.grid_x, self.grid_y))*2 - 1

        # settings. will store some basic features like paths, colors, etc.
        self.settings = Settings()

        # inverse temperature: beta=1/T
        self.beta = 0.4
        self.swapping_energies = {4: 0,
                                  8: 0}
        self.update_swapping_energies()

    def get_inverse_temperature(self):
        return self.beta

    def set_inverse_temperature(self, val):
        self.beta = val

    def get_grid_x(self):
        return self.grid_x

    def set_grid_x(self, val):
        self.grid_x = val

    def get_grid_y(self):
        return self.grid_y

    def set_grid_y(self, val):
        self.grid_y = val

    def init_mapping(self):
        self.mapping = np.zeros(shape=(self.grid_x, self.grid_y))

    def get_mapping(self):
        return self.mapping

    def get_settings(self):
        return self.settings

    def update_swapping_energies(self):
        for var in [4, 8]:
            self.swapping_energies[var] = math.exp(-float(var) * self.beta)

    def update_model(self):
        self.mapping = np.random.randint(low=0, high=2, size=(self.grid_x, self.grid_y)) * 2 - 1

    # calculate initial energy of the system
    def calculate_energy(self):
        print self.grid_x, self.grid_y

        energy = 0
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                energy += self.calculate_energy_delta(i, j)

        return energy / 4

    def calculate_energy_delta(self, i, j):
        return 2 * self.J * self.mapping[i, j] * (self.mapping[(i+1) % self.grid_x, j] +
                                                  self.mapping[i, (j+1) % self.grid_y] +
                                                  self.mapping[i-1, j] +
                                                  self.mapping[i, j-1])

    def run(self):
        energy = self.calculate_energy()

        sw = self.grid_x * self.grid_y

        while True:
            #
            # One sweep
            r = np.random.uniform(0, 1, size=sw)
            i_x = np.random.randint(0, self.grid_x, sw)
            i_y = np.random.randint(0, self.grid_y, sw)
            # print r[0:10]

            # Metropolis dynamics
            for r_val, ind_x, ind_y in zip(list(r), list(i_x), list(i_y)):
                de = self.calculate_energy_delta(ind_x, ind_y)

                if de <= 0:
                    self.mapping[ind_x, ind_y] *= -1
                    energy += de
                else:
                    if r_val < self.swapping_energies[de]:
                        self.mapping[ind_x, ind_y] *= -1
                        energy += de
            print 'Energy: ', energy
