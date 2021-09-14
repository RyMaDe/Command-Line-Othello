# Command Line Othello Game

This is a command line version of the Othello game, made with an object-oriented design.

It is multiplayer and is played on a 8x8 board.

## Othello
Othello is a game played between two players, one of whom will have black pieces and the other white pieces. Each player starts with two pieces on the board and in each turn must capture at least one of the opponent's pieces. In order to capture a piece, you must place your piece in such a way that the opponent's piece(s) will be sitting between two of your pieces. This must be in a straight line, including diagonally.

## Guide
### Hints
To make it easier to see where you can place pieces, you can type the character "h" and press enter. This will toggle on the hints. To turn these off, just type "h" again and press enter.

### Gameplay
The game starts with player white. Each time a player makes a move, it will switch to the other player, given there is a possible move for them to play. If that player does not have any possible moves, it will remain the prior player's turn and they will place another piece.

To place a piece, you must enter coordinate in the following manner:

>  3, 2

This represents row 3, column 2.
