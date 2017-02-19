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

def genericContentBasedUserItems(user_number, userDict, isbnDict, featuresDict,users,books, t=7):
    
    v = []

    for key in userDict[user_number]:

        if int(userDict[user_number][key]) > t:

            v.append(key)

    # select users that have rated books rated by initial user        

    w = []

    for isbn in v:
        for key in  isbnDict[isbn]:

            if int(isbnDict[isbn][key]) > 8 and (key != user_number):

                w.append(key)    

    w = list(set(w))


    # books rated by users that have rated the book(s) rated by initial user

    z = []

    for user in w:

        for isbn in userDict[user]:

            if int(userDict[user][isbn]) > 9:

                z.append(isbn)

    z = list(set(z)) 

    if len(z) > 700:

        z = z[:700]  

    X_myUser = np.zeros(len(featuresDict))

    # others users
    X_items = np.zeros((len(z),len(featuresDict)))


    for feature in users[user_number]:

        X_myUser[featuresDict[feature]] = users[user_number][feature]


    for j in range(len(z)):

        try:
            for feature in books[z[j]]:


                X_items[j][featuresDict[feature]] = books[z[j]][feature]

        except:
            continue

    num = (X_myUser*X_items).sum(axis=1)

    d_myUser = np.sqrt((X_myUser**2).sum())
    d_items = np.sqrt((X_items**2).sum(axis=1))

    res = num/(d_myUser*d_items)
   
    f = sorted(zip(z,res), key=lambda tup: tup[1], reverse=True)

    f1 = []

    for tu in f:

        if tu[1] != 0.0 and not np.isnan(tu[1]):

            f1.append(tu)

    f1 = sorted(f1, key=lambda tup: tup[1], reverse=True)

    recommendation = {user_number: [tu[0] for tu in f1[:10]]}
    
    return recommendation


def genericContentBasedUserUsers(user_number, userDict, isbnDict, featuresDict,users,books,t=7):

    v = []

    for key in userDict[user_number]:

        if int(userDict[user_number][key]) > t:

            v.append(key)

    # select users that have rated books rated by initial user        

    w = []

    for isbn in v:
        for key in  isbnDict[isbn]:

            if int(isbnDict[isbn][key]) > 8 and (key != user_number):

                w.append(key)    

    w = list(set(w))

    if len(w) > 700:

        w = w[:700]

    X_myUser = np.zeros(len(featuresDict))

    # others users
    X_otherUsers = np.zeros((len(w),len(featuresDict)))


    for feature in users[user_number]:

        X_myUser[featuresDict[feature]] = users[user_number][feature]


    for j in range(len(w)):

        try:
            for feature in users[w[j]]:

                X_otherUsers[j][featuresDict[feature]] = users[w[j]][feature]
        except:
            continue

    num = (X_myUser*X_otherUsers).sum(axis=1)

    d_myUser = np.sqrt((X_myUser**2).sum())
    d_otherUsers = np.sqrt((X_otherUsers**2).sum(axis=1))

    res = num/(d_myUser*d_otherUsers)
    

    f = sorted(zip(w,res), key=lambda tup: tup[1], reverse=True)

    Rated = userDict[user_number]

    recommendation = {user_number: []}

    for tup in f:

        for book in userDict[tup[0]]:

            if int(userDict[tup[0]][book]) > 8 and book not in Rated and book not in  recommendation[user_number]:

                recommendation[user_number].append(book)

            if len(recommendation[user_number]) > 10:

                break

        if len(recommendation[user_number]) > 10:

                break
                
    return recommendation
            


def userRecommendations(user_number,books_dataFrame, recommendation):
    
    for isbn in recommendation[user_number]:

        try:
            print("<",books_dataFrame.loc[isbn]["Book-Title"],"> written by <",books_dataFrame.loc[isbn]["Book-Author"],">")
        except:
            continue
            
    return None

def userRatings(user_number, userDict,books_dataFrame):

    for isbn in userDict[user_number]:

        try:
            if  int(userDict[user_number][isbn]) > 8:
                print("<",books_dataFrame.loc[isbn]["Book-Title"],"> written by <",books_dataFrame.loc[isbn]["Book-Author"],">")
        except:
            continue
            
    return None


def chooseUser(userDict, d_user):
    
    print("Please choose a user\n")
    print("user or random user: \n")
    user_number = input()
    if user_number == "":
        user_number = None
    if user_number == None:
        n = randint(0,len(userDict))
        user_number = d_user[n]
        return user_number
    else:
        return user_number


def mainContentBased(featuresDict,userDict,isbnDict,users,books,d_user,d_isbn,books_dataFrame,mostRated,t):
    
    r = -1
    while r not in [1,2]:
        
        print("\nPlease select a recommender system:\n")
        print("1 Content Based user-items\n")
        print("2 Content Based user-users\n")
        try:
            r = int(input())
        except:
            continue
    
    if r == 1:

        user_number = chooseUser(userDict,d_user)
        print("Please wait...")
        recommendation = genericContentBasedUserItems(user_number, userDict, isbnDict, featuresDict,users,books)
        if recommendation[user_number] == []:
            print("We don't have a recommendation for user <",user_number,">. We can only recommend the most popular and well rated books in the database:\n")
            for i in mostRated:
                print("<",books_dataFrame["Book-Title"][i[0]],"> written by <",books_dataFrame["Book-Author"][i[0]],">")
            return user_number,mostRated
            return None
        print("For user <",user_number,"> we recommend using a content based approach:\n")
        userRecommendations(user_number,books_dataFrame, recommendation)
        return user_number,recommendation

    elif r == 2:
        
        user_number = chooseUser(userDict,d_user)
        print("Please wait...")
        recommendation = genericContentBasedUserUsers(user_number, userDict, isbnDict, featuresDict,users,books)
        if recommendation[user_number] == []:
            print("We don't have a recommendation for user <",user_number,">. We can only recommend the most popular and well rated books in the database:\n")
            for i in mostRated:
                print("<",books_dataFrame["Book-Title"][i[0]], "> written by <",books_dataFrame["Book-Author"][i[0]],">")
            return user_number,mostRated
            return None
        print("For user <",user_number,"> we recommend using a content based approach:\n")
        userRecommendations(user_number,books_dataFrame, recommendation)
        return user_number,recommendation


def buy(recommendation,mostRated,books_dataFrame):
    
    r = -1
    while r not in ["y","n"]:
        print("\nDo you want to see one of this books?")
        print("y")
        print("n\n")
        r = input()

    if r == "y":
    
        if recommendation == mostRated:
            mostRatedDict = {k:i[0] for k,i in enumerate(mostRated)}
            print("What do you prefer?\n")
            r = -1
            while r not in list(mostRatedDict.keys()):
                for m in mostRatedDict:
                    print(m, "<",books_dataFrame["Book-Title"][mostRatedDict[m]], "> written by <", books_dataFrame["Book-Author"][mostRatedDict[m]],">")
                r = int(input())  
            isbn = mostRatedDict[r]
            url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
            webbrowser.open(url+isbn)
        else:
            recDict = {k:v for k,v in enumerate(list(recommendation.values())[0])}
            print("What do you prefer?\n")
            r = -1
            while r not in list(recDict.keys()):
                for m in recDict:
                    print(m, "<",books_dataFrame["Book-Title"][recDict[m]], "> written by <", books_dataFrame["Book-Author"][recDict[m]],">")
                r = int(input())  
            isbn = recDict[r]
            url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
            webbrowser.open(url+isbn)
        return None
    else:
        return None
        
    