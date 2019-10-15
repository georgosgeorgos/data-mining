import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


class createTables:
    def __init__(self, ground_truth):

        self.ground_truth = ground_truth

    def createTruth(self):

        n_queries = max(self.ground_truth["Query_id"].values)
        truth = {}
        for q in range(1, n_queries + 1):
            truth[q] = list(self.ground_truth[self.ground_truth["Query_id"] == q]["Relevant_Doc_id"])

        return truth

    def createQueryTable(self, cran):

        """
        input: DataFrame
        output: Dict ---> key1:(int) queryID  value1:(dict) --->  key2: (int) rank  value2: (list) [docID, score]
        """

        n_queries = max(cran["Query_ID"])
        cran_dict = {}

        for q in range(1, n_queries + 1):

            docs = list(cran[cran["Query_ID"] == q]["Doc_ID"])
            rank = list(cran[cran["Query_ID"] == q]["Rank"])
            score = list(cran[cran["Query_ID"] == q]["Score"])

            cran_dict[q] = {rank[i]: [docs[i], score[i]] for i in range(len(rank))}

        return cran_dict


class evaluation_nMDCG:
    def __init__(self, cran_dict, truth):

        self.cran_dict = cran_dict
        self.truth = truth

    def compute_nMDCG(self, query_id, K):

        k = 1
        MDCG = []

        doc_id1 = self.cran_dict[query_id][k][0]

        rel = self.relevance(query_id, doc_id1)
        if rel != 0:
            MDCG.append(rel)
        k += 1

        K = min(K, len(self.cran_dict[query_id]))

        while k <= K:

            doc_id = self.cran_dict[query_id][k][0]
            rel = self.relevance(query_id, doc_id) / np.log2(k)
            if rel != 0:
                MDCG.append(rel)

            k += 1

        max_MDCG = self.routine(MDCG)

        if max_MDCG != []:
            nMDCG = sum(MDCG) / sum(max_MDCG)
        else:
            nMDCG = sum(MDCG)

        return nMDCG, MDCG, max_MDCG

    def routine(self, MDCG):

        """
        compute the max_nMDCG
        """

        max_MDCG = []
        K = len(MDCG)
        if K == 0:
            return []
        k = 1
        max_MDCG.append(1)
        k += 1

        while k <= K:
            max_MDCG.append(1 / np.log2(k))
            k += 1

        return max_MDCG

    def relevance(self, query_id, doc_id):

        rel = 0
        if doc_id in self.truth[query_id]:
            rel = 1
        return rel

    def average_nMDCGs_given_k(self, k):

        l_nMDCG = []

        for q in self.cran_dict.keys():
            try:
                nMDCG = self.compute_nMDCG(q, k)[0]
                l_nMDCG.append(nMDCG)

            except:
                continue

        return np.mean(l_nMDCG)

    def average_nMDCGs(self, Ks):

        vector = []

        for k in Ks:
            vector.append([k, self.average_nMDCGs_given_k(k)])

        vector = np.array(vector)

        return vector

    def plot_result(self, vector, name):

        plt.plot(vector[:, 0], vector[:, 1])
        plt.grid()
        plt.xlabel("k")
        plt.ylabel("average nMDCG")
        plt.title(name)

        folder = name.split("_")[0]
        plt.savefig("./output/" + folder + "/" + name + ".pdf", bbox_inches="tight")


def main_nMDCG(cran_string, string_truth, name):

    ground_truth = pd.read_csv(string_truth, delimiter="\t")
    cran = pd.read_csv(cran_string, delimiter="\t")

    cT = createTables(ground_truth)
    truth = cT.createTruth()
    cran_dict = cT.createQueryTable(cran)
    evals = evaluation_nMDCG(cran_dict, truth)
    Ks = [1, 3, 5, 10]
    vector = evals.average_nMDCGs(Ks)
    evals.plot_result(vector, name)

    print(name)
    for v in vector:
        print("k: ", int(v[0]))
        print("averaged nMDCG: ", round(v[1], 4))
    print("\n")

    return vector


string = sys.argv

cran_string = string[1]
string_truth = string[2]
name = string[3]


main_nMDCG(cran_string, string_truth, name)
