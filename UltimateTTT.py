# Author: Blake Mosley
# Email: Blaketmosley12@gmail.com

import math
import tkinter as tk

class UltimateTicTacToe:
    def __init__(self):
        # Global board: Each board is represented by its status.
        # For unfinished boards, we simply keep its index.
        self.gloBoard = list(range(9))
        # Local boards: 9 boards each with 9 cells (0..8).
        self.loBoards = [list(range(9)) for _ in range(9)]
        self.comPlayer = 'O'   # AI 
        self.humPlayer = 'X'   # Human 
        self.turn = 0
        self.maxDepth = 2  # depth of search going past 2 adds a lot of time for the Ai to think
        # active_board is the board in which the next move must be played(rule 3 and background will be yellow)
        # if None the player can choose any unfinished board. (background will be blank)
        self.active_board = None

    def empty_glo_indices(self, gloBoard):
        # return indices of boards that are unfinished
        return [s for s in gloBoard if isinstance(s, int)]

    def empty_lo_indices(self, openBoards, loBoards):
        # For each board in openBoards return a list of cell indices that are not yet occupied
        emptySpots = []
        for boardIndex in openBoards:
            spots = [i for i, sq in enumerate(loBoards[boardIndex]) if sq not in ['X', 'O']]
            emptySpots.append(spots)
        return emptySpots

    # winnign conditions
    def winning(self, board, player):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in wins:
            if board[a] == player and board[b] == player and board[c] == player:
                return True
        return False

    def all_x_or_o(self, board):
        # Returns true if every cell in the board is either X or O
        return all(cell in ['X', 'O'] for cell in board)

    def eval_board(self, current, los):
        """
        Evaluation function for the current state
         - current: the index of the board in which the last move was played
         - lo: the local boards a list of 9 boards each a list of 9 cells

        Returns a numeric score representing the desirability of the state
        Lower scores favor the AI (O) and higher scores favor the human (X).
        """
        allWinningCombos = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
        # Weight for positions in a board
        positionScores = [0.3, 0.2, 0.3, 0.2, 0.4, 0.2, 0.3, 0.2, 0.3]
        # Weight for each small board
        loBoardWeightings = [1.35, 1, 1.35, 1, 1.7, 1, 1.35, 1, 1.35]

        def row_score(arr):
            # Calculates a score for a given row or column/diagonal in a board
            oCount = sum(1 for x in arr if x == 'O')
            xCount = sum(1 for x in arr if x == 'X')
            numCount = sum(1 for x in arr if x not in ['X', 'O'])
            if oCount == 3:
                return -12
            if oCount == 2 and numCount == 1:
                return -6
            if xCount == 2 and numCount == 1:
                return 6
            if xCount == 2 and oCount == 1:
                return -9
            if xCount == 3:
                return 12
            if oCount == 2 and xCount == 1:
                return 9
            return 0

        score = 0
        glo = [None] * 9# builds a temporary global board representation
        for i in range(9):
            if self.winning(los[i], self.comPlayer):
                glo[i] = 'O'
                score -= positionScores[i] * 150
            elif self.winning(los[i], self.humPlayer):
                glo[i] = 'X'
                score += positionScores[i] * 150
            elif self.all_x_or_o(los[i]):
                glo[i] = 'D'
            else:
                glo[i] = i  # Board is still open

        # Evaluate global board status
        if self.winning(glo, self.comPlayer):
            score -= 50000
        elif self.winning(glo, self.humPlayer):
            score += 50000

        # Evaluate each local board
        for i in range(9):
            for j in range(9):
                if los[i][j] == self.comPlayer:
                    # if this board is the active board weight moves more heavily
                    if i == current:
                        score -= positionScores[j] * 1.5 * loBoardWeightings[i]
                    else:
                        score -= positionScores[j] * loBoardWeightings[i]
                elif los[i][j] == self.humPlayer:
                    if i == current:
                        score += positionScores[j] * 1.5 * loBoardWeightings[i]
                    else:
                        score += positionScores[j] * loBoardWeightings[i]

            # Sum row scores for each row/column/diagonal for this board
            raw_scores = set()
            for combo in allWinningCombos:
                loArr = [los[i][combo[0]], los[i][combo[1]], los[i][combo[2]]]
                rowScoreVal = row_score(loArr)
                if rowScoreVal not in raw_scores:
                    if combo in [(0, 4, 8), (2, 4, 6)]:
                        if rowScoreVal in [6, -6]:
                            score += rowScoreVal * (1.2 * 1.5 * loBoardWeightings[i] if i == current 
                                                    else 1.2 * loBoardWeightings[i])
                        else:
                            score += rowScoreVal * (1.5 * loBoardWeightings[i] if i == current 
                                                    else loBoardWeightings[i])
                    else:
                        score += rowScoreVal * (1.5 * loBoardWeightings[i] if i == current 
                                                else loBoardWeightings[i])
                    raw_scores.add(rowScoreVal)

        # Evaluate the global board combines the results of each small board
        raw_scores_global = set()
        for combo in allWinningCombos:
            gloArr = [glo[combo[0]], glo[combo[1]], glo[combo[2]]]
            rowScoreVal = row_score(gloArr)
            if rowScoreVal not in raw_scores_global:
                if combo in [(0, 4, 8), (2, 4, 6)]:
                    if rowScoreVal in [6, -6]:
                        score += rowScoreVal * 1.2 * 150
                    else:
                        score += rowScoreVal * 150
                else:
                    score += rowScoreVal * 150
                raw_scores_global.add(rowScoreVal)

        # Additional heuristic
        # Reward boards that are close to being decided by adding bonus for filled cells
        for i in range(9):
            if isinstance(self.gloBoard[i], int):  # Board is still open.
                empty = len([sq for sq in self.loBoards[i] if sq not in ['X', 'O']])
                score += (9 - empty) * 5

        # If an active board is set give bonus if it is nearly resolved
        if self.active_board is not None:
            moves_in_active = len([sq for sq in self.loBoards[self.active_board] if sq not in ['X', 'O']])
            score += (5 - moves_in_active) * 20

        return score

    def minimax(self, move, los, player, depth, maxDepth):
        """
        Implements the minimax algorithm
        
         - move: a dictionary with keys gloIndex and loIndex representing the move being evaluated
         - los: the list of local boards
         - player: the current player for this move X or O
         - depth: current search depth
         - alpha, beta: values for alpha-beta pruning
         - maxDepth: maximum search depth
        
        Returns a dictionary containing a score key and when not at a leaf the best  move is found
        """
        score = self.eval_board(move['gloIndex'], los)
        if depth == maxDepth:
            return {'score': score}

        # build a temporary global board for the minimax search
        gloBoardMinimax = [None] * 9
        for i in range(9):
            if self.winning(los[i], self.comPlayer):
                gloBoardMinimax[i] = 'O'
            elif self.winning(los[i], self.humPlayer):
                gloBoardMinimax[i] = 'X'
            elif self.all_x_or_o(los[i]):
                gloBoardMinimax[i] = 'D'
            else:
                gloBoardMinimax[i] = i

        # If the global board is won at this level return a score adjusted by depth
        if self.winning(gloBoardMinimax, self.comPlayer):
            return {'score': score + depth}
        elif self.winning(gloBoardMinimax, self.humPlayer):
            return {'score': score - depth}

        #selftemp is tempporary
        openBoardsMinimax = self.empty_glo_indices(gloBoardMinimax)
        if len(openBoardsMinimax) == 0:
            return {'score': score}

        emptySpotsInLoBoards = self.empty_lo_indices(openBoardsMinimax, los)

        if player == self.humPlayer:
            # this is the maximizing branch human is trying to maximize the score
            maxVal = -math.inf
            bestMove = None
            for o, boardIndex in enumerate(openBoardsMinimax):
                for loIndex in emptySpotsInLoBoards[o]:
                    moveCandidate = {'gloIndex': boardIndex, 'loIndex': loIndex}
                    original = los[boardIndex][loIndex]
                    los[boardIndex][loIndex] = 'X'  # simulate move for human
                    result = self.minimax(moveCandidate, los, self.comPlayer, depth + 1, maxDepth)
                    los[boardIndex][loIndex] = original  # undo move
                    if result['score'] > maxVal:
                        maxVal = result['score']
                        bestMove = {'gloIndex': boardIndex, 'loIndex': loIndex, 'score': result['score']}
            return bestMove if bestMove is not None else {'score': maxVal}
        else:
            minVal = math.inf
            bestMove = None
            for o, boardIndex in enumerate(openBoardsMinimax):
                for loIndex in emptySpotsInLoBoards[o]:
                    moveCandidate = {'gloIndex': boardIndex, 'loIndex': loIndex}
                    # Save current state and try move
                    original = los[boardIndex][loIndex]
                    los[boardIndex][loIndex] = 'O'
                    # Recursively call minimax for the opponent
                    result = self.minimax(moveCandidate, los, self.humPlayer, depth + 1, maxDepth)
                    los[boardIndex][loIndex] = original  # undo move
                    if result['score'] < minVal:
                        minVal = result['score']
                        bestMove = {'gloIndex': boardIndex, 'loIndex': loIndex, 'score': result['score']}
            return bestMove if bestMove is not None else {'score': minVal}

    def update_global_board(self, nextBoardIndex):
        """
        Updates the global board status based on each local board's status.
        A board is marked as X, O, or D if it is finished. otherwise it remains open.
        Also sets the active board based on the nextBoardIndex.
        """
        for i in range(9):
            if self.winning(self.loBoards[i], self.humPlayer):
                self.gloBoard[i] = 'X'
            elif self.winning(self.loBoards[i], self.comPlayer):
                self.gloBoard[i] = 'O'
            elif self.all_x_or_o(self.loBoards[i]):
                self.gloBoard[i] = 'D'
            else:
                self.gloBoard[i] = i  # still available

        # Set the active board
        if isinstance(self.gloBoard[nextBoardIndex], int):
            self.active_board = nextBoardIndex
        else:
            self.active_board = None

    def make_move(self, gloIndex, loIndex, player):
        # Reject the move if the board is closed
        if not isinstance(self.gloBoard[gloIndex], int):
            print(f"Board {gloIndex} is closed. You cannot play there.")
            return False
        # If an active board is set enforce that move must be in that board
        if self.active_board is not None and gloIndex != self.active_board:
            print(f"You must play in board {self.active_board}.")
            return False
        if self.loBoards[gloIndex][loIndex] in ['X', 'O']:
            print("That cell is already taken. Please choose a different cell.")
            return False
        self.loBoards[gloIndex][loIndex] = player
        self.turn += 1
        self.update_global_board(loIndex)
        return True

    def play_ai_move(self):
        # If there's an active board, only consider that one.
        if self.active_board is not None:
            openBoards = [self.active_board]
        else:
            openBoards = self.empty_glo_indices(self.gloBoard)
        if not openBoards:
            return None
        bestMove = None
        minScore = math.inf
        emptySpotsInLoBoards = self.empty_lo_indices(openBoards, self.loBoards)
        for o, boardIndex in enumerate(openBoards):
            for loIndex in emptySpotsInLoBoards[o]:
                moveCandidate = {'gloIndex': boardIndex, 'loIndex': loIndex}
                original = self.loBoards[boardIndex][loIndex]
                # Try the move temporarily
                self.loBoards[boardIndex][loIndex] = 'O'
                # Run minimax for this move
                result = self.minimax(moveCandidate, self.loBoards, self.humPlayer, 0, self.maxDepth)
                self.loBoards[boardIndex][loIndex] = original  # revert the move
                if result is not None and result.get('score', math.inf) < minScore:
                    minScore = result['score']
                    bestMove = {'gloIndex': boardIndex, 'loIndex': loIndex, 'score': result['score']}
        if bestMove:
            self.loBoards[bestMove['gloIndex']][bestMove['loIndex']] = 'O'
            print(f"AI plays at global board {bestMove['gloIndex']}, cell {bestMove['loIndex']}")
            self.update_global_board(bestMove['loIndex'])
            self.turn += 1
            return bestMove
        return None

# GUI using Tkinter
class UltimateTicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        # Sset main frame background to black to display black grid lines
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.game = UltimateTicTacToe()
        # Create 9 frames for each small board 3x3 grid
        self.boards = {}
        self.cell_buttons = {}  # Dictionary mapping board index to a 3x3 list of buttons
        for board_index in range(9):
            # Each board frame will have a white background 
            frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
            self.boards[board_index] = frame
            self.cell_buttons[board_index] = [[None for _ in range(3)] for _ in range(3)]
        
        # Place the 9 board frames in a 3x3 grid with padding so the black background shows as grid lines
        for i in range(3):
            for j in range(3):
                board_index = i * 3 + j
                self.boards[board_index].grid(row=i, column=j, padx=5, pady=5)
                # Create a 3x3 grid of buttons within each board
                for r in range(3):
                    for c in range(3):
                        cell_index = r * 3 + c
                        btn = tk.Button(self.boards[board_index],
                                        text=str(cell_index),
                                        width=4, height=2,
                                        command=lambda b=board_index, cell=cell_index: self.on_cell_click(b, cell))
                        btn.grid(row=r, column=c, padx=2, pady=2)
                        self.cell_buttons[board_index][r][c] = btn

        self.status_label = tk.Label(root, text="Your turn (X)")
        self.status_label.grid(row=1, column=0, pady=5)
        self.update_gui()

    def on_cell_click(self, board_index, cell_index):
        # When a cell is clicked try to make a move
        if self.game.make_move(board_index, cell_index, self.game.humPlayer):
            self.update_gui()
            if self.game.winning(self.game.gloBoard, self.game.humPlayer):
                self.status_label.config(text="Human wins!")
                self.disable_all_buttons()
                return
            elif not self.game.empty_glo_indices(self.game.gloBoard):
                self.status_label.config(text="Draw!")
                self.disable_all_buttons()
                return
            self.status_label.config(text="AI is thinking...")
            self.root.update_idletasks()  # Refresh GUI
            self.game.play_ai_move()
            self.update_gui()
            if self.game.winning(self.game.gloBoard, self.game.comPlayer):
                self.status_label.config(text="AI wins!")
                self.disable_all_buttons()
                return
            elif not self.game.empty_glo_indices(self.game.gloBoard):
                self.status_label.config(text="Draw!")
                self.disable_all_buttons()
                return
            self.status_label.config(text="Your turn (X)")
        else:
            self.status_label.config(text="Invalid move. Try again.")

    def update_gui(self):
        # Update each cell button based on the game state
        for board_index in range(9):
            for r in range(3):
                for c in range(3):
                    cell_index = r * 3 + c
                    val = self.game.loBoards[board_index][cell_index]
                    btn = self.cell_buttons[board_index][r][c]
                    if val in ['X', 'O']:
                        # Set X's to blue and O's to red
                        fg_color = "blue" if val == 'X' else "red"
                        btn.config(text=val, state="disabled", fg=fg_color)
                    else:
                        btn.config(text=str(val), state="normal", fg="black")
            # If the board is closed, disable all its buttons and change background
            if not isinstance(self.game.gloBoard[board_index], int):
                if self.game.gloBoard[board_index] == 'X':
                    board_color = "lightblue"  # Human won
                elif self.game.gloBoard[board_index] == 'O':
                    board_color = "lightcoral"  # AI won
                else:
                    board_color = "lightgrey"  # Draw
                for r in range(3):
                    for c in range(3):
                        self.cell_buttons[board_index][r][c].config(state="disabled", bg=board_color)
            else:
                # Reset background if board is open
                for r in range(3):
                    for c in range(3):
                        self.cell_buttons[board_index][r][c].config(bg="white")
        # Highlight the active board with a yellow frame
        for board_index, frame in self.boards.items():
            if self.game.active_board is not None and board_index == self.game.active_board:
                frame.config(bg="yellow")
            else:
                # If the board is closed retain its closed color else white
                if isinstance(self.game.gloBoard[board_index], int):
                    frame.config(bg="white")
                else:
                    if self.game.gloBoard[board_index] == 'X':
                        frame.config(bg="lightblue")
                    elif self.game.gloBoard[board_index] == 'O':
                        frame.config(bg="lightcoral")
                    else:
                        frame.config(bg="lightgrey")

    def disable_all_buttons(self):
        # Disable every button used when the game is over
        for board_index in range(9):
            for r in range(3):
                for c in range(3):
                    self.cell_buttons[board_index][r][c].config(state="disabled")

# Run the GUI
if __name__ == '__main__':
    root = tk.Tk()
    gui = UltimateTicTacToeGUI(root)
    root.mainloop()
