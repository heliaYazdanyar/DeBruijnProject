import random
import numpy as np


class ItemBuilder:
    def _generate_random_binary_id(length):
        return "".join(str(random.randint(0, 1)) for _ in range(length))

    def item_list_generation(num_items, max_binary_id_length):
        list_of_items = []
        for i in range(1, num_items + 1):
            binary_id = ItemBuilder._generate_random_binary_id(max_binary_id_length)
            time_stamp = 0
            item = Item(binary_id, time_stamp)
            list_of_items.append(item)
        return list_of_items

    # frequencies
    def frequencies_zipf(alpha, num_items, numRequest):
        s = np.random.zipf(alpha, num_items)
        result = (s / sum(s)) * numRequest
        y = result.astype(int)
        return y

    def frequencies_uniform(seed, num_items):
        np.random.seed(seed)
        limit = 1000
        list_rep = np.rint(np.random.uniform(1, limit, size=num_items, ))
        return list_rep

    # in this function there are multiple random functions to
    # produce frequencies
    def list_of_repetitions(num_items):
        np.random.seed()
        # ## normal distribution
        # list_rep = np.rint(np.random.normal(10, 3.5, size=num_items)) ## add time seed
        ## (exponential +1)*4
        # list_rep = np.rint((np.random.standard_exponential(num_items)+1)*4)
        ## couchy
        s = np.rint(np.random.standard_cauchy(num_items))
        s = np.where(s < 0, s * -1, s)
        list_rep = np.where(s == 0, s + 1, s)
        ## Wald
        # list_rep = np.rint(np.random.wald(10, 4, num_items))
        # ## uniform
        # list_rep = np.rint(np.random.uniform(10,20,num_items))
        # ## rand int
        # list_rep = np.random.randint(20, size=num_items)
        return list_rep


class Item:
    time_stamp = ""
    binary_repr = ""
    curr_frequency = 0

    # location in Network

    def __init__(self, binary_repr, time_stamp):
        self.binary_repr = binary_repr
        self.time_stamp = time_stamp

