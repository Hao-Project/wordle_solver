"""Test player winning rate."""

import pandas as pd
from lib.game import Game
from lib.player import RandomPlayer

RANDOM_STATE_GAME = 123
RANDOM_STATE_PLAYER = 1234

bag_words = pd.read_csv(r"wordle_solver\datasets\5letter_words_top5000.csv")

game = Game(RANDOM_STATE_GAME)
game.set_bag_words(bag_words)
random_player = RandomPlayer(RANDOM_STATE_PLAYER)
random_player.set_bag_words(bag_words)

game_won_count = 0
for _ in range(100):
    game_won_count = game_won_count + game.play(random_player)

print(game_won_count)
