"""Test player winning rate."""

import sys
from datetime import datetime
from configparser import ConfigParser
import pandas as pd
from tensorflow import keras
from lib.game import Game
from lib.rl_strategy_player import RLStrategyPlayer

DATA_PATH = r"wordle_solver\datasets\words"
SUMMARY_PATH = r"wordle_solver\summary"

# Model needs to guess at round 2-6. For each round, using one-hot coding,the
# input includes 5 columns for the round number, 26 * 5 columns for the
# previous guess (26 columns for each letter), and 3 * 5 columns for previous
# hints. So the maximum input size is (5 + 26*5 + 3*5) * 5 = 750
INPUT_SIZE = 750

def main(config_file=r"wordle_solver\test_rl_setup.ini"):
    start_time = datetime.now()
    time_stamp = start_time.strftime("%Y%m%d_%H%M%S")
    log_file = r"wordle_solver\log\test_rl_player_{0}.log".format(time_stamp)
    log = open(log_file, "a")
    sys.stdout = log

    config = ConfigParser()
    config.read(config_file)

    bag_word = pd.read_csv(config["common"]["path_bag_words"])
    num_testing_rounds = config.getint("common", "num_testing_rounds")
    game_play_verbose = config.getboolean("common", "game_play_verbose")
    game_seed_fixed = config.getboolean("common", "game_seed_fixed")
    random_state_game = config.getint("common", "random_state_game")
    player_seed_fixed = config.getboolean("common", "player_seed_fixed")
    random_state_player = config.getint("common", "random_state_player")

    model_path = config["common"]["model"]

    model = keras.models.load_model(model_path)

    game = Game(game_seed_fixed, random_state_game)
    rl_player = RLStrategyPlayer(
        model, INPUT_SIZE, player_seed_fixed,
        random_state_player)
    game.set_bag_words(bag_word)
    rl_player.set_bag_words(bag_word)
    game_won_count = 0
    for _ in range(num_testing_rounds):
        game_won_count += game.play(rl_player, game_play_verbose)
        rl_player.reset_status()
    game_won_ratio = game_won_count / num_testing_rounds

    print(f"Tested model: {model_path}")
    testing_message = (
        f"Played {num_testing_rounds} rounds, Won {game_won_count} Rounds, "
        f"Win Ratio = {game_won_ratio}")
    print(testing_message)
    end_time = datetime.now()
    print("Testing Time: {}".format(end_time - start_time))
    log.close()

if __name__ == "__main__":
    main(*sys.argv[1:])
