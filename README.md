# wordle_solver
An automated program to solve the Wordle game.

As of 2022/6/7:
Done:
- Wordle game and abstract game solver
- Game solver using randomized strategy: randomly guess a word from possible words
- Performance of randomized strategy as benchmark
- Set up of reinforcement learning game solver, with method generating guess and train model

To Do:
- Solve challenge of reinforcement learning converging to guessing only in same groups of words

To Test:
- Are there a vanishing gradient issue? Try add clip value?
- Use different models (maybe share early layers) for guesses at different rounds?
- Only use reinforcement learning for later rounds (round >= 4?)

Things have learned
- Should not train on fluke wins
- Strategy at earlier round should be different from the strategy at the last round. The last round only needs to guess the word that is most likely to be the answer, but the early rounds need to explore to get more hints.
- It's hard to learn how to guess earlier rounds when the model has not learned how to guess at later rounds.
- Let machine learn embedding of word may be requiring too much data.
- Simply reducing learning rate or changing reward function not solving early converging issue.
