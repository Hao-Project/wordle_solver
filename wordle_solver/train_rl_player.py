"""Train player with reinforcement learning strategy"""

import sys
from datetime import datetime
from configparser import ConfigParser
import pandas as pd
from tensorflow import keras
from lib.game import Game
from lib.rl_strategy_player import RLStrategyPlayer

DATA_PATH = r"wordle_solver\datasets\words"
SUMMARY_PATH = r"wordle_solver\summary"

NUM_OOV_BUCKETS = 4 # Used in construct reinforcement learning player

def main(config_file=r"wordle_solver\train_rl_setup.ini"):
    start_time = datetime.now()
    time_stamp = start_time.strftime("%Y%m%d_%H%M%S")
    log_file = r"wordle_solver\log\train_rl_player_{0}.log".format(time_stamp)
    log = open(log_file, "a")
    # sys.stdout = log

    config = ConfigParser()
    config.read(config_file)
    bag_word = pd.read_csv(config["common"]["path_bag_words"])
    random_state_game = int(config["common"]["random_state_game"])
    random_state_player = int(config["common"]["random_state_player"])
    num_training_rounds = int(config["common"]["num_training_rounds"])
    game_play_verbose = bool(config["common"]["game_play_verbose"])

    if config["common"]["mode"] == "new":
        embed_size = 20
        num_words = bag_word.shape[0]
        model = keras.models.Sequential([
            keras.layers.Embedding(
                num_words + NUM_OOV_BUCKETS, embed_size, input_shape=[30,],
                mask_zero=True),
            keras.layers.GRU(128),
            keras.layers.Dense(50),
            keras.layers.Dense(num_words, activation="softmax")
        ])
    else:
        model = keras.models.load_model(config["model"]["model_in"])

    game = Game(True, random_state_game)
    rl_player = RLStrategyPlayer(random_state_player, model, NUM_OOV_BUCKETS)
    adam_optimizer = keras.optimizers.Adam(lr=0.01)
    game.set_bag_words(bag_word)
    rl_player.set_bag_words(bag_word)

    for _ in range(num_training_rounds):
        game.play(rl_player, verbose=game_play_verbose)
        rl_player.train(game.game_state, adam_optimizer)
    rl_player.save_model(config["model"]["model_out"])

    end_time = datetime.now()
    sys.stdout = log
    print("Training Time: {}".format(end_time - start_time))
    log.close()

if __name__ == "__main__":
    main(*sys.argv[1:])