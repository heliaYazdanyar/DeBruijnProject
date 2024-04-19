import random
from Network import Network
from static import Allocation
from online import OnlineAdjustment
from Items import ItemBuilder
from WBL import WBL_Network


def run_setup(log_numNodes, num_items, global_routing, additive_flag, factor):
    print("servers:", 2 ** log_numNodes)
    # num_items = (2**SeedNetSize)*8
    print("items:", num_items)
    additional_cap = 2
    # node_cap = int(num_items / (2 ** lon_numNodes)) + additional_cap
    if additive_flag:
        node_cap = int(int(num_items / (2 ** log_numNodes)) + factor)
    else:  # multiplicative
        node_cap = int(int(num_items / (2 ** log_numNodes)) * factor)

    print("cap:", node_cap)

    # We set binary repr of items length = nlog(n) in order for it to be big enough
    # long binary repr
    max_binary_id_length = node_cap + int(log_numNodes * (2 ** log_numNodes))

    # short length binary repr
    # max_binary_id_length = node_cap + int(log_numNodes)

    list_of_items = ItemBuilder.item_list_generation(num_items, max_binary_id_length)

    net = Network(log_numNodes, node_cap, global_routing)
    wbl_network = WBL_Network(log_numNodes, node_cap)
    return net, wbl_network, list_of_items


# static setup items in the network.
logn = 8
num_items = (2 ** logn) * 8
additive = True
factor = 5
network, wbl_net, list_items = run_setup(logn, num_items, global_routing=False, additive_flag=additive,
                                                 factor=factor)
frequencies = ItemBuilder.list_of_repetitions(num_items)


# allocate items in WBL

cost = Allocation.WBL_static_allocation(wbl_net, list_items, frequencies)
print("WBL static allocation cost is = ", cost)

# allocate items in DeBruijn

# greedy
# cost = Allocation.greedy(network, list_items, frequencies)
# print("Allocated with Static greedy allocation cost = ", cost)

# Arash's fractional
cost = Allocation.arash_Tree_algorithm(network, list_items, frequencies)
print("DeBruijn (Arash) Fractional Static allocation cost = ", cost)

# fractional
# network.allocation_fractional_space(frequencies)
# cost =Allocation.fractional_allocation(network, list_items, frequencies)
# print("DeBruijn Fractional Static allocation cost = ", cost)


# use online input to adjust
# num_requests = 1000
# access_list = []
# arr = []
# sum = 0
# for i in range(0, num_requests):
#     item_index = random.randint(0, len(list_items)-1)
#
#     # normal
#     cost = OnlineAdjustment.access(network, list_items[item_index])
#     # fractional
#     # cost = OnlineAdjustment.fractional_access(network, list_items[item_index])
#     sum += cost
#
#     arr.append(cost)
#     access_list.append(list_items[item_index].binary_repr)
#     print("Item: ", list_items[item_index].binary_repr, "cost: ", cost)
#
#
# print(sum)


# check process of static every step and algorithms
# set up adjustments for online
# write down algorithm using
# run on examples
