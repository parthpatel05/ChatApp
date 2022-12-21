# this trains the NN model
import json
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
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

print(X_train)
X_train = np.array(X_train)
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


# Parameters
batch_size = 8
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
learning_rate = .001
num_epochs = 1000

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.type(torch.LongTensor)
        labels = labels.to(device)

        # forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backprop and optim
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch +1 )% 100 ==0:
        print(f'epoch {epoch+1} / {num_epochs}  loss= {loss.item():.4f}')


print(f'final loss= {loss.item():.4f}')

data = {
    'model_state': model.state_dict(),
    "input_size": input_size,
    "hidden_size":hidden_size,
    'output_size':output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = 'data.pth'
torch.save(data, FILE)

