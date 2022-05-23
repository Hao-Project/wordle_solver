"""Create the player for a Wordle game."""

class Player:
    """A super class of wordle game player"""
    def __init__(self):
        self.bag_words = None
        return

    def set_bag_words(self, bag_words):
        """Set dictionary used by the player"""
        self.bag_words = bag_words

    def gen_guess(self, state, verbose=False):
        """Generate guess to wordle game"""
