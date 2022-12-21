chat.data - the saved NN model from train.py
chat.py - evaluates the NN model with input and returns output, could be imported by GUI
chat.txt - chat log
chatSVM.py - evaluates SVM model, could be imported by GUI
data.pth - the saved NN model from train.py
GUI.py - the GUI for everything
i2.json -
intents.json - data for train.py and NN model
intents2.json -
main.py - terminal version of GUI
main2.py - terminal version of GUI
model.py - NN model
modelSVM.sav - saved SVM model
my.kv - kivy file for GUI
nltk_utils.py - helper functions for nltk, bag of words and tokenize
t.py - rn GUI.py to test as other user
train.py - trains the NN model on intents.json and saves to data.pth
trainSVM.py - trains SVM on intents.json and saves in modelSVM.sav


in dialogsdata
analyzer.py
dialogs.txt - data for dialogs model
train_dialogs.py - trains on dialogs.py on SVM -
train_dialogsNN.py - trains dialogs.py on NN
chatDialogs.py - evaluates svm with dialogs data, imported by GUI
chatDialogsNN.py - evaluates NN with dialogs data, imported by GUI
dataDialogs.pth - the save NN model from train_dialogs.py
modelSVMdia.sav - svm model with diaalogs data

