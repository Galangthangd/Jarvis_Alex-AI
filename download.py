import utils
import config
import json
import nltk

from model.model_training import TrainingModel

#f = open('datachat'+self.os+'.json', encoding='utf-8')
f = open('datachatAlex.json', encoding='utf-8')
data = json.load(f)
words = []
classes = ['Chat']
data_x = []
data_y = []
for group in data['intents'][0]['response']:
    tokens = nltk.word_tokenize(group['questions'])
    words.extend(tokens)
    data_x.append(group['questions'])
    data_y.append('Chat')
words = sorted(set(words))
classes = sorted(set(classes))
training_model = TrainingModel(words, classes, data_x, data_y)
trained_model = training_model.train()

while True:
    command = input('user : ')
    Answers = TrainingModel.get_answers_type(command, data, 'response','answers')
    print('alex : '+Answers)
    utils.speak(Answers)
