import pandas as pd
import numpy as np
import sys

class createTables:
    
    def __init__(self,ground_truth):
        
        self.ground_truth = ground_truth
        
        
    def createTruth(self):
    
        n_queries = max(self.ground_truth["Query_id"].values)
        truth = {}
        for q in range(1,n_queries+1):
            truth[q] = list(self.ground_truth[self.ground_truth["Query_id"] == q]["Relevant_Doc_id"])
            
        return truth
    
    def createQueryTable(self, cran):
    
        '''
        input: DataFrame
        output: Dict ---> key1:(int) queryID  value1:(dict) ---> key2: (int) rank  value2: (list) [docID, score]
        '''

        n_queries = max(cran["Query_ID"])
        cran_dict = {}

        for q in range(1,n_queries+1):

            docs =  list(cran[cran["Query_ID"] == q]["Doc_ID"])
            rank =  list(cran[cran["Query_ID"] == q]["Rank"])
            score = list(cran[cran["Query_ID"] == q]["Score"])

            cran_dict[q] = {rank[i]:[docs[i], score[i]] for i in range(len(rank))}

        return cran_dict



class evaluation_R:

    def __init__(self,cran_dict,truth):

            self.cran_dict = cran_dict
            self.truth = truth

    def R_precision(self,query_id):

            relevant = self.truth[query_id]
            rel = len(relevant)

            retrieved = list(self.cran_dict[query_id].values())
            retrieved = [retr[0] for retr in retrieved[:rel]]

            intersect = set(retrieved).intersection(set(relevant))

            r = len(intersect)

            R = r/rel
            return R

    def average_R(self):

        l_R = []
        for q in self.cran_dict.keys():
            try:    
                R = self.R_precision(q) 
                l_R.append(R)
            except:
                continue
                
        return np.mean(l_R)




def main_R(cran_string,string_truth,name):

    ground_truth = pd.read_csv(string_truth,delimiter="\t")
    cran = pd.read_csv(cran_string, delimiter="\t")

    cT = createTables(ground_truth)
    truth = cT.createTruth()
    cran_dict = cT.createQueryTable(cran)

    evals = evaluation_R(cran_dict,truth)
    aR = evals.average_R()
    
    print(name)
    print("averaged R-precision: ", round(aR,4))
    print("\n")
    
    return aR




string = sys.argv

cran_string = string[1]
string_truth = string[2]
name = string[3]



main_R(cran_string,string_truth,name)