import unittest
from board import Board

class TestInit(unittest.TestCase):
    def test_init(self):
        board = Board([(1, 2), (5, 7), (3, 6)])
        self.assertListEqual(board.get_rook_positions(), [None, None, -1, None, None, None, -3, -5])
        self.assertCountEqual(board.get_free_cols(), [0, 2, 4, 6, 7])
        self.assertCountEqual(board.get_free_rows(), [0, 1, 3, 4, 5])

    def test_init_empty(self):
        board = Board()
        self.assertListEqual(board.get_rook_positions(), [None, None, None, None, None, None, None, None])
        self.assertCountEqual(board.get_free_cols(), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertCountEqual(board.get_free_rows(), [0, 1, 2, 3, 4, 5, 6, 7])

    def test_init_colliding_rooks_col(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (2, 4), (1, 6)])

    def test_init_colliding_rooks_row(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (2, 4), (0, 4)])

    def test_init_invalid_nrow_ncol(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (5, 7), (3, 6)], nrow=0)

    def test_init_invalid_ncol(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (5, 7), (3, 6)], ncol=0)

    def test_init_rooks_out_of_row_range(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (5, 9), (3, 6)], ncol=8, nrow=8)

    def test_init_rooks_out_of_col_range(self):
        with self.assertRaises(ValueError):
            board = Board([(9, 2), (5, 7), (3, 6)], ncol=8, nrow=8)

    def test_init_rooks_out_of_row_range_neg(self):
        with self.assertRaises(ValueError):
            board = Board([(1, 2), (5, -1), (3, 6)], ncol=8, nrow=8)

    def test_init_rooks_out_of_col_range_neg(self):
        with self.assertRaises(ValueError):
            board = Board([(-1, 2), (5, 7), (3, 6)], ncol=8, nrow=8)

    def test_init_explicit_ncol_nrow(self):
        board = Board([(1, 2), (3, 3)], ncol=4, nrow=4)
        self.assertListEqual(board.get_rook_positions(), [None, None, -1, -3])
        self.assertCountEqual(board.get_free_cols(), [0, 2])
        self.assertCountEqual(board.get_free_rows(), [0, 1])

    def test_init_invalid_algo(self):
        with self.assertRaises(ValueError):
            board = Board(algo='abcd')

    def test_init_ordered_algo(self):
        board = Board([(1, 2), (5, 7), (3, 6)], algo='ordered')
        self.assertListEqual(board.get_rook_positions(), [None, None, -1, None, None, None, -3, -5])
        self.assertListEqual(board.get_free_cols(), [0, 2, 4, 6, 7])
        self.assertListEqual(board.get_free_rows(), [0, 1, 3, 4, 5])