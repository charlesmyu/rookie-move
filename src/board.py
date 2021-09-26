import random

class Board():
    def __init__(self, initial_rooks: list = [], nrow: int = 8, ncol: int = 8, algo: str = 'random') -> None:
        '''
        Initializes an object that represents a chess board. 
        
        Three private instance variables are created:
            rows: array representing each row of the chess board, where the absolute value represents the rook's 
                column-wise position. If value is None, no rook is placed at that row. If value is positive, rook 
                placed by program. If value is negative, rook placed by user on initialization.
            free_rows: queue representing all rows not currently occupied by a rook
            free_cols: queue representing all columns not currently occupied by a rook

        :param initial_rooks: initial placement of rooks represented as a list of tuples that are ordered 
            pairs (col, row), indexed by 0 from bottom left. Placements must not collide.
        :param nrow: number of rows on chessboard. Defaults to 8.
        :param ncol: number of columns on chessboard. Defaults to 8.
        :param algo: 'algorithm' in which new rooks will be placed. Either 'random' or 'ordered'. Defaults to 'random'.
        '''
        if nrow <= 0 or ncol <= 0:
            raise ValueError('Invalid number of rows or columns detected!')
        if not algo in ['random', 'ordered']:
            raise ValueError('Specified algorithm not valid')
        if not Board._check_rook_placement_valid(initial_rooks, nrow, ncol):
            raise ValueError('Rook placement invalid!')

        # Declare instance variables if all check out
        self._rows = [None]*nrow 
        self._free_rows = list(range(nrow))
        self._free_cols = list(range(ncol))

        # Add initial_rooks into instance variables, remove from queues
        for position in initial_rooks:
            self._rows[position[1]] = -position[0]
            self._free_rows.remove(position[1])
            self._free_cols.remove(position[0])

        if algo == 'random':
            random.shuffle(self._free_rows)
            random.shuffle(self._free_cols)

    def get_rook_positions(self) -> list:
        return self._rows

    def get_free_rows(self) -> list:
        return self._free_rows

    def get_free_cols(self) -> list:
        return self._free_cols

    @staticmethod
    def _check_rook_placement_valid(rook_positions: list, nrow: int = 8, ncol: int = 8) -> bool:
        '''
        Checks to see if rook placement is valid. Checks for colliding rooks and for rooks placed off the board

        Iterates through all input ordered pairs, and records if row and column has been used before. If so, return false
        as rooks collide. Implementation uses sets, so time complexity is linear.

        :param rook_positions: placement of rooks represented as a list of ordered pairs, indexed by 0 from top left.
        :return: True if rooks do collide, False if rooks do not collide
        '''
        rows_used = set()
        cols_used = set()

        for position in rook_positions:
            if position[0] >= ncol or position[0] < 0:
                return False
            if position[1] >= nrow or position[1] < 0:
                return False

            if position[0] in cols_used or position[1] in rows_used:
                return False
            
            cols_used.add(position[0])
            rows_used.add(position[1])
        
        return True

