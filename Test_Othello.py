import unittest
from Othello_Game import *


class OthelloGameTest(unittest.TestCase):
    def setUp(self):
        self.game = Othello()

    def test_GetWhite(self):
        self.assertEqual(self.game.GetWhite(), self.game.white)

    def test_GetBlack(self):
        self.assertEqual(self.game.GetBlack(), self.game.black)


class OthelloPlayerTest(unittest.TestCase):
    def setUp(self):
        self.game = Othello()

    def test_GetOpp(self):
        self.assertEqual(self.game.white.getOpp(), self.game.black)

    def test_place(self):
        # Checking if an invalid move will result in no change
        self.game.white.place(0, 0)
        self.assertEqual(self.game.board.board[0][0], 0)

        # Checking that a valid move does result in change
        self.game.white.place(3, 5)
        self.assertEqual(self.game.board.board[3][5].colour, "W")
        self.assertEqual(self.game.board.board[3][4].colour, "W")
        self.assertEqual(self.game.board.board[3][3].colour, "W")

        # Checking that the validation for the bounds is working.
        # We make sure it's black's turn then have them place an
        # out of bounds piece. The turn should still be black's.
        self.game.black.Toggle()
        self.game.black.place(99999, 99999)
        self.assertEqual(self.game.black.turn, True)

    def test_checkAll(self):
        self.assertEqual(self.game.white.checkAll(), True)

    def test_Toggle(self):
        self.game.white.Toggle()
        self.assertEqual(self.game.white.turn, True)

    def test_Hints(self):
        # Testing to make sure that when the hints are toggled on,
        # the correct hints appear on the board.
        self.game.white.turn = True
        self.game.white.Hints()
        self.assertEqual(self.game.board.board[5][3], 1)
        self.assertEqual(self.game.board.board[4][2], 1)
        self.assertEqual(self.game.board.board[2][4], 1)
        self.assertEqual(self.game.board.board[3][5], 1)

        # Testing to make sure hints disappear when toggled off.
        self.game.white.Hints()
        self.assertEqual(self.game.board.board[5][3], 0)
        self.assertEqual(self.game.board.board[4][2], 0)
        self.assertEqual(self.game.board.board[2][4], 0)
        self.assertEqual(self.game.board.board[3][5], 0)

    def test_placeHints(self):
        # Testing that the hints appear after a turn is made.
        self.game.white.turn = True
        self.game.white.Hints()
        self.game.white.place(5, 3)
        # Need to check black's hints are on.
        self.assertEqual(self.game.board.board[5][4], 1)
        self.assertEqual(self.game.board.board[5][2], 1)
        self.assertEqual(self.game.board.board[3][2], 1)


class OthelloPieceTest(unittest.TestCase):
    def setUp(self):
        self.game = Othello()

    def test_flip(self):
        self.piece = Piece(self.game.white, 1, 1)
        self.piece.flip(self.game.black)
        self.assertEqual(self.piece.player, self.game.black)
        self.assertEqual(self.piece.colour, self.game.black.player)


class OthelloBoardTest(unittest.TestCase):
    def setUp(self):
        self.game = Othello()

    def test_Turn(self):
        self.game.board.Turn(self.game.white, [(0, 0), (0, 1)])
        self.assertEqual(self.game.board.board[0][0].colour, "W")
        self.assertEqual(self.game.board.board[0][1].colour, "W")


if __name__ == "__main__":
    unittest.main()
