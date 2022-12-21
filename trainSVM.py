# this trains the NN model on intents
import json
import pickle
import sklearn.model_selection
from sklearn import svm
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# getting all the tags, and tokenizing and adding all of the words
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        tokeSent = tokenize(pattern)
        all_words.extend(tokeSent)
        xy.append((tokeSent, tag))

# stemming and removing puncuation
ignoreWords = ['?', "!", '.', '.']
all_words = [stem(w) for w in all_words if w not in ignoreWords]
all_words = sorted(set(all_words))
tags = sorted(set(tags))


X_train = []
Y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

#x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X_train, Y_train, test_size=.1)


print(X_train)
svm_model = svm.SVC(kernel='linear', C=8)
svm_model.fit(X_train, Y_train)

y_pred = svm_model.predict(X_train)
acc = sklearn.metrics.accuracy_score(Y_train, y_pred)
print(len(X_train))
for i in range(len(y_pred)):
    print(y_pred[i])
    print(Y_train[i])

data = {
    'model' : svm_model,
    'all_words' : all_words,
    "tags": tags
}

pickle.dump(data, open('modelSVM.sav', 'wb'))
print(acc)
