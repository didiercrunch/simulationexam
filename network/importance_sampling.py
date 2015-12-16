from random import Random
from network.network import create_network, get_number_of_activated_antenna


class AntennaGenerator(object):

    def __init__(self, box_size, random):
        self.box_size = box_size
        self._antennas = list(range(box_size * box_size))
        self.random = random

    def get_random_antenna(self):
        idx, prob = self.get_random_index_and_its_probability()
        if idx == -1:
            self._antennas = []
            return -1, prob
        choosen_antenna = self._antennas[idx]
        self._remove_antenna(idx)
        return choosen_antenna, prob


class SuccesiveAntennaGenerator(AntennaGenerator):
    def _remove_antenna(self, idx):
        ant = self._antennas[idx]
        if ant == -1:
            self._antennas = []
            return ant
        if (ant + 1) % self.box_size:
            self._antennas = self._antennas[idx + 2:]
        else:
            self._antennas = self._antennas[idx + 1:]

        if ant + self.box_size < self.box_size * self.box_size:
            self._antennas.remove(ant + self.box_size)

    def get_random_index_and_its_probability(self):
        idx = self.random.randint(-1, len(self._antennas)-1)
        prob = (len(self._antennas) + 1) ** -1
        return idx, prob


class BadAntennaGenerator(SuccesiveAntennaGenerator):
    '''this antenna generator does not return 'real' probabilities
    and thus cannot be used in importance_sampling'''
    def _remove_antenna(self, idx):
        ant = self._antennas[idx]
        to_remove = {ant, ant + self.box_size, ant - self.box_size}
        if (ant + 1) % self.box_size:
            to_remove.add(ant + 1)

        if ant % self.box_size:
            to_remove.add(ant - 1)
        self._antennas = [a for a in self._antennas if a not in to_remove]


class BetterSuccesiveAntennaGenerator(SuccesiveAntennaGenerator):

    def _get_random_index(self, max_number_inclusive):
        if max_number_inclusive < 1:
            return self.random.randint(-1, max_number_inclusive)
        mean_ = max_number_inclusive/2
        x = int(self.random.expovariate(mean_**-1))
        if x > max_number_inclusive:
            return -1
        return x

    def get_random_index_and_its_probability(self):
        idx = self._get_random_index(len(self._antennas)-1)
        prob = (len(self._antennas) + 1) ** -1
        return idx, prob


def get_random_network(box_size, random, Generator):
    antenna_generator = Generator(box_size, random)
    antennas = []
    antenna, network_prob = antenna_generator.get_random_antenna()

    while antenna != -1:
        antennas.append(antenna)
        antenna, p = antenna_generator.get_random_antenna()
        network_prob *= p

    return create_network(antennas), network_prob


def estimate_number_of_activated_antenna(n, box_size, random, Generator):
    ret, sum_of_probs = 0, 0
    for i in range(n):
        network, p = get_random_network(box_size, random, Generator)
        ret += get_number_of_activated_antenna(network) / p
        sum_of_probs += p**-1
    return ret / sum_of_probs
