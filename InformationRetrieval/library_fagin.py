import numpy as np


class Fagin:
    
    def __init__(self,cran_title,cran_text):
        
        self.cran_title = cran_title
        self.cran_text = cran_text
        

    def fagin(self,data, K=200):

        k = 0
        res = {}

        N = len(data["title"]["order"])
        sections = list(data)

        n = 0
        for n in range(N):
            for section in sections:

                element = data[section]["order"][n]
                res[element] = res.get(element,[]) + [section]

                if len(res[element]) == len(sections):
                    k +=1

                if k >= K:
                    break
            if k >= K:
                break


        final_result = {k:0 for k in res}
        for section in sections:
            for x in res:
                element = data[section]["score"]
                final_result[x] += element.get(x,0)

        top_k = sorted([(f,final_result[f]) for f in final_result], key=lambda u: u[1], reverse=True)

        return top_k
    
    
    def writeData(self,result_DataFrame, top_k, query):
        new = []
        rank = 1
        for t_k in top_k:

            new.append([str(query),str(t_k[0]),str(rank),str(t_k[1])])
            rank +=1

        new = pd.DataFrame(np.array(new), columns=result_DataFrame.columns)
        result_DataFrame = pd.concat([result_DataFrame,new], axis=0)

        return result_DataFrame

    def main(self):

        result_DataFrame = pd.DataFrame(columns=["Query_ID", "Doc_ID", "Rank", "Score"])
        for query in self.cran_title.keys():
            try:
                title = self.cran_title[query]
                text = self.cran_text[query]
                title_rank = [title[t][0] for t in title]
                text_rank = [text[t][0] for t in text]

                data = {"title": { "score": {title[t][0]:title[t][1]*2 for t in title},  "order":title_rank},
                        "text":  { "score": {text[t][0]:text[t][1] for t in text},      "order":text_rank}}

                top_k = self.fagin(data)
                top_k = top_k[:200]
                result_DataFrame = self.writeData(result_DataFrame, top_k, query)

            except:
                continue


        return result_DataFrame