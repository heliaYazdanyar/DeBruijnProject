import random
from Network import Network
from static import Allocation
from online import OnlineAdjustment
from Items import ItemBuilder
from WBL import WBL_Network


def run_setup(log_numNodes, num_items, global_routing, additive_flag, factor, long_binary_item=True):
    """setting up tests:"""
    'input-----------'
    'log_numNodes = log (n)'
    'num_items = n'
    'boolean global_routing - if not : local_routing'
    'boolean additive_flag -  if not multiplicative'
    ' factor : additive or multiplicative factor'
    'boolean long_binary_item : if binary repr of items are long or not (for Arash Algorithm)'
    'output ------------'
    '1- DeBruijn Network'
    '2- WBL Network'
    '3- node capacity '

    print("servers:", 2 ** log_numNodes)
    print("items:", num_items)

    # setting up node capacity (additive or multiplicative)
    if additive_flag:
        node_cap = int(int(num_items / (2 ** log_numNodes)) + factor)
    else:  # multiplicative
        node_cap = int(int(num_items / (2 ** log_numNodes)) * factor)

    print("cap:", node_cap)

    # create DeBruijn Network
    net = Network(log_numNodes, node_cap, global_routing)
    # create WBL Network
    wbl_network = WBL_Network(log_numNodes, node_cap)

    return net, wbl_network, node_cap


def static_allocation_DeBruijn(method, net, items, frequency_of_items):
    if method == "greedyFreeForAll":
        cost = Allocation.greedy_free_for_all(net, items, frequency_of_items)
        print("Allocated with Static greedy allocation cost = ", cost)
    elif method == "Chen":
        cost = Allocation.Chen_greedy(net, items, frequency_of_items)
        print("DeBruijn Chen's Static allocation cost = ", cost)
    elif method == "LevelByLevel":
        cost = Allocation.levels_greedy(net, items, frequency_of_items)
        print("DeBruijn Level By Level Static allocation cost = ", cost)
    elif method == "Arash":
        net.allocation_fractional_space()
        cost, errors = Allocation.arash_Tree_algorithm(net, items, frequency_of_items)
        print("DeBruijn (Arash) Fractional Static allocation cost = ", cost)
        print(" !! Number of Failed attempts = ", errors)
    elif method == "Prop-Arash":
        net.set_proportions(items)
        net.allocate_proportional_fractional_space()
        cost, errors = Allocation.arash_prop_Tree_algorithm(net, items, frequency_of_items)
        print("DeBruijn (Arash) Proportional - Fractional Static allocation cost = ", cost)
        print("!! Number of Failed attempts = ", errors)

    elif method == "Fractional":
        net.allocation_fractional_space()
        cost = Allocation.fractional_allocation(net, items, frequency_of_items)
        print("DeBruijn Fractional Static allocation cost = ", cost)
    else:
        cost = 0

    return cost


def single_test_online(method, net, item):
    if method == "normal":
        res = OnlineAdjustment.normal_access(net, item)
    elif method == "Arash":
        res = OnlineAdjustment.Arash_fractional_access(net, item)
    elif method == "Fractional":  # TODO: Needs Debugging
        res = OnlineAdjustment.fractional_access(net, item)
    else:
        res = 0
    return res


def run_online(method, number_of_requests, net, items):
    access_list = []
    arr = []
    cost_sum = 0

    for i in range(0, number_of_requests):
        item_index = random.randint(0, len(list_items) - 1)
        adj_cost = single_test_online(method, network, list_items[item_index])
        cost_sum += adj_cost
        arr.append(adj_cost)
        access_list.append(list_items[item_index].binary_repr)

    print("Total online cost for ", num_requests, " requests is ", cost_sum)
    return cost_sum


# TO DO - reading real data
def get_data(real, long_binary_item, node_cap, log_numNodes):
    if long_binary_item:  # We set binary repr of items length = nlog(n) in order for it to be big enough long binary
        # repr
        max_binary_id_length = node_cap + int(((2 ** log_numNodes) ** 2))
    else:  # short length binary repr
        max_binary_id_length = node_cap + int(log_numNodes)

    list_of_items = ItemBuilder.item_list_generation(num_items, max_binary_id_length)
    frequencies = ItemBuilder.list_of_repetitions(num_items)

    return list_of_items, frequencies


' parameters of network and setup '
logn = 6
num_items = (2 ** logn) * 10
additive = False
factor = 2
network, wbl_net, node_cap = run_setup(logn, num_items, global_routing=False, additive_flag=additive, factor=factor)

'frequency of items for static allocation'
list_items, frequencies = get_data(False, long_binary_item=True, node_cap=node_cap, log_numNodes=logn)

'static- allocate items in WBL'
# cost_of_wbl = Allocation.WBL_static_allocation(wbl_net, list_items, frequencies)
# print("WBL static allocation cost is = ", cost_of_wbl)

'static- allocate items in DeBruijn'
'------ options for method = {"greedyFreeForAll", "Chen", "LevelByLevel, "Arash", "Fractional", "Prop-Arash"}'

# string_method = "greedyFreeForAll"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()
#
# string_method = "Chen"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()
#
# string_method = "LevelByLevel"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()

string_method = "Arash"
cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()

# string_method = "Prop-Arash"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()

# string_method = "Fractional"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()

# Testing  Online Adjustments
num_requests = 100
# ------ options for method = {"normal, "Arash", "Fractional"}
cost_online = run_online("Arash", num_requests, network, list_items)

