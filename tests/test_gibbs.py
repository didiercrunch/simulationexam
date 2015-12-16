from unittest import TestCase
from random import Random
from math import sqrt
from collections import defaultdict
from network.gibbs import get_random_networks, estimate_number_of_activated_antenna


def standard_deviation(lst):
    sum_x = 0
    sum_x_2 = 0
    for elm in lst:
        sum_x += elm
        sum_x_2 += elm * elm

    n = len(lst)
    return sqrt(sum_x_2 / n - (sum_x / n)**2)


class TestGibbs(TestCase):

    def test_get_random_networks(self):
        counter = defaultdict(int)
        random, n = Random(555), 1000
        for _, network in zip(range(n), get_random_networks(2, random)):
            counter[network] += 1

        self.assertSetEqual(set(counter.keys()), {0, 1, 2, 4, 6, 8, 9})
        self.assertLess(standard_deviation(counter.values()) / n, 0.1)

    def test_estimate_number_of_activated_antenna(self):
        random = Random(666)

        est = estimate_number_of_activated_antenna(100, 2, random)
        real = (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7
        assert abs(est - real) < 0.1
