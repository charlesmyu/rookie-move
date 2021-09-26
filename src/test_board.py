import unittest
import random
from board import Board

class TestInit(unittest.TestCase):
    def test_init(self):
        board = Board([(1, 2), (5, 7), (3, 6)])
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
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
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), (3, 'user')])
        self.assertCountEqual(board.get_free_cols(), [0, 2])
        self.assertCountEqual(board.get_free_rows(), [0, 1])

    def test_init_invalid_algo(self):
        with self.assertRaises(ValueError):
            board = Board(algo='abcd')

    def test_init_ordered_algo(self):
        board = Board([(1, 2), (5, 7), (3, 6)], algo='ordered')
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board.get_free_cols(), [0, 2, 4, 6, 7])
        self.assertListEqual(board.get_free_rows(), [0, 1, 3, 4, 5])

    def test_init_random_algo(self):
        random.seed(2021)
        board = Board([(1, 2), (5, 7), (3, 6)], algo='random')
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board.get_free_cols(), [2, 0, 4, 7, 6])
        self.assertListEqual(board.get_free_rows(), [1, 5, 0, 3, 4])

class TestGenerateRook(unittest.TestCase):
    def test_generate(self):
        random.seed(2021)
        board = Board([(1, 2), (5, 7), (3, 6)])
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, (6, 'program'), None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board.get_free_cols(), [2, 0, 4, 7])
        self.assertListEqual(board.get_free_rows(), [1, 5, 0, 3])

    def test_generate_no_valid_spaces(self):
        board = Board([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
        res = board.generate_rook()

        self.assertEqual(res, False)
        self.assertListEqual(board.get_rook_positions(), [(0, 'user'), (1, 'user'), (2, 'user'), (3, 'user'), 
                                                          (4, 'user'), (5, 'user'), (6, 'user'), (7, 'user')])
        self.assertListEqual(board.get_free_cols(), [])
        self.assertListEqual(board.get_free_rows(), [])

    def test_generate_explicit_dimensions(self):
        board = Board([(1, 2), (2, 1), (3, 3)], nrow=4, ncol=4)
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board.get_rook_positions(), [(0, 'program'), (2, 'user'), (1, 'user'), (3, 'user')])
        self.assertListEqual(board.get_free_cols(), [])
        self.assertListEqual(board.get_free_rows(), [])

        res = board.generate_rook()
        self.assertEqual(res, False)

    def test_generate_random(self):
        random.seed(2021)
        board = Board([(1, 2), (5, 7), (3, 6)], algo='random')
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, (6, 'program'), None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board.get_free_cols(), [2, 0, 4, 7])
        self.assertListEqual(board.get_free_rows(), [1, 5, 0, 3])

    def test_generate_ordered(self):
        board = Board([(1, 2), (5, 7), (3, 6)], algo='ordered')
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board.get_rook_positions(), [None, None, (1, 'user'), None, None, (7, 'program'), (3, 'user'), (5, 'user')])
        self.assertCountEqual(board.get_free_cols(), [0, 2, 4, 6])
        self.assertCountEqual(board.get_free_rows(), [0, 1, 3, 4])