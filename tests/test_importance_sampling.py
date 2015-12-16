from unittest import TestCase
from random import Random
from network.importance_sampling import (AntennaGenerator,
                                         SuccesiveAntennaGenerator,
                                         BadAntennaGenerator,
                                         BetterSuccesiveAntennaGenerator,
                                         estimate_number_of_activated_antenna)


class TestSuccesiveAntennaGenerator(TestCase):
    def test_get_random_antenna(self):
        self.antenna_genetator = SuccesiveAntennaGenerator(5, Random(678))

        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(ant, 2)
        expt = [4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        self.assertListEqual(self.antenna_genetator._antennas, expt)

        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(ant, 14)
        expt = [15,16,17,18,20,21,22,23,24]
        self.assertListEqual(self.antenna_genetator._antennas, expt)

        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(ant, -1)
        expt = []
        self.assertListEqual(self.antenna_genetator._antennas, expt)

    def test_get_random_antenna_bottom_line(self):
        self.antenna_genetator = SuccesiveAntennaGenerator(5, Random(607))
        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(ant, 21)
        expt = [23, 24, ]
        self.assertListEqual(self.antenna_genetator._antennas, expt)

    def test_get_random_antenna_right_line(self):
        self.antenna_genetator = SuccesiveAntennaGenerator(5, Random(637))
        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(ant, 14)
        expt = [15, 16, 17, 18, 20, 21, 22, 23, 24]
        self.assertListEqual(self.antenna_genetator._antennas, expt)

    def test_get_random_antenna_last_box(self):
        self.antenna_genetator = SuccesiveAntennaGenerator(5, Random(631))
        ant, _ = self.antenna_genetator.get_random_antenna()
        self.assertEqual(24, ant)
        expt = []
        self.assertListEqual(self.antenna_genetator._antennas, expt)

    def test_probability(self):
        self.antenna_genetator = SuccesiveAntennaGenerator(5, Random(678))
        ant, prob = self.antenna_genetator.get_random_antenna()
        self.assertAlmostEqual(prob, 26**-1)
        self.assertEqual(ant, 2)

        _, prob = self.antenna_genetator.get_random_antenna()
        self.assertAlmostEqual(prob, 21**-1)

class TestImportanceSampling(TestCase):

    def test_SuccesiveAntennaGenerator(self):
        random = Random(666)

        est = estimate_number_of_activated_antenna(150, 2, random, SuccesiveAntennaGenerator)
        real = (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7
        print(real)
        print(est)
        assert abs(est - real) > 0.1

    def test_BadAntennaGenerator(self):
        random = Random(666)

        est = estimate_number_of_activated_antenna(2500, 2, random, BadAntennaGenerator)
        real = (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7
        assert abs(est - real) > 0.1

    def test_BetterSuccesiveAntennaGenerator(self):
        random = Random(666)

        est = estimate_number_of_activated_antenna(150, 2, random, BetterSuccesiveAntennaGenerator)
        real = (0 + 1 + 1 + 1 + 1 + 2 + 2) / 7
        print(real)
        print(est)
        assert abs(est - real) > 0.1


class TestBadAntennaGenerator(TestCase):
    def test_remove_antenna_easy(self):
        gen = BadAntennaGenerator(3, Random(666))
        gen._remove_antenna(2)
        expt = [0,3,4,6,7,8]
        self.assertListEqual(gen._antennas, expt)

        gen = BadAntennaGenerator(3, Random(666))
        gen._remove_antenna(3)
        expt = [1, 2, 5, 7, 8]
        self.assertListEqual(gen._antennas, expt)

        gen = BadAntennaGenerator(3, Random(666))
        gen._remove_antenna(4)
        expt = [0,2,6,8]
        self.assertListEqual(gen._antennas, expt)

        gen = BadAntennaGenerator(3, Random(666))
        gen._remove_antenna(7)
        expt = [0,1,2,3,5]
        self.assertListEqual(gen._antennas, expt)

    def test_remove_antenna(self):
        gen = BadAntennaGenerator(3, Random(666))
        gen._remove_antenna(gen._antennas.index(2))
        expt = [0,3,4,6,7,8]
        self.assertListEqual(gen._antennas, expt)

        gen._remove_antenna(gen._antennas.index(0))
        expt = [4,6,7,8]
        self.assertListEqual(gen._antennas, expt)

        gen._remove_antenna(gen._antennas.index(7))
        expt = []
        self.assertListEqual(gen._antennas, expt)
