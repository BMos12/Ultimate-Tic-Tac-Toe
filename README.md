# Ultimate-Tic-Tac-Toe
Ultimate Tic Tac Toe using the Minmax AI algorithm

# Rules
1. The two players X and O take turns starting with X which is the player

2. The game starts with X playing wherever they want in any of the 81 empty spots

3. Thereafter each player moves in the small board corresponding to the position of the 
    previous move in its small board. Example: if the player chose to play in board 0
    cell 6 then the AI would have play its move in board 6. If the AI chose board 6 cell 4
    then the player plays in board 4. The back ground will turn yellow if you are forced to
    play in a board. If it is not yellow then you can choose any board.

4. If a move is played so that it wins a small board by the rules of normal tic-tac-toe then 
    the entire small board is marked as won by the player in the larger board. This is indicated
    by the background of the small board turning either blue or red. blue for X and red for O.

5. Once a small board is won by a player or it is filled completely no more moves may be played in
    that board. If a player is sent to such a board then that player may play in any other board.
    example: You won board 4. Ai plays on board 6 cell 4. Board 4 is unplayable so you can choose
    boards 0-3 aor 3-8.

6. Game play ends when either a player wins the larger board or there are no legal moves remaining 
    in which case the game is a draw. Winning the larger board means getting 3 in a row of the smaller
    boards which you must win.

# Visuals
- Active boards are highlighted in yellow.
- Won boards are tinted: light blue for you, light coral for the AI.
- The status label at the bottom guides gameplay and shows results.
