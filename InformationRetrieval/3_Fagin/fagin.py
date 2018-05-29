import csv
import pandas as pd
import numpy as np
import operator

# given a DataFrame it returns a dictonary of dictionaries: the first key is the number of the query, the second is the 
# DocID and its score for that query, in 'rank' finally is stored the rank for the Docs in an ordered list of DocsID.
def createQueryDic(cranFile):
    n_queries = max(cranFile["Query_ID"].values)
    cranDic = {}
    for q in range(1,n_queries+1):
        docs =  list(cranFile[cranFile["Query_ID"] == q]["Doc_ID"])
        docs = list(map(str,docs))
        score =  list(cranFile[cranFile["Query_ID"] == q]["Score"])
        cranDic[q] = {str(docs[i]): score[i] for i in range(len(score))}
        cranDic[q]['rank'] = docs
    return(cranDic)

# given the dictonaries for the results of the queries for title and text it computes the fagin's algorithm for the 
# query q, for k results.
def fagin(cran_title, cran_text, q, k):
    cdocs = [] # candidate docsID
    count = 0 # how many couples of docs we've find till row r 
    r = 0 # the row number (or the rank)
    
    while count<k and r<len(cran_title[q]['rank']) and r<len(cran_text[q]['rank']):
        doc = cran_title[q]['rank'][r]
        if doc not in cdocs:
            cdocs.append(doc)
        else:
            count += 1
        doc = cran_text[q]['rank'][r]
        if doc not in cdocs:
            cdocs.append(doc)
        else:
            count += 1
        r += 1
        
    if k!=count:
        cdocs = set(cran_title[q]['rank']).union(cran_text[q]['rank'])
    # now we have to compute the scores for the candidate documents and we store them into fdocs
    fdocs = {} # final scores for the documents
    for doc in cdocs:
        score = 0
        if doc in cran_title[q].keys():
            score += cran_title[q][doc]*2 # two times for the title
        if doc in cran_text[q].keys():
            score += cran_text[q][doc] # one time for the text
        fdocs[doc] = score
    # finally k docs with the higher score
    fdocs['rank'] = [i for i,j in sorted(fdocs.items(), key=operator.itemgetter(1), reverse = True)][:k]
    return(fdocs)


# it prints the results into a tsv file.
def printResults(output,outputFileName):
    with open(outputFileName, 'w') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter = '\t')
        tsv_writer.writerow(['Query_ID', 'Doc_ID', 'Rank', 'Score']) # first row
        for query in sorted(output.keys()): # for each query
            r = 1
            for doc in output[query]['rank']: # the ordered docsID
                tsv_writer.writerow([str(query), doc, str(r), str(output[query][doc])])
                r += 1


#############################################################################################################

import sys
try:
    titlef = sys.argv[1]
    textf = sys.argv[2]
    outputf = sys.argv[3]
    k = int(sys.argv[4])
except:
    sys.exit(('\nWrong number of arguments: given '+str(len(sys.argv)-1)+' arguments, the correct number is 4.\n\n\n' 
              'Correct use:\n\n'
              'python fagin.py output_title_file.tsv output_text_file.tsv output_fagin_file.tsv k'))

# we import the input files into DataFrames 
cran_titlef = pd.read_csv(titlef,delimiter="\t")
cran_textf = pd.read_csv(textf,delimiter="\t")

# and then we create query dictionaries
cran_title = createQueryDic(cran_titlef)
cran_text = createQueryDic(cran_textf)


output = {}
# we compute the fagin's algorithm for each query
nquery = max(cran_title.keys())
for q in range(1,nquery+1):
    output[q] = fagin(cran_title, cran_text, q, k)

# and finally we save the results into the output file
printResults(output,outputf)



# python fagin.py C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_title.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_text.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_Fagin.tsv 20


# java Fagin C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_title.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_text.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_Fagin2.tsv 20