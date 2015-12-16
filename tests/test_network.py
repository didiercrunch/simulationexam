from unittest import TestCase
from network.network import (get_activated_antennas,
                             create_network,
                             pp_network,
                             _are_two_consicutive_horizontaly_antennas_activated,
                             _are_two_consicutive_verticaly_antennas_activated,
                             turn_on_antenna,
                             turn_off_antenna,
                             can_antenna_be_turned_on,
                             has_antenna)


class TestFunctions(TestCase):
    def test_create_network(self):
        assert create_network([]) == 0
        assert create_network([0,2,3,7,8,9]) == 909

    def test_pp_network(self):
        a = 111
        expt = """\
■-■-■-■
□-■-■-□
□-□-□-□
□-□-□-□
"""
        self.assertEqual( pp_network(a, 4), expt)


    def test_get_activated_antennas(self):
        self.assertListEqual(list(get_activated_antennas(0)), [])
        self.assertListEqual(list(get_activated_antennas(1)), [0])
        self.assertListEqual(list(get_activated_antennas(2)), [1])
        self.assertListEqual(list(get_activated_antennas(2)), [1])

        # 909 is written as 1110001101 in binary
        expt = [0,2,3,7,8,9]
        self.assertListEqual(list(get_activated_antennas(909)), expt)

    def test_are_two_consicutive_horizontaly_antennas_activated(self):
        assert _are_two_consicutive_horizontaly_antennas_activated(160, 4) == False
        assert _are_two_consicutive_horizontaly_antennas_activated(24, 4) == False
        assert _are_two_consicutive_horizontaly_antennas_activated(96, 4) == True

    def test_are_two_consicutive_verticaly_antennas_activated(self):
        assert _are_two_consicutive_verticaly_antennas_activated(24, 4) == False
        assert _are_two_consicutive_verticaly_antennas_activated(16384, 4) == False
        assert _are_two_consicutive_verticaly_antennas_activated(17408, 4) == True
        assert _are_two_consicutive_verticaly_antennas_activated(136, 4) == True
        assert _are_two_consicutive_verticaly_antennas_activated(1104, 4) == True

    def test_turn_on_antenna(self):
        self.assertEqual(turn_on_antenna(5, 111), 111)
        self.assertEqual(turn_on_antenna(4, 111), 111+2**4)

    def test_has_antenna(self):
        network = create_network([0,2,3,7,8,9])
        assert has_antenna(0, network)
        assert has_antenna(3, network)
        assert has_antenna(9, network)

        assert not has_antenna(4, network)
        assert not has_antenna(10, network)

    def test_turn_off_antenna(self):
        network = create_network([0,2,3,7,8,9])
        assert turn_off_antenna(2, network) == 905
        assert turn_off_antenna(7, network) == 781
        assert turn_off_antenna(10, network) == 909
        assert turn_off_antenna(4, network) == 909


    def test_can_antenna_be_turned_on(self):
        # □-□-□-□-■
        # □-□-□-□-□
        # □-□-■-□-□
        # □-□-□-□-■
        # □-□-□-□-□

        network = create_network([4, 12, 20])
        assert can_antenna_be_turned_on(0, network, 5)
        assert can_antenna_be_turned_on(1, network, 5)
        assert can_antenna_be_turned_on(5, network, 5)
        assert can_antenna_be_turned_on(19, network, 5)

        assert not can_antenna_be_turned_on(3, network, 5)
        assert not can_antenna_be_turned_on(7, network, 5)
        assert not can_antenna_be_turned_on(11, network, 5)
        assert not can_antenna_be_turned_on(13, network, 5)
        assert not can_antenna_be_turned_on(17, network, 5)
