"""Create the player for a Wordle game."""


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

    def gen_guess(self, state):
        "generate a guess"
        new_random_state = self.random_state + state.num_guesses
        guess = (self.bag_words["word"].sample(
            n=1, random_state=new_random_state).values[0])
        return guess
