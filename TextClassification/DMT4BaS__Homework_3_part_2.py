import os
import csv
import numpy as np
from nltk import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import SGDClassifier
import pprint as pp

np.random.seed(123)

stemmer = EnglishStemmer()


def stemming_tokenizer(text):
    stemmed_text = [stemmer.stem(word) for word in word_tokenize(text, language="english")]
    return stemmed_text


def extract_data(first_dir, second_dir):

    data = all_files(first_dir, 1) + all_files(second_dir, 0)

    X = np.array([d[0] for d in data])
    Y = np.array([d[1] for d in data])

    population = list(range(X.shape[0]))

    for _ in range(10):
        np.random.shuffle(population)

    X = X[population]
    Y = Y[population]

    return X, Y


def all_files(d, num):

    data = []

    files = os.listdir(d)

    for file in files:
        PATH = d + file
        f = open(PATH, "r")
        s = f.read()

        data.append([s, num])

    return data


train_pos_dir = "./Positve_negative_sentences/Positve_negative_sentences/Training/Positive/"
train_neg_dir = "./Positve_negative_sentences/Positve_negative_sentences/Training/negative/"

test_pos_dir = "./Positve_negative_sentences/Positve_negative_sentences/Test/Positive/"
test_neg_dir = "./Positve_negative_sentences/Positve_negative_sentences/Test/negative/"

x_train, y_train = extract_data(train_pos_dir, train_neg_dir)
x_test, y_test = extract_data(test_pos_dir, test_neg_dir)

#####################################################################################################################

ext_tfidf = TfidfVectorizer()

svm_rbf = {"svm_rbf__C": [0.1, 0.5, 1, 5, 10, 50, 100], "svm_rbf__gamma": [0.1, 0.5, 1, 3, 6, 10]}
sgd = {"sgd__penalty": ["l1", "l2"], "sgd__alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10]}
neigh = {"neigh__n_neighbors": [1, 3, 5, 7, 9, 11], "neigh__leaf_size": [2, 3]}

classifiers = {"svm_rbf": svm.SVC(kernel="rbf"), "sgd": SGDClassifier(loss="hinge"), "neigh": KNeighborsClassifier()}

parameters = {"svm_rbf": svm_rbf, "sgd": sgd, "neigh": neigh}


# answers

ntrain = len(y_train)
ntrainH = sum(y_train)
ntest = len(y_test)
ntestH = sum(y_test)
print("TRAIN:", ntrain)
print("Positive", ntrainH)
print("Negative", ntrain - ntrainH)
print("")
print("TEST:", ntest)
print("Positive", ntestH)
print("Negative", ntest - ntestH)


def routine(X, Y, s, classifiers, parameters):

    pipeline = Pipeline([("tfidf", ext_tfidf), (s, classifiers[s])])

    par = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__tokenizer": [None, stemming_tokenizer],
        "tfidf__stop_words": [None, "english"],
    }

    par.update(parameters[s])

    grid_search = GridSearchCV(
        pipeline, par, scoring=metrics.make_scorer(metrics.matthews_corrcoef), cv=10, n_jobs=-1, verbose=1
    )

    grid_search.fit(X, Y)

    ## Print results for each combination of parameters.
    # number_of_candidates = len(grid_search.cv_results_['params'])
    # print("Results:")
    # for i in range(number_of_candidates):
    #    print(i, 'params - %s; mean - %0.3f; std - %0.3f' %
    #          (grid_search.cv_results_['params'][i],
    #           grid_search.cv_results_['mean_test_score'][i],
    #           grid_search.cv_results_['std_test_score'][i]))
    print("")
    print("PARAMETERS ----------------------------------------------")
    pp.pprint(par)
    print("")

    print("Best Parameters -----------------------------------------")
    pp.pprint(grid_search.best_params_)
    print("")

    y_predicted = grid_search.predict(x_test)

    # Evaluate the performance of the classifier on the original Test-Set
    output_classification_report = metrics.classification_report(y_test, y_predicted)
    print("")
    print("---------------------------------------------------------")
    print(output_classification_report)
    print("---------------------------------------------------------")
    print("")

    # Compute the confusion matrix
    confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)
    print("")
    print("Confusion Matrix: True-Classes X Predicted-Classes-------")
    print(confusion_matrix)
    print("")

    print("")
    print("---------------------------------------------------------")
    print("Normalized-accuracy value:", metrics.accuracy_score(y_test, y_predicted))
    print("")

    print("")
    print("---------------------------------------------------------")
    print("Matthews-correlation-coefficient value:", metrics.matthews_corrcoef(y_test, y_predicted))
    print("")
    return [grid_search.best_params_, grid_search.best_score_]


d = {}

for clas in classifiers:
    print(classifiers[clas])
    d[clas] = routine(x_train, y_train, clas, classifiers, parameters)

print(d)
