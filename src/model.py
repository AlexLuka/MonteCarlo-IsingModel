import math
import itertools
import numpy as np
from src.settings import Settings


class Model:

    """
        Here we work not with temperature but with beta = inverse_temperature!

    """

    J = 1

    def __init__(self):
        # default size of the system
        self.grid_x = 100
        self.grid_y = 100

        # initial state. later add options: INITIAL_RANDOM, INITIAL_ALL_ONES, INITIAL_ALL_ZEROS
        self.mapping = np.random.randint(low=0, high=2, size=(self.grid_x, self.grid_y))*2 - 1

        # settings. will store some basic features like paths, colors, etc.
        self.settings = Settings()

        # inverse temperature: beta=1/T
        self.beta = 0.33
        self.swapping_energies = {4: 0,
                                  8: 0}
        self.update_swapping_energies()

        #
        self.is_running_flag = True

        #
        self.magnetization = []

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

    def get_magnetization(self):
        return self.magnetization

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

    def calculate_magnetization(self):
        return np.sum(self.mapping.flatten()) / float(self.grid_x * self.grid_y)

    def set_running_flag(self, val):
        self.is_running_flag = val

    def run(self, queue):
        energy = self.calculate_energy()
        m = self.calculate_magnetization()

        sw = self.grid_x * self.grid_y

        self.is_running_flag = True
        self.update_swapping_energies()
        self.magnetization.append(m)

        while self.is_running_flag:
            #
            # One sweep
            r = np.random.uniform(0, 1, size=sw)

            # Metropolis dynamics
            for r_val, (ind_x, ind_y) in zip(list(r), itertools.product(range(0, self.grid_x), range(0, self.grid_y))):
                de = self.calculate_energy_delta(ind_x, ind_y)

                if de <= 0:
                    self.mapping[ind_x, ind_y] *= -1
                    energy += de
                    m += 2*self.mapping[ind_x, ind_y] / float(sw)
                else:
                    # print r_val, self.swapping_energies[de]
                    if r_val < self.swapping_energies[de]:
                        self.mapping[ind_x, ind_y] *= -1
                        energy += de
                        m += 2 * self.mapping[ind_x, ind_y] / float(sw)
                        # print 'Accepted'
            self.magnetization.append(m)
        print 'Model was stopped'
        queue.put('STOP')
        return
