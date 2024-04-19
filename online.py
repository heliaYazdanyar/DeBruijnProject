import random
import math
from Network import Network


class OnlineAdjustment:

    def Arash_fractional_access(network, item):
        # making a copy in case it failed
        network_copy = network.copy()

        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 0

        # item is already in src
        if root.contains_item(item):
            print("Item in src")
            return cost

        # item not in src
        host, initial_level = network.find_item_host_arashALG(item)
        if host is None:
            print("ERROR = Item has not been allocated")
            return network.num_nodes

        host.remove_item(item)

        # root adds the item
        root.add_item(item)
        curr_node = root

        cost = 0
        level = 1

        while True:
            if level == initial_level:
                break
            level += 1
            cost += OnlineAdjustment.push_down_one_level_fractional(network, curr_node, 1)
            print("Pushdown")
            if cost >= math.inf:
                print("Pushdown failed. Trying again...")
                OnlineAdjustment.Arash_fractional_access(network_copy, item)

        return cost

    def push_down_one_level_fractional(network, node, counter):
        if counter > 2 * node.capacity:
            return math.inf
        index = random.randint(0, len(node.items) - 1)
        item = node.items[index]

        curr_node = node

        root, next_node = network.item_next_path_arashALG(item, curr_node)

        if not next_node.fraction_is_full(root.index):
            next_node.add_item(item)
            return counter
        else:
            counter += 1
            return OnlineAdjustment.push_down_one_level_fractional(network, node, counter)

    # TODO ?
    def push_up_one_level_fraction(network, node, counter):
        return

    def push_up(self, initial_node, current_dst):

        return

    def access(network, item):
        item_binary = item.binary_repr
        root = network._find_root_node(item_binary)
        cost = 0

        # item is already in src
        if root.contains_item(item):
            return cost

        # remove item from its current place
        host = network.find_item_host(item)
        if host is None:
            print("item in main sycle")
            return network.num_nodes

        host.remove_item(item)

        if root.is_full():
            cnt = 0
            while True:
                cnt += 1
                cost += OnlineAdjustment.push_down_random_item(network, root)
                print("used pushdown")
                if cost != -1:
                    root.add_item(item)
                    return cost

                if cnt > -1.61/math.log10(1-1/root.capacity):  # 80% chance for each
                    print("stuck in while-", "cap=", root.capacity, "limit = ", -1.61/math.log10(1-1/root.capacity))
                    return network.num_nodes

        # add item to src
        root.add_item(item)
        return cost

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

    def push_down_random_item(network, node):
        index = random.randint(0, len(node.items)-1)
        item = node.items[index]
        return OnlineAdjustment.push_down(network, item, node)

    def push_down(network, item, node):
        cnt = 0
        item_binary = item.binary_repr
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

            if not curr_node.is_full():
                curr_node.add_item(item)
                return cnt

            # if in cycle
            if index == 0:
                return -1
            index = (index + 1) % len(item_binary)

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

