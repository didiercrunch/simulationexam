from network.network import is_valid_network, get_number_of_activated_antenna

def _get_all_possible_network(box_size):
    '''returns all networks, broken or not'''
    return range( 2**(box_size*box_size) )


def get_all_possible_network(box_size):
    if box_size < 1:
        return
    for network in _get_all_possible_network(box_size):
        if is_valid_network(network, box_size):
            yield network


def _get_random_networks(n, box_size, random):
    all_networks = list(get_all_possible_network(box_size))
    n = min(n, len(all_networks))
    return random.sample(all_networks, n), n


def estimate_number_of_activated_antenna(n, box_size, random):
    networks, n = _get_random_networks(n, box_size, random)
    estimate = 0
    for network in networks:
        estimate += get_number_of_activated_antenna(network)
    return estimate / n
