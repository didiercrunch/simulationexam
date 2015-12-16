from unittest import TestCase
from network.brute_force import (get_all_possible_network,
                                 estimate_number_of_activated_antenna)
from random import Random


class TestBruteForce(TestCase):

    def test_get_all_possible_network(self):
        self.assertEqual(list(get_all_possible_network(0)), [])

        self.assertEqual(list(get_all_possible_network(1)), [0, 1])

        expt = [0, 1, 2, 4, 6, 8, 9]
        self.assertEqual(list(get_all_possible_network(2)), expt)

    def test_estimate_number_of_activated_antenna(self):
        random = Random(666)
        est = estimate_number_of_activated_antenna(7, 2, random)
        self.assertEqual(est, (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7)

        est = estimate_number_of_activated_antenna(100, 2, random)
        self.assertEqual(est, (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7)

        est = estimate_number_of_activated_antenna(3, 2, random)
        self.assertEqual(est, 1)
