# TicTacToeAI
ML program that learns how to play Tic-tac-toe really well.

A fully trained AI is saved in the file model.json. You can load this file and play against it with 'python3 TicTacToeAI.py'. You play the game by using the number pad on your keyboard. They nine squares of tic-tac-toe are mapped to the numbers on the number pad as follows:

7 | 8 | 9
----------
4 | 5 | 6
----------
1 | 2 | 3

You can re-train the AI with 'python3 TicTacToeAI.py --train'

The AI uses a dictionary to learn how to play. Each key in the dictionary is a state of the game and the value is the choice that the AI makes. Initially, the dictionary is empty, and the AI just makes random choices. If it wins the game, then it remembers the choices that it made, but if it loses, then it forgets those choices.

Each state of the game consists of 9 numbers representing the status of the 9 squares in tic-tac-toe. They can each take 3 values: 1, 2, or 3. The value 1 means the square is empty. The value 2 means player1 has a mark there, and the value 3 means player2 has a mark there. The final number is a number between 0 and 8 that represents the location where the AI should place its next mark. The square that the AI actually chooses is the value plus one.

For example, a key,value pair in the dictionary could be:
"111111111":4
This means that if all the squares are blank, the AI should take the center square.
