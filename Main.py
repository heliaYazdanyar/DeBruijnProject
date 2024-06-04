import random
import time

from Network import Network
from static import Allocation
from online import OnlineAdjustment
from Items import ItemBuilder
from WBL import WBL_Network
import matplotlib.pyplot as plt


# set up tests
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


def temporal_data(p, all_items, prev_item):
    coin = random.random()
    if coin < p:
        return prev_item
    else:
        rand_index = random.randint(0, len(all_items)-1)
        return all_items[rand_index]


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

    elif method == "CnA":
        cost = Allocation.CnA_algorithm(net, items, frequency_of_items)
        print("DeBruijn Chen and Arash Static allocation cost = ", cost)
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
    elif method == "CnA":
        res = OnlineAdjustment.CnA_access(net, item)
    elif method == "global":
        res = OnlineAdjustment.global_access(net, item)
    else:
        res = 0
    return res


# Static G-DACH
def single_test_static(method, net, item):
    if method == "normal":
        res = OnlineAdjustment.static_normal_access(net, item)
    elif method == "CnA":
        res = OnlineAdjustment.CnA_access_static(net, item)
    elif method == "global":
        res = OnlineAdjustment.global_static_access(net, item)
    else:
        res = 0
    return res


def run_online(method, number_of_requests, net,wbl_network, items, p):
    # access_list = []
    cost_sum = 0
    static_sum = 0
    wbl_sum = 0
    network_copy = net.copy()

    item_index = random.randint(0, len(list_items) - 1)
    prev_item = items[item_index]
    for i in range(0, number_of_requests):
        item = temporal_data(p, items, prev_item)
        # item_index = random.randint(0, len(list_items) - 1)
        # item = items[item_index]
        cost_sum += single_test_online(method, net, item)
        static_sum += single_test_static(method, network_copy, item)
        wbl_sum += OnlineAdjustment.wbl_access(wbl_network, item)
        # access_list.append(item.binary_repr)

    print("Total online cost for ", num_requests, " requests is ", cost_sum)
    return cost_sum/num_requests, static_sum/num_requests, wbl_sum/num_requests


# First plot
def run_1(number_of_requests, CnA_net, WBL_net, items, p):
    cna_sum = 0
    static_sum = 0
    wbl_sum = 0
    network_copy = CnA_net.copy()

    item_index = random.randint(0, len(list_items) - 1)
    prev_item = items[item_index]
    for i in range(0, number_of_requests):
        item = temporal_data(p, items, prev_item)
        cna_sum += single_test_online("CnA", CnA_net, item)
        static_sum += single_test_static("CnA", network_copy, item)
        wbl_sum += OnlineAdjustment.wbl_access(WBL_net, item)
        # TODO : Global : L-DACH

    print("Total online cost for ", num_requests, " requests is ", cna_sum)
    return cna_sum/num_requests, static_sum/num_requests, wbl_sum/num_requests


def plot_1(wbl_result, stat_res, Local_CnA, temporal_locality):
    fig = plt.figure(figsize=(3, 6))
    plt.plot(temporal_locality, wbl_result, color="green", label='WBL')
    plt.plot(temporal_locality, stat_res, color="blue", label='Static G-DACH')
    plt.plot(temporal_locality, Local_CnA, color="red", label='Online G-DACH')
    # plt.plot(temporal_locality, results[:, 3], color="black", label='Proportional Fractional')
    plt.title(f'Different Algorithms')
    plt.xlabel("Temporal Locality")
    plt.ylabel("Average Access Cost per Request")
    plt.legend()
    plt.xticks(temporal_locality)
    plt.show()
    fig.savefig('plot1.png', dpi=fig.dpi)
    return


# Second Plot
def run_2(number_of_requests, CnA_net, free_for_all_net, items, p):
    cna_sum = 0
    static_sum = 0
    global_online_sum = 0
    global_static = 0
    network_copy = CnA_net.copy()
    free_for_all_copy = free_for_all_net.copy()

    item_index = random.randint(0, len(list_items) - 1)
    prev_item = items[item_index]
    for i in range(0, number_of_requests):
        item = temporal_data(p, items, prev_item)
        # C and A
        cna_sum += single_test_online("CnA", CnA_net, item)
        static_sum += single_test_static("CnA", network_copy, item)
        # global
        global_online_sum += single_test_online("global", CnA_net, item)
        global_static += single_test_static("global", free_for_all_copy, item)

    print("Total online cost of CnA for", num_requests, " requests is ", cna_sum)
    print("Total online cost of Global for", num_requests, " requests is ", global_online_sum)

    return cna_sum/static_sum, global_online_sum/global_static


def plot_2(cna_res, global_res, temporal_locality):
    fig = plt.figure(figsize=(3, 6))
    plt.plot(temporal_locality, cna_res, color="green", label='Online G-DACH')
    plt.plot(temporal_locality, global_res, color="blue", label='Online L-DACH')
    plt.title(f'Different Algorithms')
    plt.xlabel("Temporal Locality")
    plt.ylabel("Access Cost/ Static Cost")
    plt.legend()
    plt.xticks(temporal_locality)
    plt.show()
    fig.savefig('plot2.png', dpi=fig.dpi)
    return


# Plot 3
def run_3(number_of_requests, CnA_net, free_for_all_net, items, p):
    cna_sum = 0
    static_sum = 0
    global_online_sum = 0
    global_static = 0
    network_copy = CnA_net.copy()
    free_for_all_copy = free_for_all_net.copy()

    item_index = random.randint(0, len(list_items) - 1)
    prev_item = items[item_index]
    for i in range(0, number_of_requests):
        item = temporal_data(p, items, prev_item)
        # C and A
        cna_sum += single_test_online("CnA", CnA_net, item)
        static_sum += single_test_static("CnA", network_copy, item)
        # global
        global_online_sum += single_test_online("global", CnA_net, item)
        global_static += single_test_static("global", free_for_all_copy, item)

    print("Total online cost of CnA for", num_requests, " requests is ", cna_sum)
    print("Total online cost of Global for", num_requests, " requests is ", global_online_sum)

    return cna_sum/static_sum, global_online_sum/global_static


def plot_3(cna_res, global_res, degree_of_net):
    fig = plt.figure(figsize=(3, 6))
    plt.plot(degree_of_net, cna_res, color="green", label='Online G-DACH')
    plt.plot(degree_of_net, global_res, color="blue", label='Online L-DACH')
    plt.title(f'Different Algorithms')
    plt.xlabel("Temporal Locality")
    plt.ylabel("Access Cost/ Static Cost")
    plt.legend()
    plt.xticks(degree_of_net)
    plt.show()
    fig.savefig('plot2.png', dpi=fig.dpi)
    return


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


# Plotting functions
' parameters of network and setup '
logn = 6
num_items = (2 ** logn) * 1000
additive = True
factor = 4
network, wbl_net, node_cap = run_setup(logn, num_items, global_routing=False, additive_flag=additive, factor=factor)

'frequency of items for static allocation'
list_items, frequencies = get_data(False, long_binary_item=True, node_cap=node_cap, log_numNodes=logn)

network_chen = network.copy()
network_Arash = network.copy()
network_CnA = network.copy()
network_global = network.copy()

'static- allocate items in WBL'
cost_of_wbl = Allocation.WBL_static_allocation(wbl_net, list_items, frequencies)
print("WBL static allocation cost is = ", cost_of_wbl)

'static- allocate items in DeBruijn'
'------ options for method = {"greedyFreeForAll", "Chen", "LevelByLevel, "CnA", "Arash", "Fractional", "Prop-Arash"}'
start_time = time.time()
string_method = "greedyFreeForAll"
cost_of_static = static_allocation_DeBruijn(string_method, network_global, list_items, frequencies)
# network.empty_network()
#
string_method = "Chen"
cost_of_static = static_allocation_DeBruijn(string_method, network_chen, list_items, frequencies)
# network.empty_network()
#
# string_method = "LevelByLevel"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()
#
string_method = "Arash"
cost_of_static = static_allocation_DeBruijn(string_method, network_Arash, list_items, frequencies)
# network.empty_network()
#
# string_method = "Prop-Arash"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()
#
# string_method = "Fractional"
# cost_of_static = static_allocation_DeBruijn(string_method, network, list_items, frequencies)
# network.empty_network()

string_method = "CnA"
cost_of_static = static_allocation_DeBruijn(string_method, network_CnA, list_items, frequencies)
# network.empty_network()
print("Time for static=", time.time()-start_time)

"""Testing  Online Adjustments"""
"""------ options for method = {"normal, "Arash", "Fractional", "CnA"}"""
# start_time = time.time()

# First Plot
num_requests = 1000
p_arr = [0.1, 0.3, 0.5, 0.7, 0.9]
static_res = []
cna_online = []
wbl_res = []
repeats = 2
for p in p_arr:
    result = 0
    online = 0
    static = 0
    wbl = 0
    for r in range(0, repeats):
        net_copy = network_CnA.copy()
        cost_online, cost_static, wbl_cost = run_1(num_requests, net_copy, wbl_net, list_items, p)
        online += cost_online
        static += cost_static
        wbl += wbl_cost
    cna_online.append(online/repeats)
    static_res.append(static/repeats)
    wbl_res.append(wbl/repeats)
    print("WBL=", wbl)

# print("Time for All Onlines=", time.time()-start_time)
plot_1(wbl_res, static_res, cna_online, p_arr)


# # Second plot
# num_requests = 1000
# p_arr = [0.1, 0.3, 0.5, 0.7, 0.9]
# cna_online = []
# global_online = []
# repeats = 2
# for p in p_arr:
#     result = 0
#     cna_run = 0
#     global_run = 0
#     wbl = 0
#     for r in range(0, repeats):
#         net_copy = network_CnA.copy()
#         cost_online, cost_global = run_2(num_requests, net_copy, network_global, list_items, p)
#         cna_run += cost_online
#         global_run += cost_global
#     cna_online.append(cna_run/repeats)
#     global_online.append(global_run/repeats)
#
# # print("Time for All Onlines=", time.time()-start_time)
# plot_2(cna_online, global_online, p_arr)
#





