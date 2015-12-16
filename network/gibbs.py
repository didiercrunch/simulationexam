from network.network import (get_number_of_activated_antenna,
                             can_antenna_be_turned_on,
                             turn_off_antenna,
                             turn_on_antenna)

def _flip_coin(random):
    return random.random() < 0.5

def create_new_network(network, box_size, random):
    number_of_square = box_size * box_size
    for antenna in range(number_of_square):
        if can_antenna_be_turned_on(antenna, network, box_size) and _flip_coin(random):
            network = turn_on_antenna(antenna, network)
        else:
            network = turn_off_antenna(antenna, network)
    return network


def get_pseudo_random_networks(box_size, random):
    network = 0
    while True:
        network = create_new_network(network, box_size, random)
        yield network

def get_random_networks(box_size, random):
    time_between_sample = 20
    for i, network in enumerate(get_pseudo_random_networks(box_size, random), 1):
        if i % time_between_sample == 0:
            yield network


def estimate_number_of_activated_antenna(n, box_size, random):
    estimate = 0
    for _, network in zip(range(n), get_random_networks(box_size, random)):
        estimate += get_number_of_activated_antenna(network)
    return estimate / n
