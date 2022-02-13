"""Create a bag of 5-letter words used by Wordle game."""
import pandas as pd

df = pd.read_csv(r"wordle_solver\datasets\unigram_freq.csv")

df_5letter = df[df["word"].str.len() == 5]

df_5letter["likelihood"] = df_5letter["count"] / df_5letter["count"].sum()

df_5letter[["word", "likelihood"]].to_csv(
    r"wordle_solver\datasets\5letter_words.csv", index=False)

df_5letter_top5000 = df_5letter.head(5000)
df_5letter_top5000["likelihood"] = (
    df_5letter_top5000["count"] / df_5letter_top5000["count"].sum())

df_5letter_top5000[["word", "likelihood"]].to_csv(
    r"wordle_solver\datasets\5letter_words_top5000.csv", index=False)
