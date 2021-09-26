import random

class Board():
    def __init__(self, initial_rooks: list = [], nrow: int = 8, ncol: int = 8, algo: str = 'random') -> None:
        '''
        Initializes an object that represents a chess board. 
        
        Three private instance variables are created:
            rows: array representing each row of the chess board, where the value is a tuple representing the rook's column-
                wise position and source of placement (col, placement). Placement value can either be 'program' or 'user', 
                depending on whether the program generated the rook's placement, or if the user added the rook on initialization.
                If no rook at row, value is None. 
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
            self._rows[position[1]] = (position[0], 'user')
            self._free_rows.remove(position[1])
            self._free_cols.remove(position[0])

        if algo == 'random':
            random.shuffle(self._free_rows)
            random.shuffle(self._free_cols)

    def generate_rook(self) -> bool:
        '''
        Generates a new rook on board object that does not collide with any other rook. Implemented to be in constant time
        to allow for rapid generation if necessary.

        :return: bool representing success of request. True if rook successfully generated, false if rook cannot be generated.
        '''
        if len(self._free_rows) == 0 or len(self._free_cols) == 0:
            return False

        rook_row = self._free_rows.pop()
        rook_col = self._free_cols.pop()

        self._rows[rook_row] = (rook_col, 'program')

        return True

    def get_rook_positions(self) -> list:
        '''
        Returns positions of rooks in a list representing each column, with information about whether user or program added rook.

        :return: Ordered list of tuples, (rook_col, rook_source), where index denotes row position of rook, rook_col denotes
            column position of rook, and rook_source denotes whether user or program added rook 
        '''
        return self._rows

    def get_free_rows(self) -> list:
        '''
        Returns all rows that are not currently occupied by rooks.

        :return: Queue with all rows that a rook is not currently occupying
        '''
        return self._free_rows

    def get_free_cols(self) -> list:
        '''
        Returns all columns that are not currently occupied by rooks.

        :return: Queue with all columns that a rook is not currently occupying
        '''
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

