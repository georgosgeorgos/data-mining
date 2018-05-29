import re
import csv
import time
import nltk
import json
import string
import webbrowser
import numpy as np
import pandas as pd
from nltk import stem
import sklearn.metrics
from random import randint
from numpy.linalg import norm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import time

from library_query import *
from library_content_based import *
from library_collaborative_filtering import *
#-------------------------------------------------------------------------------------------------------------------------------------

s = time.time()

books_dataFrame = pd.read_csv("../Preprocess/books_dataFrame.csv", index_col=0)


with open('../ContentBased/userDict.json', 'r') as fp:
    
    userDict = json.load(fp)
    
with open('../ContentBased/isbnDict.json', 'r') as fp:
    
    isbnDict = json.load(fp)
    
    
with open('../ContentBased/inverted_index/featuresDict_new.json', 'r') as fp:
    
    featuresDict = json.load(fp)
    
    
with open('../ContentBased/inverted_index/booksDict_new.json', 'r') as fp:
    
    booksDict = json.load(fp)
    
with open('../ContentBased/inverted_index/usersDict_new.json', 'r') as fp:
    
    usersDict = json.load(fp)
    
with open('../ContentBased/inverted_index/inverted_index.json', 'r') as fp:
    
    inverted_index = json.load(fp)
    
print("Ok")

#--------------------------------------------------------------------------------------------------------------------------------------

with open('../ContentBased/Content_based/books.json', 'r') as fp:
    
    books = json.load(fp)
    
with open('../ContentBased/Content_based/users.json', 'r') as fp:
    
    users = json.load(fp)
    
    
with open('../ContentBased/Content_based/mostRated.json', 'r') as fp:
    
    mostRated = json.load(fp)

print("Ok")

#---------------------------------------------------------------------------------------------------------------------------------------


with open('../CollaborativeFiltering/new_userDict.json', 'r') as fp:
    
    new_userDict = json.load(fp)
    
# select only books in isbnDict rated by more that three users with a non-zero rating    
    
with open('../CollaborativeFiltering/new_isbnDict.json', 'r') as fp:
    
    new_isbnDict = json.load(fp)
    
    
with open('../CollaborativeFiltering/dict_row.json', 'r') as fp:
    
    dict_row = json.load(fp)
    
    
with open('../CollaborativeFiltering/dict_col.json', 'r') as fp:
    
    dict_col = json.load(fp)
    
    
with open('../CollaborativeFiltering/clustering/file/clusters_dict_row.json', 'r') as fp:
    
    clusters_dict_row = json.load(fp)
       
with open('../CollaborativeFiltering/clustering/file/clusters_dict_col.json', 'r') as fp:
    
    clusters_dict_col = json.load(fp)
    

with open('../CollaborativeFiltering/clustering/index_book_user_clusters/index_user_cluster.json', 'r') as fp:
    
    index_user_cluster = json.load(fp)
    
    
with open('../CollaborativeFiltering/clustering/index_book_user_clusters/index_book_cluster.json', 'r') as fp:
    
    index_book_cluster = json.load(fp)
    
    
with open('../CollaborativeFiltering/clustering/CLUSTERS_ITEMS.json', 'r') as fp:
    
    CLUSTERS_ITEMS = json.load(fp)
    
    
with open('../CollaborativeFiltering/clustering/CLUSTERS_USERS.json', 'r') as fp:
    
    CLUSTERS_USERS = json.load(fp)

print("Ok")
#--------------------------------------------------------------------------------------------------------------------------

u_cluster, R_cluster, utility_DataFrame_cluster = computeMatrices(CLUSTERS_USERS,CLUSTERS_ITEMS,
                                                                           CLUSTERS_USERS,CLUSTERS_ITEMS,
                                                                            clusters_dict_row,clusters_dict_col)


u, R, utility_DataFrame = computeMatrices(new_userDict,new_isbnDict,new_userDict,new_isbnDict,dict_row,dict_col)

d_user_content = sorted(userDict.keys())
d_isbn_content = sorted(isbnDict.keys())


print("Data loaded")

e = time.time()

print(e-s)
#----------------------------------------------------------------------------------------------------------------------------

def main():

	r = -1
	while True:
	    while r not in ["y","n"]:
	        print("\nDo you want a recommendation?\n")
	        print("y")
	        print("n\n")
	        r = input()
	    if r == "y":
	        while r not in [0,1]:
	            print("\nWhat method do you want to use?\n")
	            print("0 Content Based")
	            print("1 Collaborative Filtering\n")
	            
	            r = int(input())
	        if r == 0:

	            try:
	                user_number,recommendation = mainContentBased(featuresDict,userDict,isbnDict,users,books,
	                                                              d_user_content,d_isbn_content,books_dataFrame,mostRated,0.2)
	                try:
	                	buy(recommendation,mostRated,books_dataFrame)
	                except:
	                	print("Sorry no more memory...")
	            
	            except:

	                print("you are a new user(Cold Star!!!). We can only recommend you the most popular books in our database:\n")
	                for i in mostRated:
	                    print(books_dataFrame["Book-Title"][i[0]])
	                try:
	                	buy(recommendation,mostRated,books_dataFrame)
	                except:
	                	print("Sorry no more memory...")

	        elif r == 1:
	            mainCollaborativeFiltering_CLUSTERING(books_dataFrame, utility_DataFrame, utility_DataFrame_cluster,R_cluster, new_userDict, new_isbnDict,
	                                          index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated)    
	    elif r == "n":

	        print("Bye")
	        break

	return None


main()