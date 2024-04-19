import random
from Network import Network
from static import Allocation
from online import OnlineAdjustment
from Items import ItemBuilder
from WBL import WBL_Network


# ---------- setting up tests:
# input-----------
# log_numNodes = log (n)
# num_items = n
# boolean global_routing - if not : local_routing
# boolean additive_flag -  if not multiplicative
# factor : additive or multiplicative factor
# boolean long_binary_item : if binary repr of items are long or not (for Arash's Algorithm)
# output ------------
# 1- DeBruijn Network
# 2- WBL Network
# 3- list of items

def run_setup(log_numNodes, num_items, global_routing, additive_flag, factor, long_binary_item=True):
    print("servers:", 2 ** log_numNodes)
    print("items:", num_items)

    # setting up node capacity (additive or multiplicative)
    if additive_flag:
        node_cap = int(int(num_items / (2 ** log_numNodes)) + factor)
    else:  # multiplicative
        node_cap = int(int(num_items / (2 ** log_numNodes)) * factor)

    print("cap:", node_cap)

    if long_binary_item:  # We set binary repr of items length = nlog(n) in order for it to be big enough long binary
        # repr
        max_binary_id_length = node_cap + int(log_numNodes * (2 ** log_numNodes))
    else:  # short length binary repr
        max_binary_id_length = node_cap + int(log_numNodes)

    # create items
    list_of_items = ItemBuilder.item_list_generation(num_items, max_binary_id_length)

    # create DeBruijn Network
    net = Network(log_numNodes, node_cap, global_routing)
    # create WBL Network
    wbl_network = WBL_Network(log_numNodes, node_cap)

    return net, wbl_network, list_of_items


def static_allocation_DeBruijn(method, net, items, frequency_of_items):
    if method == "greedy":
        cost = Allocation.greedy(net, items, frequency_of_items)
        print("Allocated with Static greedy allocation cost = ", cost)
    elif method == "Arash":
        cost = Allocation.arash_Tree_algorithm(net, items, frequency_of_items)
        print("DeBruijn (Arash) Fractional Static allocation cost = ", cost)
    elif method == "Fractional":
        cost =Allocation.fractional_allocation(net, items, frequency_of_items)
        print("DeBruijn Fractional Static allocation cost = ", cost)
    else:
        cost = 0

    return cost


def test_online(method, net, item):
    if method == "normal":
        cost = OnlineAdjustment.access(net, item)
    elif method == "Arash":
        cost = OnlineAdjustment.Arash_fractional_access(net, item)
    elif method == "Fractional":
        cost = OnlineAdjustment.fractional_access(net, item)
    else:
        cost = 0

    return cost


# parameters of network and setup
logn = 6
num_items = (2 ** logn) * 8
additive = True
factor = 5
network, wbl_net, list_items = run_setup(logn, num_items, global_routing=False, additive_flag=additive,
                                         factor=factor)

# frequency of items for static allocation
frequencies = ItemBuilder.list_of_repetitions(num_items)

# static- allocate items in WBL
# cost_of_wbl = Allocation.WBL_static_allocation(wbl_net, list_items, frequencies)
# print("WBL static allocation cost is = ", cost_of_wbl)

# static- allocate items in DeBruijn
# ------ options for method = {"greedy, "Arash", "Fractional"}
cost_of_static = static_allocation_DeBruijn("Arash", network, list_items, frequencies)


# Testing  Online Adjustments

num_requests = 1000
access_list = []
arr = []
sum = 0

for i in range(0, num_requests):
    item_index = random.randint(0, len(list_items) - 1)

    # online- allocate items in DeBruijn
    # ------ options for method = {"normal, "Arash", "Fractional"}
    adj_cost = test_online("Arash", network, list_items[item_index])

    sum += adj_cost
    arr.append(adj_cost)
    access_list.append(list_items[item_index].binary_repr)
    # print("Item: ", list_items[item_index].binary_repr, "cost: ", adj_cost)

print("Total online cost for ", num_requests, " requests is ", sum)

