"""Create and play a Wordle game."""

from string import ascii_lowercase


class Game:
    """A wordle game"""
    def __init__(self, random_state):
        self.total_round_guess = 6
        self.random_state = random_state
        self.bag_words = None
        self.game_state = None
        self.count_game_played = 0

    def set_bag_words(self, bag_words):
        """Set words used by the game"""
        self.bag_words = bag_words

    def set_game_answer(self):
        """Set an answer to a round of game"""
        new_random_state = self.random_state + self.count_game_played
        word = (self.bag_words["word"].sample(
            n=1, random_state=new_random_state).values[0])
        return word

    def play(self, player, verbose=False):
        """Play one round of game"""
        self.game_state = GameState(self.set_game_answer())
        for _ in range(self.total_round_guess):
            guess = player.gen_guess(self.game_state)
            self.game_state.update(guess)
            if verbose:
                self.game_state.print()
            if self.game_state.has_won:
                self.count_game_played += 1
                return self.game_state.has_won
        self.game_state.is_game_ongoing = False
        self.game_state.has_won = False
        if verbose:
            self.game_state.print()
        self.count_game_played += 1
        return self.game_state.has_won


class GameState:
    """The state of a Wordle game."""
    def __init__(self, answer):
        self.answer = answer
        self.num_guesses = 0
        self.guesses = []
        self.hints = []
        self.letter_to_count = {}
        for letter in ascii_lowercase:
            self.letter_to_count[letter] = 0
        for letter in self.answer:
            self.letter_to_count[letter] += 1
        self.is_game_ongoing = True
        self.has_won = None

    def get_game_status(self):
        """Return game status"""
        return self.is_game_ongoing

    def update(self, new_guess):
        """Update game status after getting a new guess."""
        self.num_guesses += 1
        self.guesses.append(new_guess)
        new_hint_list = [""] * 5
        letter_to_count_use = {}
        for letter in ascii_lowercase:
            letter_to_count_use[letter] = 0
        for i in range(5):
            if new_guess[i] == self.answer[i]:
                new_hint_list[i] = "2"
                letter_to_count_use[new_guess[i]] += 1
        for i in range(5):
            if new_hint_list[i] != "2":
                if (letter_to_count_use[new_guess[i]] <
                        self.letter_to_count[new_guess[i]]):
                    letter_to_count_use[new_guess[i]] += 1
                    new_hint_list[i] = "1"
                else:
                    new_hint_list[i] = "0"
        new_hint = "".join(new_hint_list)
        self.hints.append(new_hint)
        if new_hint == "22222":
            self.is_game_ongoing = False
            self.has_won = True

    def print(self, print_all=False):
        """Print game status."""
        message = (
            f"Correct answer: {self.answer}, "
            f"# of guesses: {self.num_guesses}, guesses: {self.guesses},\n"
            f"Hints: {self.hints},\n"
            f"game ongoing: {self.is_game_ongoing}, "
            f"game won: {self.has_won}\n"
        )
        if print_all:
            message += f"letter count: {self.letter_to_count}"
        print(message)
