"""Test player winning rate."""

import pandas as pd
from lib.game import Game
from lib.random_strategy_player import RandomStrategyPlayer

DATA_PATH = r"wordle_solver\datasets\words"
SUMMARY_PATH = r"wordle_solver\summary"

RANDOM_STATE_GAME = 123
RANDOM_STATE_PLAYER = 1234

LABEL_TO_DATA = {
    "Top 100 Words": r"\5letter_words_top100.csv",
    "Top 1000 Words": r"\5letter_words_top1000.csv",
    "Top 5000 Words": r"\5letter_words_top5000.csv",
    "All Words": r"\5letter_words.csv",
}
TESTING_ROUNDS = [10, 100, 1000, 10000]

def play_multiple_rounds(game, player, bag_words, num_rounds):
    game.set_bag_words(bag_words)
    player.set_bag_words(bag_words)
    game_won_count = 0
    for _ in range(num_rounds):
        game_won_count = game_won_count + game.play(player)
    return game_won_count

def main():
    word_bags = {}
    for key, data in LABEL_TO_DATA.items():
        word_bags[key] = pd.read_csv(DATA_PATH + data)

    game = Game(RANDOM_STATE_GAME)
    random_player = RandomStrategyPlayer(True, RANDOM_STATE_PLAYER, 0.01)

    win_rates = {}
    for key, bag_words in word_bags.items():
        win_rates[key] = []
        for num_rounds in TESTING_ROUNDS:
            win_rate = play_multiple_rounds(
                game, random_player, bag_words, num_rounds) / num_rounds
            win_rates[key].append(win_rate)

    df_win_rates = (
        pd.DataFrame(win_rates, TESTING_ROUNDS)
        .rename_axis(index="Num of Rounds", columns="Win Rates"))
    print(df_win_rates)
    df_win_rates.to_csv(SUMMARY_PATH + r"\random_strategy_win_rates.csv")

if __name__ == "__main__":
    main()
