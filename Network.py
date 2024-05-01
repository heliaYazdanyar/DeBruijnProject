import random
import hashlib
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
from queue import Queue
import math
import time
from numpy.linalg import matrix_power
from Node import Node
from Items import ItemBuilder


# TODO
# 2- adjusting items in main cycle


class Network:

    def __init__(self, log_num_nodes, node_cap, global_routing):
        self.binary_len = log_num_nodes
        self.num_nodes = 2 ** log_num_nodes
        self.global_routing = global_routing
        self.node_cap = node_cap
        self.proportions = []
        self.server_distances = []

        # nodes
        self.nodes = [Node(f"{i:0{log_num_nodes}b}", index=i) for i in range(self.num_nodes)]
        for node in self.nodes:
            _left_neighbor_repr = node.binary_repr[1:] + "0"
            _right_neighbor_repr = node.binary_repr[1:] + "1"
            _left_neighbor = next(n for n in self.nodes if n.binary_repr == _left_neighbor_repr)
            _right_neighbor = next(n for n in self.nodes if n.binary_repr == _right_neighbor_repr)
            node.set_left(_left_neighbor)
            node.set_right(_right_neighbor)
            node.capacity = node_cap

        # other initializing
        self.all_dist()
        self.allocate_proportional_fractional_space()
        return

    # distance of nodes
    def all_dist(self):
        self.server_distances = np.zeros((self.num_nodes, self.num_nodes))
        i = -1
        for src in self.nodes:
            i += 1
            j = -1
            for dst in self.nodes:
                j += 1
                d = self.shortest_path_servers(src, dst)
                self.server_distances[i][j] = d
        return

    def shortest_path_servers(self, src_node, dst_node):
        flag, first_search = self.BFS_shortestPath(src_node, dst_node)
        if flag:
            return first_search
        else:
            return first_search + self.cycle_shortestPath(src_node, dst_node)

    def BFS_shortestPath(self, src_node, dst_node):
        if src_node.binary_repr == dst_node.binary_repr:
            return True, 1

        visited = set()
        queue = Queue()
        queue.put(src_node)
        visited.add(src_node)

        parent = dict()
        parent[src_node.index] = None

        flag = False
        while not queue.empty():
            current_node = queue.get()
            if current_node.binary_repr == dst_node.binary_repr:
                flag = True
                break

            for next_node in current_node.neighbors:
                if next_node not in visited:
                    queue.put(next_node)
                    parent[next_node.index] = current_node
                    visited.add(next_node)

        # Path reconstruction
        path = []
        if flag:
            path.append(dst_node)
            while parent[dst_node.index] is not None:
                path.append(parent[dst_node.index])
                dst_node = parent[dst_node.index]
            path.reverse()
        return flag, len(path)

    def cycle_shortestPath(self, src_node, dst_node):
        return abs(src_node.index - dst_node.index)

    def item_in_cycle(self, src_node, item):
        curr_index = src_node.index
        counter = 0
        for i in range(0, len(self.nodes)):
            # update index
            curr_index += 1
            counter += 1
            curr_index = curr_index % len(self.nodes)

            # place in node if possible
            if not self.nodes[curr_index].is_full():
                self.nodes[curr_index].add_item(item)
                return counter
        return -1

    # finding place to allocate items
    def _find_root_node(self, hashed_value):
        starting_hash = hashed_value[0:self.binary_len]
        for i in range(0, self.num_nodes):
            if self.nodes[i].binary_repr == starting_hash:
                return self.nodes[i]
        return -1

    def find_place_greedy(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if not root.is_full():
            root.add_item(item)
            return cnt
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        cnt += 1
        while True:
            # if local routing was full
            if index == 0:
                cycle_counter = self.item_in_cycle(root, item)
                if cycle_counter == -1:
                    print("no empty node left")
                    return 10000 + cnt
                else:
                    return cnt + cycle_counter

            # local routing
            if not curr_node.is_full():
                curr_node.add_item(item)
                return cnt

            else:  # this part uses binary representation to find path (left or right) !
                s = (self.binary_len + index) % len(item_binary)
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right

            index = (index + 1) % len(item_binary)
            cnt += 1

        return cnt

    def find_place_global_routing(self, item):
        return

    # finding items
    def find_item_host(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if root.contains_item(item):
            return root

        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index_i = 1
        cnt += 1
        while True:
            # if local routing was full --- second implementation TODO
            if index_i == 0:
                print("local routing full")
                return None

            # local routing
            if curr_node.contains_item(item):
                return curr_node

            else:  # this part uses binary representation to find path (left or right) !
                s = (self.binary_len + index_i) % len(item_binary)
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right

            index_i = (index_i + 1) % len(item_binary)
            cnt += 1
        return

    #  ---- fractional allocation

    # proportional

    def set_proportions(self, all_items):
        for i in range(0, len(all_items)):
            item = all_items[i]
            root = self._find_root_node(item.binary_repr)
            root.add_src_item(item.binary_repr)
        return

    def allocate_proportional_fractional_space(self):
        max_dist = int(math.log2(self.num_nodes))
        for d in range(0, max_dist):
            # M = matrix_power(self.server_distances, d)
            for i in range(0, self.num_nodes):
                curr_node = self.nodes[i]
                for j in range(0, self.num_nodes):
                    if self.server_distances[i][j] == d:
                        prop = self.nodes[j].get_proportion()
                        curr_node.allocate_prop_fractional(j, d, prop)
                # print("Allocated space for ", curr_node.index, " is ", curr_node.prop_fraction_space)

        # each nodes occupies the free space for its own items
        for i in range(0, self.num_nodes):
            self.nodes[i].pick_remaining_space(i)

        # scaling the proportions to capacity
        sum = 0
        for i in range(0, self.num_nodes):
            print(self.nodes[i].prop_fraction_space)
            sum += np.sum(self.nodes[i].prop_fraction_space)

        print(sum)
        cap = self.node_cap
        for i in range(0, self.num_nodes):
            node = self.nodes[i]
            for j in range(0, self.num_nodes):
                node.prop_fraction_space[j] = (node.prop_fraction_space[j] * cap / sum)

        return

    def find_place_proportional_arash_tree_fractional(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if not root.prop_fraction_is_full(root.index):
            root.prop_fractional_add_item(root.index, item)
            return cnt

        # routing
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        total_index = 1
        cnt += 1
        curr_root = root

        while True:
            if index == 0:  # going in the new Tree
                curr_root = curr_node

            if cnt > len(item_binary) - self.binary_len:
                print("no empty node in Tree cnt=", cnt)
                return self.num_nodes

            if not curr_node.prop_fraction_is_full(curr_root.index):
                curr_node.prop_fractional_add_item(curr_root.index, item)
                print("allocated lower than root")
                return cnt

            else:  # this part uses binary representation to find path (left or right) !!!
                s = (self.binary_len + total_index)
                cnt += 1
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
            total_index += 1
            index = (index + 1) % len(item_binary)
            cnt += 1
        return cnt

    # fractional functions
    def allocation_fractional_space(self):
        max_dist = int(math.log2(self.num_nodes))
        for d in range(0, max_dist):
            # M = matrix_power(self.server_distances, d)
            for i in range(0, self.num_nodes):
                curr_node = self.nodes[i]
                for j in range(0, self.num_nodes):
                    if self.server_distances[i][j] == d:
                        curr_node.allocate_space(j, d)
                # print("Allocated space for ", curr_node.index, " is ", curr_node.fraction_space)

        # each nodes occupies the free space for its own items
        for i in range(0, self.num_nodes):
            self.nodes[i].pick_remaining_space(i)
        return

    def find_place_fractional(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if not root.fraction_is_full(root.index):
            root.fractional_add_item(root.index, item)
            return cnt

        # routing
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        cnt += 1
        while True:
            # main cycle
            if index == 0:
                cycle_counter = self.item_in_cycle(root, item_binary)
                if cycle_counter == -1:
                    print("no empty node left")
                    return 10000 + cnt
                else:
                    return cnt + cycle_counter

            if not curr_node.fraction_is_full(root.index):
                curr_node.fractional_add_item(root.index, item)
                return cnt

            else:  # this part uses binary representation to find path (left or right) !!!
                s = (self.binary_len + index) % len(item_binary)
                cnt += 1
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
            index = (index + 1) % len(item_binary)
            cnt += 1
        return cnt

    # Algorithm
    # binary repr of the item is (nlog(n)) long
    # finds root and goes threw the tree
    # if tree ends, we set the last leaf as new root to continue searching for
    # empty place
    # TODO : Do we look in the spaces related to fractional of the new root or old root?

    def find_place_arash_tree_fractional(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if not root.fraction_is_full(root.index):
            root.fractional_add_item(root.index, item)
            return cnt

        # routing
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        total_index = 1
        cnt += 1
        curr_root = root

        while True:
            if index == 0:  # going in the new Tree
                curr_root = curr_node

            if cnt > len(item_binary) - self.binary_len:
                print("no empty node in Tree cnt=", cnt)
                return self.num_nodes

            if not curr_node.fraction_is_full(curr_root.index):
                curr_node.fractional_add_item(curr_root.index, item)
                print("allocated lower than root")
                return cnt

            else:  # this part uses binary representation to find path (left or right) !!!
                s = (self.binary_len + total_index)
                cnt += 1
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
            total_index += 1
            index = (index + 1) % len(item_binary)
            cnt += 1
        return cnt

    def item_next_path_arashALG(self, item, host):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if root == host:
            if item_binary[self.binary_len] == 0:
                return root, root.left
            else:
                return root, root.right

        # routing
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        total_index = 1
        cnt += 1
        curr_root = root

        while True:
            if index == 0:  # going in the new Tree
                curr_root = curr_node

            if cnt > len(item_binary) - self.binary_len:
                print("no empty node in Tree cnt=", cnt)
                return curr_root, None

            if curr_node == host:
                if item_binary[self.binary_len + total_index] == 0:
                    return curr_root, curr_node.left
                else:
                    return curr_root, curr_node.right

            else:  # this part uses binary representation to find path (left or right) !!!
                s = (self.binary_len + total_index)
                cnt += 1
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
            total_index += 1
            index = (index + 1) % len(item_binary)
            cnt += 1
        return None, None

    def find_item_host_arashALG(self, item):
        item_binary = item.binary_repr
        cnt = 1
        root = self._find_root_node(item_binary)

        if root.contains_item(item):
            return root, 1

        # routing
        if item_binary[self.binary_len] == 0:
            curr_node = root.left
        else:
            curr_node = root.right

        index = 1
        total_index = 1
        cnt += 1
        curr_root = root

        while True:
            if index == 0:  # going in the new Tree
                curr_root = curr_node

            if cnt > len(item_binary) - self.binary_len:
                return None, -1

            if curr_node.contains_item(item):
                return curr_node, cnt

            else:  # this part uses binary representation to find path (left or right) !!!
                s = (self.binary_len + total_index)
                cnt += 1
                if item_binary[s] == 0:
                    curr_node = curr_node.left
                else:
                    curr_node = curr_node.right
            total_index += 1
            index = (index + 1) % len(item_binary)
            cnt += 1
        return None, -1

    def copy(self):
        copy = Network(self.binary_len, self.node_cap, self.global_routing)
        for i in range(0, self.num_nodes):
            copy.nodes[i].items = self.nodes[i].items
        return copy
