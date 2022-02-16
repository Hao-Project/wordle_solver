"""Create the player for a Wordle game."""

from string import ascii_lowercase

class Player:
    """A super class of wordle game player"""
    def __init__(self):
        self.bag_words = None
        return

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        self.bag_words = bag_words

    def gen_guess(self, state):
        """Generate guess to wordle game"""


class RandomPlayer(Player):
    """A player of wordle game that uses randomized strategy"""
    def __init__(self, random_state):
        Player.__init__(self)
        self.random_state = random_state
        self.word_index = {}

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        Player.set_bag_words(self, bag_words)
        self.build_word_index()

    def build_word_index(self):
        set_ascii_lowercase = set(ascii_lowercase)
        for letter in ascii_lowercase:
            for i in range(5):
                for color in ["Green", "Grey", "Yellow"]:
                    self.word_index[(letter, i, color)] = set()
        for index, row in self.bag_words.iterrows():
            letters_in_word = set(row["word"])
            for i in range(5):
                self.word_index[row["word"][i], i, "Green"].add(index)
                for letter in letters_in_word.difference(row["word"][i]):
                    self.word_index[letter, i, "Yellow"].add(index)
                for letter in set_ascii_lowercase.difference(letters_in_word):
                    self.word_index[letter, i, "Grey"].add(index)

    def print_word_index(self, verbose=False):
        if verbose:
            print(self.word_index)
        else:
            for word, indices in self.word_index.items():
                if len(indices) > 0:
                    print(f"{word}: {indices}")

    def gen_guess(self, state):
        "generate a guess"
        new_random_state = self.random_state + state.num_guesses
        guess = (self.bag_words["word"].sample(
            n=1, random_state=new_random_state).values[0])
        return guess
