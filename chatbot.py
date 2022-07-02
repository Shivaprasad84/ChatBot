
from curses import ERR
from distutils.log import ERROR
import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

with open('intents.json', 'r') as file:
    data = json.load(file)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')

def clean_up_sentence(sentence):
    sentence_words = nltk.tokenize.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print('enter quit to exit')
while True:
    message = input("You: ")
    if message == 'quit':
        break
    ints = predict_class(message)
    res = get_response(ints, data)
    print(f"Bot: {res}")
