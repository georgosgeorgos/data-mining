import csv
import pprint as pp
import networkx as nx
import itertools as it
import math
import scipy.sparse
import random


def pagerank(M, N, nodelist, alpha=0.85, personalization=None, max_iter=100, tol=1.0e-6, dangling=None):
    if N == 0:
        return {}
    S = scipy.array(M.sum(axis=1)).flatten()
    S[S != 0] = 1.0 / S[S != 0]
    Q = scipy.sparse.spdiags(S.T, 0, *M.shape, format="csr")
    M = Q * M

    # initial vector
    x = scipy.repeat(1.0 / N, N)

    # Personalization vector
    if personalization is None:
        p = scipy.repeat(1.0 / N, N)
    else:
        missing = set(nodelist) - set(personalization)
        if missing:
            # raise NetworkXError('Personalization vector dictionary must have a value for every node. Missing nodes %s' % missing)
            print()
            print("Error: personalization vector dictionary must have a value for every node")
            print()
            exit(-1)
        p = scipy.array([personalization[n] for n in nodelist], dtype=float)
        # p = p / p.sum()
        sum_of_all_components = p.sum()
        if sum_of_all_components > 1.001 or sum_of_all_components < 0.999:
            print()
            print("Error: the personalization vector does not represent a probability distribution :(")
            print()
            exit(-1)

    # Dangling nodes
    if dangling is None:
        dangling_weights = p
    else:
        missing = set(nodelist) - set(dangling)
        if missing:
            # raise NetworkXError('Dangling node dictionary must have a value for every node. Missing nodes %s' % missing)
            print()
            print("Error: dangling node dictionary must have a value for every node.")
            print()
            exit(-1)
        # Convert the dangling dictionary into an array in nodelist order
        dangling_weights = scipy.array([dangling[n] for n in nodelist], dtype=float)
        dangling_weights /= dangling_weights.sum()
    is_dangling = scipy.where(S == 0)[0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = x
        x = alpha * (x * M + sum(x[is_dangling]) * dangling_weights) + (1 - alpha) * p
        # check convergence, l1 norm
        err = scipy.absolute(x - xlast).sum()
        if err < N * tol:
            return dict(zip(nodelist, map(float, x)))
    # raise NetworkXError('power iteration failed to converge in %d iterations.' % max_iter)
    print()
    print("Error: power iteration failed to converge in " + str(max_iter) + " iterations.")
    print()
    exit(-1)


def create_graph_set_of_users_set_of_items(user_item_ranking_file):
    graph_users_items = {}
    all_users_id = set()
    all_items_id = set()
    g = nx.DiGraph()
    input_file = open(user_item_ranking_file, "r")
    input_file_csv_reader = csv.reader(input_file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_NONE)
    for line in input_file_csv_reader:
        user_id = int(line[0])
        item_id = int(line[1])
        rating = int(line[2])
        g.add_edge(user_id, item_id, weight=rating)
        all_users_id.add(user_id)
        all_items_id.add(item_id)
    input_file.close()
    graph_users_items["graph"] = g
    graph_users_items["users"] = all_users_id
    graph_users_items["items"] = all_items_id
    return graph_users_items


###############################################################################################################################
##############################################################################################################################


def create_item_item_graph(graph_users_items):

    """
    starting from the directed user item graph generate a
    undirected item item graph
    """

    global_graph = graph_users_items["graph"]
    all_users_id = graph_users_items["users"]
    all_items_id = graph_users_items["items"]

    g = nx.Graph()

    # for every user
    for node in all_users_id:

        # items rated by this user
        items_user = sorted(global_graph[node])
        N = len(items_user)

        # for every possible edge between the items
        for i in range(N):
            for j in range(i + 1, N):

                u = items_user[i]
                v = items_user[j]

                # weight on edge between items
                if g.has_edge(u, v):
                    g[u][v]["weight"] += 1
                else:
                    g.add_edge(u, v, weight=1)

    return g


def create_preference_vector_for_teleporting(user_id, graph_users_items):

    global_graph = graph_users_items["graph"]
    all_users_id = graph_users_items["users"]
    all_items_id = graph_users_items["items"]

    preference_vector = {k: 0 for k in all_items_id}

    N = 0
    for item in global_graph[user_id]:
        N = N + global_graph[user_id][item]["weight"]

    for item in global_graph[user_id]:
        preference_vector[item] = global_graph[user_id][item]["weight"] / N

    return preference_vector


def create_ranked_list_of_recommended_items(page_rank_vector_of_items, user_id, training_graph_users_items):

    # items rated by this user
    items_rated = training_graph_users_items["graph"][user_id]

    # [item,score] given by personalized PageRank
    res = [[k, page_rank_vector_of_items[k]] for k in page_rank_vector_of_items if k not in items_rated]

    # sorted [item,score]
    res = sorted(res, key=lambda u: u[1], reverse=True)

    sorted_list_of_recommended_items = [element[0] for element in res]

    return sorted_list_of_recommended_items


def discounted_cumulative_gain(user_id, sorted_list_of_recommended_items, test_graph_users_items):

    test_graph = test_graph_users_items["graph"][user_id]
    tot = len(test_graph)

    evaluation_list = []

    for item in sorted_list_of_recommended_items:
        if item in test_graph:
            evaluation_list.append((item, test_graph[item]["weight"]))
        if len(evaluation_list) == tot:
            break

    dcg = evaluation_list[0][1]

    for ix in range(1, len(evaluation_list)):

        dcg = dcg + evaluation_list[ix][1] / math.log(2 + ix, 2)

    return dcg


def maximum_discounted_cumulative_gain(user_id, test_graph_users_items):

    test_graph = test_graph_users_items["graph"][user_id]
    evaluation_list = [(item, test_graph[item]["weight"]) for item in test_graph]
    evaluation_list = sorted(evaluation_list, key=lambda u: u[1], reverse=True)

    m_dcg = evaluation_list[0][1]

    for ix in range(1, len(evaluation_list)):
        m_dcg = m_dcg + evaluation_list[ix][1] / math.log(2 + ix, 2)

    return m_dcg
