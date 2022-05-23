"""The player using reinforcement learning strategy for Wordle."""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from lib.player import Player

class RLStrategyPlayer(Player):
    """Player of Wordle using strategy trained by reinforcement learning"""
    def __init__(self, random_state, model, num_oov_buckets):
        Player.__init__(self)
        self.random_state = random_state
        self.model = model
        self.num_oov_buckets = num_oov_buckets
        self.previous_guess_indices = []
        self.previous_guess_prob =[]
        self.previous_hints = []
        self.processed_input = []
        self.hint_to_index = {"0": 1, "1": 2, "2": 3}

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        Player.set_bag_words(self, bag_words)

    def preprocess_input(self, verbose=False):
        self.processed_input.append(
            self.previous_guess_indices[-1] + self.num_oov_buckets)
        for x in self.previous_hints[-1]:
            self.processed_input.append(self.hint_to_index[x])
        if verbose:
            print(self.processed_input)
        return self.processed_input

    def pad(self, x):
        output = x.copy()
        while len(output) < 30:
            output.append(0)
        return output

    def gen_guess(self, state, verbose=False):
        "generate a guess"
        if state.num_guesses == 0:
            guess_index = (self.bag_words.sample(
                n=1, random_state=self.random_state).index[0])
        else:
            self.previous_hints.append(state.hints[-1])
            self.preprocess_input(verbose)
            tensor = np.array(self.pad(self.processed_input)).reshape((1,30))
            if verbose:
                print(tensor)
            predicted_prob = self.model.predict(tensor)
            if verbose:
                print(predicted_prob.shape)
                print(predicted_prob[0])
                print(self.bag_words.index.shape[0])
            guess_index = np.random.choice(
                self.bag_words.index, size=1, p=predicted_prob[0])[0]
            if verbose:
                print(guess_index)
            self.previous_guess_prob.append(predicted_prob[0][guess_index])
        guess = self.bag_words.loc[guess_index, "word"]
        self.previous_guess_indices.append(guess_index)
        return guess

    def reset_status(self):
        self.previous_guess_indices = []
        self.previous_guess_prob =[]
        self.previous_hints = []
        self.processed_input = []

    def train(self, state, optimizer, verbose):
        answer = state.answer
        target = self.bag_words.query("word == @answer").index.values
        if verbose:
            print(target)
        loss_object = keras.losses.SparseCategoricalCrossentropy()
        tensor = np.array(self.pad(self.processed_input)).reshape((1,30))
        with tf.GradientTape() as tape:
            predicted_prob = self.model(tensor)
            loss = tf.reduce_mean(loss_object(target, predicted_prob))
        grads = tape.gradient(loss, self.model.trainable_variables)
        if verbose:
            print(grads)
        optimizer.apply_gradients(zip(grads,
            self.model.trainable_variables))
        self.reset_status()

    def save_model(self, model_file):
        self.model.save(model_file)

    def print(self):
        print(self.__dict__)
