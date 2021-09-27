import unittest
import random
from board import Board

def init_standard(algo: str = 'random', nrow: int = 8, ncol: int = 8) -> Board:
    '''
    Use as standard method to generate new board with default rooks at (1, 2), (5, 7), (3, 6)
    '''
    return Board(['b3', 'f8', 'd7'], algo=algo, nrow=nrow, ncol=ncol)

class TestInit(unittest.TestCase):
    def test_init(self):
        board = init_standard()
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
        self.assertCountEqual(board._get_free_cols(), [0, 2, 4, 6, 7])
        self.assertCountEqual(board._get_free_rows(), [0, 1, 3, 4, 5])

    def test_init_empty(self):
        board = Board()
        self.assertListEqual(board._get_rook_positions(), [None, None, None, None, None, None, None, None])
        self.assertCountEqual(board._get_free_cols(), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertCountEqual(board._get_free_rows(), [0, 1, 2, 3, 4, 5, 6, 7])

    def test_init_colliding_rooks_col(self):
        with self.assertRaises(ValueError):
            board = Board(['b3', 'f6', 'b7'])

    def test_init_colliding_rooks_row(self):
        with self.assertRaises(ValueError):
            board = Board(['b3', 'f6', 'd3'])

    def test_init_invalid_nrow_ncol(self):
        with self.assertRaises(ValueError):
            board = init_standard(nrow=0)

    def test_init_invalid_ncol(self):
        with self.assertRaises(ValueError):
            board = init_standard(ncol=0)

    def test_init_rooks_out_of_row_range(self):
        with self.assertRaises(ValueError):
            board = Board(['b3', 'f9', 'd7'], ncol=8, nrow=8)

    def test_init_rooks_out_of_col_range(self):
        with self.assertRaises(ValueError):
            board = Board(['j3', 'f6', 'd7'], ncol=8, nrow=8)

    def test_init_explicit_ncol_nrow(self):
        board = Board(['b3', 'd4'], ncol=4, nrow=4)
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), (3, 'user')])
        self.assertCountEqual(board._get_free_cols(), [0, 2])
        self.assertCountEqual(board._get_free_rows(), [0, 1])

    def test_init_invalid_algo(self):
        with self.assertRaises(ValueError):
            board = Board(algo='abcd')

    def test_init_ordered_algo(self):
        board = init_standard(algo='ordered')
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board._get_free_cols(), [0, 2, 4, 6, 7])
        self.assertListEqual(board._get_free_rows(), [0, 1, 3, 4, 5])

    def test_init_random_algo(self):
        random.seed(2021)
        board = init_standard(algo='random')
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, None, None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board._get_free_cols(), [2, 0, 4, 7, 6])
        self.assertListEqual(board._get_free_rows(), [1, 5, 0, 3, 4])

class TestGenerateRook(unittest.TestCase):
    def test_generate(self):
        random.seed(2021)
        board = init_standard()
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, (6, 'program'), None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board._get_free_cols(), [2, 0, 4, 7])
        self.assertListEqual(board._get_free_rows(), [1, 5, 0, 3])

    def test_generate_no_valid_spaces(self):
        board = Board(['a1', 'b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8'])
        res = board.generate_rook()

        self.assertEqual(res, False)
        self.assertListEqual(board._get_rook_positions(), [(0, 'user'), (1, 'user'), (2, 'user'), (3, 'user'), 
                                                          (4, 'user'), (5, 'user'), (6, 'user'), (7, 'user')])
        self.assertListEqual(board._get_free_cols(), [])
        self.assertListEqual(board._get_free_rows(), [])

    def test_generate_explicit_dimensions(self):
        board = Board(['b3', 'c2', 'd4'], nrow=4, ncol=4)
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board._get_rook_positions(), [(0, 'program'), (2, 'user'), (1, 'user'), (3, 'user')])
        self.assertListEqual(board._get_free_cols(), [])
        self.assertListEqual(board._get_free_rows(), [])

        res = board.generate_rook()
        self.assertEqual(res, False)

    def test_generate_random(self):
        random.seed(2021)
        board = init_standard(algo='random')
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, (6, 'program'), None, (3, 'user'), (5, 'user')])
        self.assertListEqual(board._get_free_cols(), [2, 0, 4, 7])
        self.assertListEqual(board._get_free_rows(), [1, 5, 0, 3])

    def test_generate_ordered(self):
        board = init_standard(algo='ordered')
        res = board.generate_rook()

        self.assertEqual(res, True)
        self.assertListEqual(board._get_rook_positions(), [None, None, (1, 'user'), None, None, (7, 'program'), (3, 'user'), (5, 'user')])
        self.assertCountEqual(board._get_free_cols(), [0, 2, 4, 6])
        self.assertCountEqual(board._get_free_rows(), [0, 1, 3, 4])

class TestNumRooksLeft(unittest.TestCase):
    def test_num_rooks_left(self):
        board = init_standard()
        self.assertEqual(board.num_rooks_left(), 5)

    def test_num_rooks_left_none_left(self):
        board = init_standard()
        for i in range(5):
            board.generate_rook()
        self.assertEqual(board.num_rooks_left(), 0)

    def test_num_rooks_left_small_board(self):
        board = Board(['b3', 'c2', 'd4'], nrow=4, ncol=4)
        res = board.generate_rook()
        self.assertEqual(board.num_rooks_left(), 0)

class TestPrint(unittest.TestCase):
    def test_print_empty_board(self):
        expected = '\n\u272f --------\u272f\n| \u00B7 \u00B7 \u00B7 \u00B7 |\n| '\
            '\u00B7 \u00B7 \u00B7 \u00B7 |\n| \u00B7 \u00B7 \u00B7 \u00B7 |\n| '\
            '\u00B7 \u00B7 \u00B7 \u00B7 |\n\u272f --------\u272f\n\nUser Initia'\
            'lized Rooks (White): None\nProgram Generated Rooks (Black): None\n'

        board = Board(ncol = 4, nrow = 4)
        self.assertEqual(str(board), expected)

    def test_print_full_board_users(self):
        expected = '\n\u272f --------\u272f\n| \u00B7 \u00B7 \u00B7 \u265c |\n| '\
            '\u00B7 \u00B7 \u265c \u00B7 |\n| \u00B7 \u265c \u00B7 \u00B7 |\n| '\
            '\u265c \u00B7 \u00B7 \u00B7 |\n\u272f --------\u272f\n\nUser Initia'\
            'lized Rooks (White): a1, b2, c3, d4\nProgram Genera'\
            'ted Rooks (Black): None\n'

        board = Board(['a1', 'b2', 'c3', 'd4'], ncol = 4, nrow = 4)
        self.assertEqual(str(board), expected)

    def test_print_full_board_program(self):
        expected = '\n\u272f --------\u272f\n| \u00B7 \u00B7 \u00B7 \u2656 |\n| '\
            '\u00B7 \u00B7 \u2656 \u00B7 |\n| \u00B7 \u2656 \u00B7 \u00B7 |\n| '\
            '\u2656 \u00B7 \u00B7 \u00B7 |\n\u272f --------\u272f\n\nUser Initia'\
            'lized Rooks (White): None\nProgram Generated Rooks (Black): a1, b2, c3, d4\n'

        board = Board(ncol = 4, nrow = 4, algo='ordered')
        for i in range(4):
            board.generate_rook()
        self.assertEqual(str(board), expected)

    def test_print(self):
        expected = '\n\u272f --------\u272f\n| \u265c \u00B7 \u00B7 \u00B7 |\n| '\
            '\u00B7 \u00B7 \u00B7 \u2656 |\n| \u00B7 \u00B7 \u00B7 \u00B7 |\n| '\
            '\u00B7 \u00B7 \u00B7 \u00B7 |\n\u272f --------\u272f\n\nUser Initia'\
            'lized Rooks (White): a4\nProgram Generated Rooks (Black): d3\n'

        board = Board(['a4'], ncol = 4, nrow = 4, algo='ordered')
        board.generate_rook()
        self.assertEqual(str(board), expected)