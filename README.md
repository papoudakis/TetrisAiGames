# TetrisAiGames

This is a Bot in python for Tetris. It was created for [theaigames](http://theaigames.com/competitions/ai-block-battle).
There are two implementations, the Heuristic and the Qlearning.

#Heuristic Implementation
In this implementation we compute feature and evaluate the best move based on a linear evaluation function. The weights of this function compute with tuning

# QLearning Implementation
Similar to heuristic implementation. The only difference is that we compute the weights of evaluation function using qlearning.

**To run qlearning locally**

-cd blockbattle-engine/

-create an empty file named weigths.txt

-python run_matches.py  
