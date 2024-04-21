

class Allocation:
    def build_tuple(items, arr2):
        k = len(items)
        result = []
        for i in range(0, k):
            result.append([items[i], arr2[i]])
        return result

    def greedy_no_frequency(network, list_of_items):
        cost = 0
        m = len(list_of_items)
        for i in range(0, m):
            item = list_of_items[i]
            distance = network.find_place_greedy(item)
            cost += distance
        return cost

    def greedy(network, list_of_items, rep):
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            item = sorted_arr[i][0]
            distance = network.find_place_greedy(item)
            cost += sorted_arr[i][1] * distance
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
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            print("Item number ", i, " is being allocated.")
            item = sorted_arr[i][0]
            distance = network.find_place_arash_tree_fractional(item)
            cost += sorted_arr[i][1] * distance
        return cost

    # proportional-fractional - Arash Alg
    def arash_prop_Tree_algorithm(network, list_of_items, rep):
        cost = 0
        sigma = Allocation.build_tuple(list_of_items, rep)
        sorted_arr = sorted(sigma, key=lambda x: x[1], reverse=True)
        m = len(rep)
        for i in range(0, m):
            # print("Item number ", i, " is being allocated.")
            item = sorted_arr[i][0]
            distance = network.find_place_proportional_arash_tree_fractional(item)
            cost += sorted_arr[i][1] * distance
        return cost

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
