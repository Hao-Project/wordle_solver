"""The player using reinforcement learning strategy for Wordle."""

from datetime import datetime
from string import ascii_lowercase
import numpy as np
import tensorflow as tf
from tensorflow import keras
from lib.player import Player

class RLStrategyPlayer(Player):
    """Player of Wordle using strategy trained by reinforcement learning"""
    def __init__(
            self, model, input_size, use_fixed_seed=False, random_state=None):
        Player.__init__(self)
        self.model = model
        self.input_size = input_size
        self.previous_guess_indices = []
        self.previous_guess_prob =[]
        self.previous_hints = []
        self.processed_input = [0] * 5
        if use_fixed_seed:
            self.rng = np.random.default_rng(random_state)
        else:
            curr_dt = datetime.now()
            random_state = int(round(curr_dt.timestamp())) + 1
            self.rng = np.random.default_rng(random_state)

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        Player.set_bag_words(self, bag_words)

    def preprocess_input(self, num_previous_guess, verbose=False):
        # one-hot code the number of previous guesses
        for i in range(5):
            self.processed_input[i] = 0
        self.processed_input[num_previous_guess-1] = 1
        # one-hot code the letters of previous guess
        for x in self.bag_words.loc[self.previous_guess_indices[-1], "word"]:
            for letter in ascii_lowercase:
                self.processed_input.append(int(x == letter))
        # one-hot code the previous hint
        for x in self.previous_hints[-1]:
            for token in ["0", "1", "2"]:
                self.processed_input.append(int(x == token))
        if verbose:
            print(self.processed_input)
        return self.processed_input

    def pad(self, x):
        output = x.copy()
        while len(output) < self.input_size:
            output.append(0)
        return output

    def gen_guess(self, state, verbose=False):
        "generate a guess"
        if state.num_guesses == 0:
            guess_index = self.rng.choice(self.bag_words.index, size=1)[0]
        else:
            self.previous_hints.append(state.hints[-1])
            self.preprocess_input(state.num_guesses, verbose)
            tensor = np.array(self.pad(self.processed_input)).reshape(
                (1, self.input_size))
            if verbose:
                print(tensor)
            predicted_prob = self.model.predict(tensor)
            if verbose:
                print(predicted_prob.shape)
                print(predicted_prob[0])
                print(self.bag_words.index.shape[0])
            guess_index = self.rng.choice(
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
        self.processed_input = [0] * 5

    def train(self, state, optimizer, verbose):
        if state.num_guesses <= 3:
            if verbose:
                print(f"lucky with only {state.num_guesses} guess -> not train")
        else:
            answer = state.answer
            num_previous_guess = state.num_guesses - 1
            tensor = np.array(self.pad(self.processed_input)).reshape(
                (1, self.input_size))
            target = self.bag_words.query("word == @answer").index.values
            self.train_with_single_round(
                optimizer, tensor, target, True, verbose)
            while num_previous_guess >= 1:
                # Set coding for the round of the game
                self.processed_input[:5] = [0] * 5
                self.processed_input[num_previous_guess - 1] = 1
                # Drop info after this round of guess
                num_cols_drop = 29 * 5 * (5 - num_previous_guess)
                self.processed_input[5 + num_previous_guess*29*5:] = (
                    [0] * num_cols_drop)
                tensor = np.array(self.pad(self.processed_input)).reshape(
                    (1, self.input_size))
                guess = self.previous_guess_indices[num_previous_guess]
                self.train_with_single_round(
                    optimizer, tensor, guess, state.has_won, verbose)
                num_previous_guess -= 1
        self.reset_status()

    def train_with_single_round(
            self, optimizer, tensorized_input, guess, has_won, verbose):
        if verbose:
            print("Model before training", self.model.trainable_variables)
        loss_object = keras.losses.SparseCategoricalCrossentropy()
        learning_rate = 0.1
        if has_won:
            reward = 1
        else:
            reward = -learning_rate
        with tf.GradientTape() as tape:
            predicted_prob = self.model(tensorized_input)
            loss = tf.reduce_mean(loss_object(guess, predicted_prob)) * reward
        grads = tape.gradient(loss, self.model.trainable_variables)
        if verbose:
            print("Gradient Values:", grads)
        optimizer.apply_gradients(zip(grads,
            self.model.trainable_variables))
        if verbose:
            print("Model after training", self.model.trainable_variables)

    def save_model(self, model_file):
        self.model.save(model_file)

    def print(self):
        print(self.__dict__)
