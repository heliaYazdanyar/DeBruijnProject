import math


class Allocation:

    def build_tuple(items, arr2):
        k = len(items)
        result = []
        for i in range(0, k):
            result.append([items[i], arr2[i]])
        return result

    # Greedy Algorithms
    def Chen_greedy(network, list_of_items, rep):
        """In this algorithm we scan the sorted input array, and allocate any item that can be allocated in its source.
         After the first scan is finished, we will scan the remaining sorted array again and
          allocate the remaining items in the first available space in their corresponding routing servers."""
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)  # should we sort or not?
        m = len(rep)
        remaining_items = []
        remaining_rep = []

        # first level allocation
        for i in range(0, m):
            item = sorted_arr[i][0]
            check = network.simple_greedy_first_step(item.binary_repr)
            if check == 1:
                cost += sorted_arr[i][1]
            else:
                remaining_items.append(sorted_arr[i][0])
                remaining_rep.append(sorted_arr[i][1])

        # second level allocation
        m2 = len(remaining_rep)
        for i in range(0, m2):
            item = remaining_items[i]
            distance = network.find_place_greedy(item)
            cost += remaining_rep[i] * distance

        return cost

    def greedy_free_for_all(network, list_of_items, rep):
        """In this algorithm we scan the sorted input and allocate items
        to the first space found in their corresponding routing."""
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            item = sorted_arr[i][0]
            distance = network.find_place_greedy(item)
            cost += sorted_arr[i][1] * distance
        return cost

    def greedy_no_frequency(network, list_of_items):
        cost = 0
        m = len(list_of_items)
        for i in range(0, m):
            item = list_of_items[i]
            distance = network.find_place_greedy(item)
            cost += distance
        return cost

    def levels_greedy(network, list_of_items, rep):
        """This algorithm consists of multiple levels. In level  i,
        we scan the sorted array and allocate each item that can be allocated in a server with distance  i
        from its source and remove this item from the array."""

        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)  # should we sort or not?

        input = []
        frequencies = []
        m = len(rep)
        for i in range(0, m):
            input.append(sorted_arr[i][0])
            frequencies.append(sorted_arr[i][1])

        logn = int(math.log2(network.num_nodes))
        for level in range(0, logn):
            if len(input) == 0:
                break

            remaining_items = []
            remaining_rep = []
            # this level allocation
            for i in range(0, m):
                item = input[i]
                # check if you can allocate
                check, node = network.level_greedy_ckeck(level, item.binary_repr)
                if check == level:
                    node.add_item(item)
                    cost += frequencies[i] * level
                else:
                    remaining_items.append(input[i])
                    remaining_rep.append(frequencies[i])
            # arrange remaining array
            m = len(remaining_rep)
            input = remaining_items.copy()
            frequencies = remaining_rep.copy()

        # level (n) - main cycle
        m = len(input)
        for i in range(0, m):
            item = input[i]
            distance = network.find_place_greedy(item)
            cost += frequencies[i] * distance

        return cost

    def fractional_allocation(network, list_of_items, rep):
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            item = sorted_arr[i][0]
            distance = network.find_place_fractional(item)
            cost += sorted_arr[i][1] * distance
        return cost

    # fractional- repeating trees
    def arash_Tree_algorithm(network, list_of_items, rep):
        # input
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)

        errors = 0
        for i in range(0, m):
            # print("Item number ", i, " is being allocated.")
            item = sorted_arr[i][0]
            distance, flag_error = network.find_place_arash_tree_fractional(item)
            cost += sorted_arr[i][1] * distance
            errors += flag_error
        return cost , errors

    # proportional-fractional - Arash Alg
    def arash_prop_Tree_algorithm(network, list_of_items, rep):
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        errors = 0
        for i in range(0, m):
            # print("Item number ", i, " is being allocated.")
            item = sorted_arr[i][0]
            distance, errors_flag = network.find_place_proportional_arash_tree_fractional(item)
            cost += sorted_arr[i][1] * distance
            errors += errors_flag
        return cost, errors

    def WBL_static_allocation(wbl_network, list_of_items, rep):
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            item = sorted_arr[i][0]
            distance = wbl_network.find_place_greedy(item)
            cost += sorted_arr[i][1] * distance
        return cost
