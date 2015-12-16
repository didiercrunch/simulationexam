from network.network import (get_number_of_activated_antenna,
                             is_valid_network)


def _get_random_networks(box_size, random):
    '''yields random networks, broken or not'''
    number_of_square = box_size * box_size
    while True:
        yield random.randint(0, 2 ** number_of_square - 1)


def get_random_networks(box_size, random):
    for network in _get_random_networks(box_size, random):
        if is_valid_network(network, box_size):
            yield network


def estimate_number_of_activated_antenna(n, box_size, random):
    estimate = 0
    for _, network in zip(range(n), get_random_networks(box_size, random)):
        estimate += get_number_of_activated_antenna(network)
    return estimate / n
