from collections import deque


def _get_print_symbol(network, position):
    black_square = '\u25A0'
    white_square = '\u25A1'
    activated_antennas = set(get_activated_antennas(network))
    if position in activated_antennas:
        return black_square
    return white_square


def pp_network(network, box_size):
    ret = ""
    for line in range(box_size):
        for column in range(box_size):
            symbol =  _get_print_symbol(network, line * box_size + column)
            ret += symbol + '-'
        ret = ret[:-1] + '\n'
    return ret


def get_activated_antennas(network):
    i = 0
    while network > 0:
        if network % 2:
            yield i
        network = network >> 1
        i += 1


def create_network(activated_antennas):
    return sum(2**activated_antenna for activated_antenna in activated_antennas)


def _are_two_consicutive_horizontaly_antennas_activated(network, box_size):
    predecessor = -2
    for antenna in get_activated_antennas(network):
        if antenna == predecessor + 1:
            return True
        if (antenna + 1) % box_size:
            predecessor = antenna
    return False


def _are_two_consicutive_verticaly_antennas_activated(network, box_size):
    invalid_entennas = set()
    for antenna in get_activated_antennas(network):
        if antenna in invalid_entennas:
            return True
        invalid_entennas.add(antenna + box_size)

    return False


def is_valid_network(network, box_size):
    if _are_two_consicutive_horizontaly_antennas_activated(network, box_size):
        return False

    if _are_two_consicutive_verticaly_antennas_activated(network, box_size):
        return False
    return True


def has_antenna(antenna, network):
    return (network >> antenna) % 2


def turn_on_antenna(antenna, network): # error with borders
    if has_antenna(antenna, network):
        return network
    return network + 2**antenna


def turn_off_antenna(antenna, network):
    if has_antenna(antenna, network):
        return network - 2**antenna
    return network


def can_antenna_be_turned_on(antenna, network, box_size):
    for ant in get_activated_antennas(network):
        if ant == antenna + 1 and ant % box_size:
            return False
        if ant == antenna - 1 and antenna % box_size:
            return False
        if ant == antenna + box_size:
            return False
        if ant == antenna - box_size:
            return False
        if ant > antenna + box_size:
            return True
    return True


def get_number_of_activated_antenna(network):
    return len(list(get_activated_antennas(network)))
