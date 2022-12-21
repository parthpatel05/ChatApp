import pickle
import sklearn
import json
from nltk_utils import bag_of_words, tokenize
import random

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

loaded_model = pickle.load(open('modelSVM.sav', 'rb'))
svm_model = loaded_model['model']
all_words = loaded_model['all_words']
tags = loaded_model['tags']

def getResponse(sentence):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])

    predicted = svm_model.predict(X)
    tag = tags[predicted.item()]
    print(tag)
    for intent in intents['intents']:
        if tag == intent["tag"]:
            print(f"-: {random.choice(intent['responses'])}")
            return random.choice(intent['responses'])

#getResponse("what do you take")
