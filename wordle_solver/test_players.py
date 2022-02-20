"""Test player winning rate."""

import pandas as pd
from lib.game import Game
from lib.player import RandomPlayer

RANDOM_STATE_GAME = 123
RANDOM_STATE_PLAYER = 1234

bag_words_top5000 = pd.read_csv(r"wordle_solver\datasets\5letter_words_top5000.csv")

game = Game(RANDOM_STATE_GAME)
random_player = RandomPlayer(RANDOM_STATE_PLAYER)

def play_multiple_rounds(game, player, bag_words, num_rounds):
    game.set_bag_words(bag_words)
    player.set_bag_words(bag_words)
    game_won_count = 0
    for _ in range(num_rounds):
        game_won_count = game_won_count + game.play(player)
    return game_won_count

game_won_count = play_multiple_rounds(
    game, random_player, bag_words_top5000, 100)

print(game_won_count)
