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

from library_query import *



def computeMatrices(train_userDict,train_isbnDict,small_userDict,small_isbnDict, dict_row, dict_col):

    n = len(small_isbnDict)
    m = len(small_userDict)
    
    index = sorted(small_userDict.keys())
    columns = sorted(small_isbnDict.keys())

    dict_row = {k:v for v,k in enumerate(index)}
    dict_col = {k:v for v,k in enumerate(columns)}

    u = np.zeros((m,n)) 
    R = np.zeros((m,n))
    for user in train_userDict:
        for isbn in train_userDict[user]:
            try:
                u[dict_row[user]][dict_col[isbn]] = train_userDict[user][isbn]
                R[dict_row[user]][dict_col[isbn]] = 1
            except:
                continue

    for isbn in train_isbnDict:
        for user in train_isbnDict[isbn]:
            try:
                u[dict_row[user]][dict_col[isbn]] = train_isbnDict[isbn][user]
                R[dict_row[user]][dict_col[isbn]] = 1
            except:
                continue
                
    small_utility_DataFrame = pd.DataFrame(u, index = index, columns = columns)
    R = pd.DataFrame(R, index = index, columns = columns)

    return u, R, small_utility_DataFrame



def convert(user_number,book_number, index_user_cluster, index_book_cluster):
    
    try:
        user_cluster = index_user_cluster[user_number]
    except:
        print("key problem")
        return None
    
    if book_number != None:
        
        try:
            book_cluster = index_book_cluster[book_number]
            return user_cluster, book_cluster
        except:
            print("key problem")
            return None
        
    return user_cluster


def booksRatedUser(new_isbnDict, new_userDict, user_number, score):
    
    '''
    input:  new_userDict (Dict), user_number (int), score (int)
    
    action: select all books well rated by my user
    
    output: books_rated (list)
    
    '''
    
    books_rated = []
    
    for book in new_userDict[str(user_number)]:
        
        if int(new_userDict[str(user_number)][book]) > score:
            
            try:
                
                new_isbnDict[book]
                books_rated.append(book)
                
            except:
                
                continue
            
    return list(set(books_rated))


def SimilarityBooks(utility_DataFrame, book_number, books_similar, measure = "euclid"):
    
    '''
    
    input: utility_DataFrame (DataFrame), book_number (int), books_similar (List)
    
    action: compute cosine similarity between book_number and all the books in books_similar
    
    output: new_similarity (List of tuples)
    
    '''

    x = utility_DataFrame[str(book_number)]
    x_length = norm(x)
    
    y = utility_DataFrame[books_similar]
    y_length = norm(utility_DataFrame[books_similar],axis=0)

    
    num = (y.T.values*x.values).sum(axis=1)
    
    if measure == "cos":
        den = x_length*y_length
    else:
        den = 1

    similarity = num/den
    similarity = np.nan_to_num(similarity)
    
    d = list(zip(list(books_similar),similarity))
    new_similarity = sorted(d, key=lambda tup: tup[1], reverse=True)
    
    return new_similarity

def itemItemsRecommendation(new_similarity, user_number, book_number, k, new_userDict):
    
    
    '''
    
    input:  new_similarity(List of tuples), new_isbnDict(Dict), k(int)
    
    action: recommend item using the ratings of similar items
    
    output: recommendation (float)
    
    '''
    
    
    if len(new_similarity) < k:
        
        
        recommendation = np.mean([u[1] for u in new_similarity])
    
    else:
        
        for u in new_similarity[:k]:
            
            recommendation = np.mean([u[1] for u in new_similarity[:k]])
        
    
    return recommendation

def itemItemsScore(new_userDict, new_similarity, k, user_number):
    
    score = [int(new_userDict[str(user_number)][u[0]]) for u in new_similarity[:k]]
    
    if score == []:
        
        #print("Not possible to perform recommendations")
        return None
    
    return np.mean(score)

def CollaborativeFilteringItemItems(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number, score_min, k):
    
    
    '''
    
    generate the book_number rating for the user_number using similarity between number_book and book rated by number_user   
    
    '''
    
    score = None
    books_rated_user = booksRatedUser(new_isbnDict, new_userDict, user_number,score_min)
    
    
    if books_rated_user == []:
        
        return score
    
    new_similarity = SimilarityBooks(utility_DataFrame, book_number, books_rated_user)
    
    
    if new_similarity == []:

        return score
    
    recommendation = itemItemsRecommendation(new_similarity[1:], user_number, book_number, k, new_userDict)
    
    
    if recommendation == 0.0:
        
        return score
        
        
    score = itemItemsScore(new_userDict, new_similarity[1:], k, user_number)
    
    return score



def mainItemItems_clustering(books_dataFrame, utility_DataFrame, utility_DataFrame_cluster,R_cluster, new_userDict, new_isbnDict, d_user, d_isbn,
                  index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated,
                  score_min = 0, k = 3):
    
    
    print("Please choose a user and/or an item\n")
    print("user or random user: \n")
    user_number = input()
    if user_number == "":
        user_number = None
    print("Do you want to search by ISBN or by words?\n")
    print("0 by ISBN")
    print("1 by words")
    g = -1
    while g not in [0,1]:
        g = int(input())
    if g == 1:
        book_numbers = mainSimilarity(isbnDict,inverted_index, featuresDict,booksDict,books_dataFrame)
        try:
            new_isbnDict[str(book_numbers)]
        except:
            print("We don't have this book in the utility matrix. We can only recommend the most popular and well rated books in the database:\n")
            for i in mostRated:
                print(books_dataFrame["Book-Title"][i[0]])
            return None
    elif g == 0:
        print("item or random item: \n")
        book_numbers = input()
    if book_numbers == "":
        book_numbers = None
    
    if user_number != None or book_numbers != None:
        
        if user_number == None:
            
            n = randint(0,len(new_userDict))
            user_number = d_user[n]
            
        if book_numbers == None:
            
            m = randint(0,len(new_isbnDict))
            book_numbers = d_isbn[m]
        
        for book_number in book_numbers.split():
            score = None
            
            score = CollaborativeFilteringItemItems(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number,
                                                    score_min, k)
            if score == None:

                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)

                if R_cluster[book_cluster][user_cluster] == 1:

                    score = utility_DataFrame_cluster[book_cluster][user_cluster]
                    
            if score == None:
                    
                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]
                    
                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]
                    
                    score = (np.mean(term1) + np.mean(term2))/2
                    
            if score == None:
                print("Nothing to recommend")
                
            else:    
                try:
                    print("\nThe predicted rating (using item-based with clusterization) for book <", 
                          books_dataFrame.loc[book_number]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", np.round(score,3),"\n")

                except:
                    print(book_number, user_number, score)
                    
            
        
    else:

        score = None

        while score == None:



            n = randint(0,len(new_userDict))
            m = randint(0,len(new_isbnDict))

            user_number = d_user[n]
            book_number = d_isbn[m]
            
            score = CollaborativeFilteringItemItems(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number, 
                                                    score_min, k)
            
            if score == None:
            
                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)
                
                if R_cluster[book_cluster][user_cluster] == 1:
                    
                    score = utility_DataFrame_cluster[book_cluster][user_cluster]
                    
            if score == None:

                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]

                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]

                    score = (np.mean(term1) + np.mean(term2))/2
                    

        try:
            print("The predicted rating (using item-based with clusterization) for book <", 
                  books_dataFrame.loc[book_number]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", np.round(score,3))

        except:
            print(book_number, user_number, score)
        
    #return book_number, user_number, score

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def usersHaveRatedBook(new_isbnDict, new_userDict, book_number, score):
    
    
    '''
    
    input:  new_isbnDict (Dict), new_userDict (Dict), book_number (int), score (int)
    
    action: select all users that have given a good rating to book_number
    
    output: users_rated (list)
    
    '''
    
    users_rated = []
    
    for user in new_isbnDict[str(book_number)]:
        
        if int(new_isbnDict[str(book_number)][user]) > score:
            
            try:
                
                new_userDict[user]
                users_rated.append(user)
                
            except:
                
                continue
            
    return list(set(users_rated))


#users_rated_book = usersHaveRatedBook(new_isbnDict, new_userDict, book_number, 5)

def SimilarityUsers(utility_DataFrame, user_number, users_similar, measure = "euclid"):
    
    '''
    
    input: utility_DataFrame (DataFrame), user_number (int), user_similar (List)
    
    action: compute cosine similarity between user_number and all the user in users_similar
    
    output: new_similarity (List of tuples)
    
    '''

    x = utility_DataFrame.loc[str(user_number)]
    x_length = norm(x)
    
    y = utility_DataFrame.loc[users_similar]
    y_length = norm(utility_DataFrame.loc[users_similar],axis=1)

    
    num = (y.values*x.values).sum(axis=1)
    
    if measure == "cos":
        den = x_length*y_length
    else:
        den = 1

    similarity = num/den
    similarity = np.nan_to_num(similarity)
    
    d = list(zip(list(users_similar),similarity))
    new_similarity = sorted(d, key=lambda tup: tup[1], reverse=True)
    
    
    return new_similarity

def ItemUsersRecommendation(new_similarity, new_userDict, k):
    
    '''
    
    input:  new_similarity(List of tuples), new_userDict(Dict), score(int), k(int)
    
    action: recommend items using the ratings of similar users
    
    output: recommendation (Dict), books (Dict)
    
    '''
    
    if new_similarity == []:
        
        return None
    
    if len(new_similarity) > k:
    
        recommendation = np.mean([u[1] for u in new_similarity[:k]]) 
    
    else:
        
        recommendation = np.mean([u[1] for u in new_similarity]) 
        
    return recommendation

def itemUsersScore(new_similarity,new_isbnDict, book_number, k):
    
    if new_similarity == []:
        
        return None
    
    if len(new_similarity) > k:
        
        score = [int(new_isbnDict[str(book_number)][u[0]]) for u in new_similarity[:k] if u[1] !=0.0]
        
    else:
        
        score = [int(new_isbnDict[str(book_number)][u[0]]) for u in new_similarity if u[1] !=0.0]
    
    return np.mean(score)

def CollaborativeFilteringItemUsers(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number, score_min = 0, k = 3):
    
    score = None
    users_rated_book = usersHaveRatedBook(new_isbnDict, new_userDict, book_number, score_min)
    
    
    if users_rated_book == []:
        
        return score
    
    
    new_similarity = SimilarityUsers(utility_DataFrame, user_number, users_rated_book)
    
    
    if new_similarity == []:

        return score
    
    recommendation = ItemUsersRecommendation(new_similarity, new_userDict, k)
    
        
    if recommendation == 0.0:
        
        return score
        
    score = itemUsersScore(new_similarity,new_isbnDict, book_number, k)
    
        
    return score


def mainItemUsers_clustering(books_dataFrame, utility_DataFrame, utility_DataFrame_cluster, R_cluster, new_userDict, new_isbnDict, d_user, d_isbn,
                  index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated,
                  score_min = 0, k = 3):
    
    
    print("Please choose a user and/or an item\n")
    print("user or random user: \n")
    user_number = input()
    if user_number == "":
        user_number = None
    print("Do you want to search by ISBN or by words?\n")
    print("0 by ISBN")
    print("1 by words")
    g = -1
    while g not in [0,1]:
        g = int(input())
    if g == 1:
        book_numbers = mainSimilarity(isbnDict,inverted_index, featuresDict,booksDict,books_dataFrame)
        try:
            new_isbnDict[str(book_numbers)]
        except:
            print("We don't have this book in the utility matrix. We can only recommend the most popular and well rated books in the database:\n")
            for i in mostRated:
                print(books_dataFrame["Book-Title"][i[0]])
            return None
    elif g == 0:
        print("item or random item: \n")
        book_numbers = input()
    if book_numbers == "":
        book_numbers = None
    
    if user_number != None or book_numbers != None:
        
        if user_number == None:
            
            n = randint(0,len(new_userDict))
            user_number = d_user[n]
            
        if book_numbers == None:
            
            m = randint(0,len(new_isbnDict))
            book_numbers = d_isbn[m]
        
        for book_number in book_numbers.split():
            
            score = None
            
            score = CollaborativeFilteringItemUsers(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number,
                                                    score_min, k)
            if score == None:

                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)

                if R_cluster[book_cluster][user_cluster] == 1:

                        score = utility_DataFrame_cluster[book_cluster][user_cluster]
                        
                if score == None:

                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]

                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]

                    score = (np.mean(term1) + np.mean(term2))/2
                    
            if score == None:
                print("Nothing to recommend")
            else:
                try:
                    print("\nThe predicted rating (using user-based with clusterization) for book <", 
                      books_dataFrame.loc[str(book_number)]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", np.round(score,3), "\n")

                except:
                    print(book_number, user_number, score)
           
                
    else:
            
        score = None

        while score == None:


            n = randint(0,len(new_userDict))
            m = randint(0,len(new_isbnDict))

            user_number = d_user[n]
            book_number = d_isbn[m]
            

            score = CollaborativeFilteringItemUsers(utility_DataFrame, new_userDict, new_isbnDict, user_number, book_number,
                                                    score_min,k)
            if score == None:
            
                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)
                
                if R_cluster[book_cluster][user_cluster] == 1:
                    
                    score = utility_DataFrame_cluster[book_cluster][user_cluster]
                    
                if score == None:

                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]

                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]

                    score = (np.mean(term1) + np.mean(term2))/2
                    
        try:

            print("The predicted rating (using user-based with clusterization) for book <", 
              books_dataFrame.loc[str(book_number)]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", np.round(score,3))

        except:

            print(book_number, user_number, score)
#----------------------------------------------------------------------------------------------------------------------------------------

def mainClustering(books_dataFrame, utility_DataFrame_cluster,R_cluster, new_userDict, new_isbnDict, d_user, d_isbn,
                  index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict, inverted_index,mostRated):
    
    
    print("Please choose a user and/or an item\n")
    print("user or random user: \n")
    user_number = input()
    if user_number == "":
        user_number = None
    print("Do you want to search by ISBN or by words?\n")
    print("0 by ISBN")
    print("1 by words")
    g = -1
    while g not in [0,1]:
        g = int(input())
    if g == 1:
        book_numbers = mainSimilarity(isbnDict,inverted_index,featuresDict,booksDict,books_dataFrame)
        try:
            new_isbnDict[str(book_numbers)]

        except:
            print("We don't have this book in the utility matrix. We can only recommend the most popular and well rated books in the database:\n")
            for i in mostRated:
                print(books_dataFrame["Book-Title"][i[0]])
            return None
    elif g == 0:
        print("item or random item: \n")
        book_numbers = input()
        if book_numbers == "":
            book_numbers = None
    
    if user_number != None or book_numbers != None:
        
        if user_number == None:
            
            n = randint(0,len(new_userDict))
            user_number = d_user[n]
            
        if book_numbers == None:
            
            m = randint(0,len(new_isbnDict))
            book_numbers = d_isbn[m]
        
        for book_number in book_numbers.split():
            
            try:
                score = None
                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)
                if R_cluster[book_cluster][user_cluster] == 1:
                        score = utility_DataFrame_cluster[book_cluster][user_cluster]
                        
                if score == None:
                    
                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]
                    
                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]
                    
                    score = (np.mean(term1) + np.mean(term2))/2
                        
                if score == None:
                    print("Nothing to recommend")
                else:
                    try:
                        print("\nThe predicted rating (using using only clusterization) for book <", 
                          books_dataFrame.loc[str(book_number)]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", 
                              np.round(score,3),"\n")
                    except:
                        print(book_number, user_number, score)
                
            except:
                continue
                    
    else:
            
        score = None

        while score == None:


            n = randint(0,len(new_userDict))
            m = randint(0,len(new_isbnDict))

            user_number = d_user[n]
            book_number = d_isbn[m]
            
            try:
                user_cluster, book_cluster = convert(user_number,book_number, index_user_cluster, index_book_cluster)

                if R_cluster[book_cluster][user_cluster] == 1:

                    score = utility_DataFrame_cluster[book_cluster][user_cluster]
                    
                if score == None:

                    term1 = utility_DataFrame_cluster[book_cluster]
                    r1 = R_cluster[book_cluster]
                    term1 = term1[r1 ==1]

                    term2 = utility_DataFrame_cluster.loc[user_cluster]
                    r2 = R_cluster.loc[user_cluster]
                    term2 = term2[r2==1]

                    score = (np.mean(term1) + np.mean(term2))/2
                    
            except:
                continue
        try:

            print("The predicted rating (using user-based with clusterization) for book <", 
              books_dataFrame.loc[str(book_number)]["Book-Title"], " > written by <",books_dataFrame.loc[book_number]["Book-Author"] ,"> given by user <", user_number, "> is", np.round(score,3))

        except:

            print(book_number, user_number, score)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

def mainCollaborativeFiltering_CLUSTERING(books_dataFrame, utility_DataFrame,utility_DataFrame_cluster,R_cluster, new_userDict, new_isbnDict,
                                          index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated,
                                          d_user = None, d_isbn = None, score_min = 0, k = 3):
    
    n = -1
    
    d_user = sorted(new_userDict.keys())
    d_isbn = sorted(new_isbnDict.keys())
    
    while n not in [1,2,3]:
    
        print("What method do you want to try?\n")

        print("1 CollaborativeFilteringItemItems using clustering")
        print("2 CollaborativeFilteringItemUsers using clustering")
        print("3 CollaborativeFiltering clustering approach")
        
        try:
            n = int(input())
        except:
            continue
        
    if n == 1:
    
        mainItemItems_clustering(books_dataFrame, utility_DataFrame, utility_DataFrame_cluster,R_cluster,new_userDict, new_isbnDict, d_user, d_isbn,
                      index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated,
                      score_min, k)
    elif n == 2:
    
        mainItemUsers_clustering(books_dataFrame, utility_DataFrame, utility_DataFrame_cluster,R_cluster,new_userDict, new_isbnDict, d_user, d_isbn,
                      index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated,
                      score_min, k)
        
    elif n ==3:
        
        mainClustering(books_dataFrame,utility_DataFrame_cluster,R_cluster, new_userDict, new_isbnDict, d_user, d_isbn,
                  index_user_cluster, index_book_cluster,isbnDict, featuresDict,booksDict,inverted_index,mostRated)

    