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
import pprint as pp

np.random.seed(123)

stemmer = EnglishStemmer()


def stemming_tokenizer(text):
    stemmed_text = [stemmer.stem(word) for word in word_tokenize(text, language="english")]
    return stemmed_text


# ham(1) spam(0)
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


train_ham_dir = "./Ham_Spam_comments/Ham_Spam_comments/Training/Ham/"
train_spam_dir = "./Ham_Spam_comments/Ham_Spam_comments/Training/Spam/"

test_ham_dir = "./Ham_Spam_comments/Ham_Spam_comments/Test/Ham/"
test_spam_dir = "./Ham_Spam_comments/Ham_Spam_comments/Test/Spam/"

x_train, y_train = extract_data(train_ham_dir, train_spam_dir)
x_test, y_test = extract_data(test_ham_dir, test_spam_dir)

ext_tfidf = TfidfVectorizer()
neigh = KNeighborsClassifier()


pipeline = Pipeline([("tfidf", ext_tfidf), ("neigh", neigh)])

par = {
    "tfidf__ngram_range": [(1, 1), (1, 2)],
    "tfidf__tokenizer": [None, stemming_tokenizer],
    "tfidf__stop_words": [None, "english"],
    "neigh__n_neighbors": [1, 3, 5, 7, 9, 11],
    "neigh__leaf_size": [2, 3],
}

grid_search = GridSearchCV(
    pipeline, par, scoring=metrics.make_scorer(metrics.matthews_corrcoef), cv=10, n_jobs=-1, verbose=1
)

grid_search.fit(x_train, y_train)

## Print results for each combination of parameters.
number_of_candidates = len(grid_search.cv_results_["params"])
print("Results:")
for i in range(number_of_candidates):
    print(
        i,
        "params - %s; mean - %0.3f; std - %0.3f"
        % (
            grid_search.cv_results_["params"][i],
            grid_search.cv_results_["mean_test_score"][i],
            grid_search.cv_results_["std_test_score"][i],
        ),
    )

print("")

# answers

ntrain = len(y_train)
ntrainH = sum(y_train)
ntest = len(y_test)
ntestH = sum(y_test)
print("TRAIN ---------------------------------------------------")
print("Ham", ntrainH)
print("Spam", ntrain - ntrainH)
print("")
print("TEST ----------------------------------------------------")
print("Ham", ntestH)
print("Spam", ntest - ntestH)

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
