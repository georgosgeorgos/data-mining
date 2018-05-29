import re
import csv
import time
import nltk
import json
import string
import numpy as np
import pandas as pd
from nltk import stem
import sklearn.metrics
from random import randint
from numpy.linalg import norm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def cleanQuery(query):

    stop = stopwords.words('english')
    stemmer = stem.PorterStemmer()
    wnl = WordNetLemmatizer()

    query = str(query).lower()
    query = re.sub(r"\W+" , " ", str(query)).split()    
    query = [wnl.lemmatize(word) for word in query if word not in stop]
    query = [stemmer.stem(word) for word in query]
    
    return query

def processQuery(q_list, inverted_index):
    
    books = set()
    i = 0
    for q in q_list:
        if i == 0:
            try:
                p = set(list(inverted_index[q].keys()))
                books = books.union(p)
            except:
                i = 1   
        else:
            try:
                p = set(inverted_index[q].keys())
                books = books.intersection(p) 
            except:
                continue        
    return books

def SimilarityinvertedIndex(isbnDict, featuresDict,booksDict, q_list, books, books_dataFrame):
    
    books = np.array(list(books))
    
    if len(books)>250:
        
        books = books[np.random.randint(0,len(books),250)]
    
    X_myQuery = np.zeros(len(featuresDict))

    # others users
    X_items = np.zeros((len(books),len(featuresDict)))


    for q in q_list:

        X_myQuery[featuresDict[q]] = 1

        
    for b in range(len(books)):

        try:
            for feature in booksDict[books[b]]:

                X_items[b][featuresDict[feature]] = booksDict[books[b]][feature]

        except:
            continue

    num = (X_myQuery*X_items).sum(axis=1)

    d_myQuery = np.sqrt((X_myQuery**2).sum())
    d_items = np.sqrt((X_items**2).sum(axis=1))

    res = num/(d_myQuery*d_items)
   
    ff = sorted(zip(books,res), key=lambda tup: tup[1], reverse=True)
    
    v = []
    titles = set()
    for f in ff[:20]:
        try:
            title = books_dataFrame["Book-Title"][f[0]]
            if title not in titles: 
                v.append([title,f[0]])

            titles.update([title])
        except:
            continue
    v = {k:v for k,v in enumerate(v)}
    
    return v


def mainSimilarity(isbnDict, inverted_index, featuresDict,booksDict,books_dataFrame):
    
    d = -1
    while d != 0:
        print("Search book:\n")
        query = input()
        print("Please wait...")
        try:
            q_list = cleanQuery(query)
            books = processQuery(q_list,inverted_index)
            ff = SimilarityinvertedIndex(isbnDict, featuresDict,booksDict, q_list, books, books_dataFrame)
            if ff == {}:
                print("Please try something else...\n")
            else:
                print("What do you prefer?\n")
                r = -1
                while r not in list(ff.keys()):
                    for k in ff:

                        print(k, ff[k][0])

                    r = int(input())

                book_number = ff[r][1]
                d = 0
                return book_number 
        except:
            print("Please try something else...\n")