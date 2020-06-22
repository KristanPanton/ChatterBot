import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tensorflow as tf
import random
import json
import pickle
import sys

stemmer = LancasterStemmer()

json_filename = "intents.json"
pickle_filename = "data.pickle"
try:
    with open(json_filename) as f:
        data = json.load(f)

except IOError:
    print(f"'{json_filename}' doesn't exist.")
    sys.exit()

try:
    chatbot_model = tf.keras.models.load_model("models/chatbot_model")

    with open(pickle_filename, "rb") as f:
        words, labels, training, output = pickle.load(f)

except ImportError or IOError:
    print(f"Model doesn't exist. Creating model now...")

    try:
        with open(pickle_filename, "rb") as f:
            words, labels, training, output = pickle.load(f)

    except IOError:
        print(f"'{pickle_filename}' doesn't exist. It will be created.")
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                wrds = [stemmer.stem(w.lower()) for w in wrds if w != "?"]
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = sorted(list(set(words)))
        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []

            for w in words:
                if w in doc:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

        print(pickle_filename, "created.")

        chatbot_model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_shape=[len(training[0]), ], activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(output[0]), activation="softmax")
        ])
        chatbot_model.compile(optimizer='adam',
                              loss="categorical_crossentropy",
                              metrics=['accuracy'])
        chatbot_model.fit(training, output, epochs=1000, verbose=2)
        chatbot_model.save("models/chatbot_model")


def _bag_of_words(s, _words):
    b_o_w = [0 for _ in range(len(_words))]
    stemmed_words = nltk.word_tokenize(s)
    stemmed_words = [stemmer.stem(word.lower()) for word in stemmed_words]

    for stemmed_word in stemmed_words:
        for i, word in enumerate(_words):
            if word == stemmed_word:
                b_o_w[i] = 1

    return b_o_w


def get_response(s):
    results = chatbot_model.predict([_bag_of_words(s, words)])
    print(results)
    tag_index = np.argmax(results)
    if results[0][tag_index] < 0.7:
        return "I do not understand your question. Please rephrase it."

    tag = labels[tag_index]
    for tg in data["intents"]:
        if tg["tag"] == tag:
            return random.choice(tg["responses"])

    print("An error has occurred.")


def test_chat():
    print("Start talking with the bot (type quit to stop):")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        print(get_response(inp))


if __name__ == "__main__":
    test_chat()
