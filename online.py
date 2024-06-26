import random
import math


class OnlineAdjustment:
    # global access
    def global_access(network, item):
        root = network._find_root_node(item.binary_repr)
        if root.contains_item(item):
            return 1

        for i in range(0, network.num_nodes):
            if network.global_all_items[i].contains(item):
                path = network.shortest_path(root, network.nodes[i])
                root.add_item(item)
                return OnlineAdjustment.global_one_level_push_down(network, 1, path, 0)
        return network.num_nodes

    def global_one_level_push_down(network, counter, path, node_index):
        if node_index > len(path):
            print("ERROR- Wrong path in global routing!")
            return None
        node = path[node_index]
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]
        next_node = path[node_index + 1]

        if not next_node.is_full():
            node.remove_item(network, item)
            next_node.add_item(item)
            return counter
        else:
            counter += 1
            node_index += 1
            return OnlineAdjustment.global_one_level_push_down(network, counter, path, node_index)

    def global_static_access(network, item):
        root = network._find_root_node(item.binary_repr)
        for i in range(0, network.num_nodes):
            if item in network.global_all_items[i]:
                path = network.shortest_path(root, network.nodes[i])
                return len(path)
        return network.num_nodes

    # WBL
    def wbl_access(wbl_net, item):
        return wbl_net.access(item)

    # Static greedy access
    def static_normal_access(network, item):
        return network.static_access(item)

    # normal online access
    def normal_access(network, item):
        # making a copy in case it failed
        network_copy = network.copy()

        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 1

        # item is already in src
        if root.contains_item(item):
            return cost

        # item not in src
        host, initial_level = network.find_item_host(item)
        if host is None:
            print("ERROR = Item has not been allocated")
            return network.num_nodes

        host.remove_item(item)

        # root adds the item
        root.add_item(item)
        curr_node = root

        cost = 1
        level = 1

        while True:
            if level == initial_level:
                break
            level += 1
            cost += OnlineAdjustment.push_down_one_level(network, curr_node, 1)
            if cost >= math.inf:
                print("Pushdown failed. Trying again...")
                OnlineAdjustment.normal_access(network_copy, item)

        return cost

    def push_down_one_level_normal(network, node, counter):
        if counter > 2 * node.capacity:
            return math.inf
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]

        curr_node = node

        next_node = network.item_next_path_normal(item, curr_node)

        if not next_node.is_full():
            next_node.add_item(item)
            return counter
        else:
            counter += 1
            return OnlineAdjustment.push_down_one_level(network, next_node, counter)

    # Arash online Algorithm
    def Arash_fractional_access(network, item):
        # making a copy in case it failed
        network_copy = network.copy()

        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 1

        # item is already in src
        if root.contains_item(item):
            return cost

        # item not in src
        host, initial_level = network.find_item_host_arashALG(item)
        if host is None:
            print("ERROR = Item has not been allocated")
            return network.num_nodes

        host.remove_item_fractional(network, item.binary_repr)

        # root adds the item
        root.add_item(item)
        curr_node = root

        cost = 1
        level = 1

        while True:
            if level == initial_level:
                break
            level += 1
            cost += OnlineAdjustment.push_down_one_level_fractional(network, curr_node, 1)
            if cost >= math.inf:
                print("Pushdown failed. Trying again...")
                OnlineAdjustment.Arash_fractional_access(network_copy, item)

        return cost

    def push_down_one_level_fractional(network, node, counter):
        if counter > 2 * network.num_nodes:
            print("Strange ERROR")
            return math.inf
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]

        curr_node = node

        root, next_node = network.item_next_path_arashALG(item, curr_node)

        if not next_node.fraction_is_full(root.index):
            node.remove_item_fractional(network, item)
            next_node.fractional_add_item(item)
            return counter
        else:
            counter += 1
            return OnlineAdjustment.push_down_one_level_fractional(network, next_node, counter)

    # CnA online Algorithm
    def CnA_access_static(network, item):
        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 1

        # item is already in src
        if root.contains_item(item):
            return cost

        # item not in src
        host, initial_level = network.find_item_host_arashALG(item)
        if host is None:
            print("ERROR = Item has not been allocated")
            return network.num_nodes

        return initial_level

    def CnA_access(network, item):
        # making a copy in case it failed
        network_copy = network.copy()

        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 1

        # item is already in src
        if root.contains_item(item):
            return cost

        # item not in src
        host, initial_level = network.find_item_host_arashALG(item)
        if host is None:
            print("ERROR = Item has not been allocated")
            return network.num_nodes

        host.CnA_remove_item(network, item)

        # root adds the item
        root.add_item(item)
        curr_node = root

        level = 1

        while True:
            if level == initial_level:
                break
            level += 1
            cost += OnlineAdjustment.CnA_push_down_one_level(network, curr_node, 1)
            if cost >= math.inf:
                print("Pushdown failed. Trying again...")
                OnlineAdjustment.CnA_access(network_copy, item)

        return cost

    def CnA_push_down_one_level(network, node, counter):
        if counter > 2 * node.capacity:
            return math.inf
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]

        curr_node = node
        root, next_node = network.item_next_path_arashALG(item, curr_node)

        if not next_node.CnA_fraction_is_full(root.index):
            curr_node.CnA_remove_item(network, item)
            next_node.CnA_fractional_add_item(network, item)
            return counter
        else:
            counter += 1
            return OnlineAdjustment.CnA_push_down_one_level(network, next_node, counter)

    # TODO ?
    def push_up_one_level_fraction(network, node, counter):
        return

    def push_up(self, initial_node, current_dst):
        return

    def fractional_access(network, item):
        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 0

        # item is already in src
        if root.contains_item(item):
            return cost

        # remove item from its current place
        host = network.find_item_host(item)
        if host is None:
            print("item in main cycle")
            return network.num_nodes

        host.remove_item(item)

        if root.is_full():
            cnt = 0
            while True:
                cnt += 1
                cost += OnlineAdjustment.random_fractional(network, root)
                print("used pushdown")
                if cost != -1:
                    root.add_item(item)
                    return cost

                if cnt > -1.61 / math.log10(1 - 1 / root.capacity):  # 80% chance for each
                    print("stuck in while-", "cap=", root.capacity, "limit = ",
                          -1.61 / math.log10(1 - 1 / root.capacity))
                    return network.num_nodes

        # add item to src
        root.add_item(item)
        return cost

    def random_fractional(network, node):
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]
        return OnlineAdjustment.fractional_pushdown(network, item, node)

    def fractional_pushdown(network, item, node):
        cnt = 0
        item_binary = item.binary_repr
        root = node
        curr_node = node
        index = 1
        while True:
            # next node
            s = (network.binary_len + index) % len(item_binary)
            if item_binary[s] == 0:
                curr_node = curr_node.left
                cnt += 1
            else:
                curr_node = curr_node.right
                cnt += 1

            if not curr_node.fraction_is_full(root.index):
                curr_node.add_item(item)
                return cnt

            # if in cycle
            if index == 0:
                return -1
            index = (index + 1) % len(item_binary)

    def find_path_to_source(network, item):
        item_binary = item.binary_repr
        path = []
        root = network._find_root_node(item)
        path.append(root)
        if root.contains_item(item):
            return path

        index = 1
        curr_node = root
        while True:

            if curr_node.contains_item(item):
                return path
            else:
                s = (network.binary_len + index) % len(item_binary)
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
                path.append(curr_node)

            # if in cycle
            if index == 0:
                print("item is in cycle-- fix later")

            index = (index + 1) % len(item_binary)
        return

    def move_to_src(network, item):
        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)

        # item is already in src
        if root.contains_item(item):
            return

        if root.is_full():
            cnt = 0
            while True:
                cnt += 1
                flag = OnlineAdjustment.push_down_random_item(network, root)
                if flag:
                    root.add_item(item)
                    break
                if cnt > -1.61/math.log10(1-1/root.capacity):  # 80% chance for each
                    print("stuck in while-", "cap=", root.capacity, "limit = ", -1.61/math.log10(1-1/root.capacity))
                    break
        return

    # def push_down_random_item(network, node):
    #     index = random.randint(0, len(node.items)-1)
    #     item = node.items[index]
    #     return OnlineAdjustment.push_down(network, item, node)
    #
    # def push_down(network, item, node):
    #     cnt = 0
    #     item_binary = item.binary_repr
    #     curr_node = node
    #     index = 1
    #     while True:
    #         # next node
    #         s = (network.binary_len + index) % len(item_binary)
    #         if item_binary[s] == 0:
    #             curr_node = curr_node.left
    #             cnt += 1
    #         else:
    #             curr_node = curr_node.right
    #             cnt += 1
    #
    #         if not curr_node.is_full():
    #             curr_node.add_item(item)
    #             return cnt
    #
    #         # if in cycle
    #         if index == 0:
    #             return -1
    #         index = (index + 1) % len(item_binary)



##

