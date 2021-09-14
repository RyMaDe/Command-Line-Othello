import colorama
from colorama import Fore
colorama.init(autoreset=True)


class Othello:
    def __init__(self):
        self.white = Player(self, "W")  # Initiate the black and white players
        self.black = Player(self, "B")
        self.board = Board(self.black, self.white)  # initiate the board
        self.board.Display()
        self.hints = False  # Hints on or off
        self.prevHints = []  # Current hints on the board

    def Place(self, player, x, y):
        # player wants to place a piece at point x,y
        self.board.New(player, x, y)
        if self.hints is True:
            # If the hints are on and the next player's turn
            # has been turned on, we can call for their
            # hints to be setup. The board can then be displayed.
            self.Hints(False)
        self.Display()

    def checkAll(self, player):
        # This checks if player has at least one available move.
        # Boolean return value
        return self.board.Available(player)

    def GetWhite(self):
        return self.white

    def GetBlack(self):
        return self.black

    def Display(self):
        self.board.Display()
        #  the current score below the board
        print("Black: {0}".format(self.black.count))
        print("White: {0}".format(self.white.count))

    def Hints(self, toggle=True):
        # Turns the hints on or off
        if toggle is True:
            if self.hints is True:
                self.hints = False
            else:
                self.hints = True

        if self.hints is True:
            # First get whose turn it is going to be.
            if self.white.turn is True:
                player = self.white
            elif self.black.turn is True:
                player = self.black
            else:
                return  # Game over - nobody's turn
            # Get all the available hints, and pass them over
            # to have them added to the board and have the old
            # hints removed.
            H = self.board.AvailableHints(player)
            self.board.TurnHints(H, self.prevHints)
            self.prevHints = H
        else:
            # remove old hints
            self.board.TurnHints([], self.prevHints)

        if toggle is True:
            self.Display()


class Player:
    def __init__(self, game, colour):
        self.game = game
        self.player = colour
        self.count = 0  # The no. of pieces the player has on the board
        self.turn = False  # True if it's their turn

    def getOpp(self):
        if self.player == "B":
            return self.game.GetWhite()
        else:
            return self.game.GetBlack()

    def place(self, x, y):
        # The player wants to place a piece at point x,y so call
        # the game method, Place, to do this.
        if (x >= 0 and x < len(self.game.board.board) and
                y >= 0 and y < len(self.game.board.board)):
            # Checking the x and y values are within bounds
            self.game.Place(self, x, y)

    def checkAll(self):
        # Checks if there is at least one move available.
        return self.game.checkAll(self)

    def Toggle(self):
        # This changes whose turn it is. If there is an available
        # move to be played then it's this player's turn. Otherwise
        # it checks the other player. This means it will not change
        # to anybody's turn unless there is a turn possible for them
        # to make.
        if self.checkAll() is True:
            self.turn = True
            self.getOpp().turn = False
        elif self.getOpp().checkAll() is True:
            pass
        else:
            self.getOpp().turn = False

    def Hints(self):  # Toggle hints
        self.game.Hints()


class Piece:
    def __init__(self, player, x, y):
        self.player = player
        self.colour = player.player
        self.player.count += 1  # Increases the player's piece count
        self.x = x
        self.y = y

    def flip(self, player):
        # Changes a piece from being one player's to the other's.
        self.player.count -= 1  # reduce old player's count by 1
        self.player = player
        self.colour = player.player
        self.player.count += 1  # increase new player's count by 1

    def __repr__(self):
        # Pieces should show in Blue or Red colour to differentiate
        # them from all other white spaces on the board. Using white
        # and black is not a good idea in the terminal.
        if self.colour == "B":
            return Fore.BLUE + self.colour + Fore.RESET
        elif self.colour == "W":
            return Fore.RED + self.colour + Fore.RESET


class Board:
    def __init__(self, black, white):
        # initialising the board and adding the default black
        # and white pieces.
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(8)]
        self.board[3][3] = Piece(white, 3, 3)
        self.board[4][4] = Piece(white, 4, 4)
        self.board[3][4] = Piece(black, 3, 4)
        self.board[4][3] = Piece(black, 4, 3)

    def Available(self, player):
        # This will loop through all available spaces in the board
        # and see whether a move can be played by the player. It
        # will return a boolean value for the checkAll method.
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0 or self.board[i][j] == 1:
                    # The 1 is to check hints also
                    count = self.New(player, i, j, turn=False)
                    if count > 0:
                        return True
        return False

    def New(self, player, x, y, turn=True):
        # "moves" list will be populated with all of the pieces
        # that need to be updated. The check  function is called
        # with different parameters to check in all directions.
        # Once the count is populated it will check if it's 0 in
        # which case no move is available for this piece at x,y.
        # If not 0 it will send the moves list to the Turn method to
        # update the pieces. We then swap the player's turn.

        # "turn" is just to check whether we want the pieces
        # to be updated or not. If it's false it's because we are calling
        # this method from Available() above and just need to
        # check that moves are available. This is why we keep a count.
        moves = []
        count = self.Check(player, x, y, -1, 0, moves)
        count += self.Check(player, x, y, +1, 0, moves)
        count += self.Check(player, x, y, 0, -1, moves)
        count += self.Check(player, x, y, 0, 1, moves)
        count += self.Check(player, x, y, -1, -1, moves)
        count += self.Check(player, x, y, -1, +1, moves)
        count += self.Check(player, x, y, +1, -1, moves)
        count += self.Check(player, x, y, +1, +1, moves)

        if count == 0 and turn is True:
            print("\nInvalid Move from {0}\n".format(player.player))
        elif turn is True:
            self.Turn(player, moves)
            player.getOpp().Toggle()
            # This is a valid move, so we change turns
        return count

    def Check(self, player, x, y, xd, yd, m, count=-1):
        # This is a recursive function that after each successful
        # recall will increment the piece by xd,yd. Each time it hits
        # an opposite piece it continues, if it hit's itself it returns
        # the count. If the move is actually invalid then we loop back
        # out of the recursion and return a 0.
        if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board):
            # Make sure coords are in bounds
            return 0
        if count == -1 and self.board[x][y] != 0 and self.board[x][y] != 1:
            # player selects section already taken
            return 0
        if count != -1 and (self.board[x][y] == 0 or self.board[x][y] == 1):
            # land on a empty piece
            return 0
        elif count == -1 or self.board[x][y].colour == player.getOpp().player:
            # Either the initial selection or following through
            count = self.Check(player, x+xd, y+yd, xd, yd, m, count+1)
            if count > 0:
                m.append((x, y))  # Add x,y to the moves list to be flipped
            return count
        elif self.board[x][y].player == player:  # Land on the same colour
            return count

    def Check2(self, player, x, y, xd, yd, m):
        # Alternative to check using iteration over recursion
        # This is not used, it's only here as a concept.
        if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board):
            # Make sure the selection is in bounds
            return 0
        if self.board[x][y] != 0 and self.board[x][y] != 1:
            # player selects section already taken
            return 0
        count = 0
        temp = (x, y)
        x += xd
        y += yd
        while True:
            if x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board):
                # Make sure the selection is in bounds
                for i in range(count):
                    del m[-1]
                return 0
            elif self.board[x][y] == 0 or self.board[x][y] == 1:
                # land on a empty piece
                for i in range(count):
                    del m[-1]
                return 0
            elif self.board[x][y].colour == player.getOpp().player:
                # Either the initial selection or following through
                m.append((x, y))
                count += 1
                x += xd
                y += yd
            elif self.board[x][y].player == player:  # Land on the same colour
                if count > 0:
                    m.append(temp)
                break
        return count

    def Turn(self, player, Moves):
        # This goes through the Moves list of coords and either
        # flips pieces to the player's colour or adds new pieces
        # at the coords of the player's colour.
        for move in Moves:
            if (self.board[move[0]][move[1]] != 0 and
                    self.board[move[0]][move[1]] != 1):
                # If the space is occupied
                self.board[move[0]][move[1]].flip(player)
            else:  # If the space is empty
                self.board[move[0]][move[1]] = Piece(player, move[0], move[1])

    def AvailableHints(self, player):
        # Finds all the available moves that can be made by the player
        # and stores them in H. Below we have to check if the board at
        # each section is a 0 (as it should be) or a 1 (previous
        # hints will still be there) meaning the space is not occupied.
        H = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0 or self.board[i][j] == 1:
                    count = self.New(player, i, j, turn=False)
                    if count > 0:
                        H.append((i, j))
        return H

    def TurnHints(self, H, prev):
        # Loop through all the previous hints and remove them.
        # Then loop through all the new hints and add them.
        for p in prev:
            if self.board[p[0]][p[1]] == 1:
                self.board[p[0]][p[1]] = 0
        for h in H:
            self.board[h[0]][h[1]] = 1

    def Display(self):
        # Prints the board to the screen
        print(" ", 0, 1, 2, 3, 4, 5, 6, 7, sep="  ")
        c = 0
        for i in self.board:
            print(c, i)
            c += 1


if __name__ == "__main__":
    x = Othello()  # initialise the game
    w = x.GetWhite()
    b = x.GetBlack()

    player = w  # This will change between B and W
    player.turn = True  # Start with player white's turn.

    while True:
        if player == w:
            # Enter input as x,y
            move = input("White move: ").split(",")
        else:
            move = input("Black move: ").split(",")

        if move == ["h"] or move == ["H"]:
            # Toggle the hints on or off
            player.Hints()
            continue

        try:
            move = list(map(int, move))
            player.place(move[0], move[1])  # Place piece at x,y if in bounds
        except (IndexError, ValueError):
            # If the input entered is invalid or outside the bounds,
            # then it will still be the player's turn so continue
            # to the next loop.
            continue

        # Check whose turn it is and change the player variable
        # to this player.
        if player.turn is True:
            pass
        elif player.getOpp().turn is True:
            player = player.getOpp()
        else:
            break  # If it's no one's turn then the game is over

    # Determine the winner by who has the greater number of pieces.
    if w.count > b.count:
        print("White won")
    elif b.count > w.count:
        print("Black won")
    else:
        print("Draw")
