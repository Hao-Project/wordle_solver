# wordle_solver
An program aiming to solve the Wordle game by reinforcement learning.

Wordle is a word-guessing game that requires player to guess a 5-letter word within 6 attempts. You can play it at https://www.nytimes.com/games/wordle/index.html For more information, check the Wikipedia at https://en.wikipedia.org/wiki/Wordle 

Here is a preview of game 
<img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Wordle_196_example.svg"
     alt="Markdown Monster icon"
     style="margin-right: 10px;" />

### Progress as of 2022/6/7:
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
