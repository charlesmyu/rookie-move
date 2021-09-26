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
            ncol: number of columns on board

        :param initial_rooks: initial placement of rooks represented as a list of tuples in chess notation. Placements must not collide.
        :param nrow: number of rows on chessboard. Defaults to 8.
        :param ncol: number of columns on chessboard. Defaults to 8.
        :param algo: 'algorithm' in which new rooks will be placed. Either 'random' or 'ordered'. Defaults to 'random'.
        '''
        if nrow <= 0 or ncol <= 0 or ncol > 26:
            raise ValueError('Invalid number of rows or columns detected!')
        if not algo in ['random', 'ordered']:
            raise ValueError('Specified algorithm not valid')

        ordered_pairs = []
        for location in initial_rooks:
            ordered_pairs.append(Board._chess_to_pair(location))

        if not Board._check_rook_placement_valid(ordered_pairs, nrow, ncol):
            raise ValueError('Rook placement invalid!')

        # Declare instance variables if all check out
        self._rows = [None]*nrow 
        self._free_rows = list(range(nrow))
        self._free_cols = list(range(ncol))
        self._ncol = ncol

        # Add ordered_pairs into instance variables, remove from queues
        for position in ordered_pairs:
            self._rows[position[1]] = (position[0], 'user')
            self._free_rows.remove(position[1])
            self._free_cols.remove(position[0])

        if algo == 'random':
            random.shuffle(self._free_rows)
            random.shuffle(self._free_cols)

    def __str__(self):
        '''
        Override __str__ method to allow user-friendly viewing of chess board

        :returns: Human readable string with image and coordinates of rooks on chess board
        '''
        corner = '\u272f'
        no_rook = '\u00B7'
        white_rook = '\u265c'
        black_rook = '\u2656'

        border = corner + ' ' + '-' * (self._ncol*2) + corner

        final = '\n' + border + '\n'

        for row in reversed(self._rows):
            final += '| '
            for col in range(self._ncol):
                pos = no_rook
                if row and row[0] == col:
                    if row[1] == 'user':
                        pos = white_rook
                    elif row[1] == 'program':
                        pos = black_rook
                final += pos + ' '
            final += '|\n'

        rook_coordinates = self._get_friendly_coordinates()

        final += border + '\n\n'
        final += 'User Initialized Rooks (White): ' + ', '.join(map(str, rook_coordinates['user'])) + '\n'
        final += 'Program Generated Rooks (Black): ' + ', '.join(map(str, rook_coordinates['program'])) + '\n'
        
        return final

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

    def num_rooks_left(self) -> int:
        '''
        Returns number of rooks that can be generated.

        :return: int representing number of rooks that can still be generated
        '''
        return min(len(self._free_rows), len(self._free_cols))

    def _get_rook_positions(self) -> list:
        '''
        Returns positions of rooks in a list representing each column, with information about whether user or program added rook.
        Primarily for testing purposes.

        :return: Ordered list of tuples, (rook_col, rook_source), where index denotes row position of rook, rook_col denotes
            column position of rook, and rook_source denotes whether user or program added rook 
        '''
        return self._rows

    def _get_free_rows(self) -> list:
        '''
        Returns all rows that are not currently occupied by rooks. Primarily for testing purposes.

        :return: Queue with all rows that a rook is not currently occupying
        '''
        return self._free_rows

    def _get_free_cols(self) -> list:
        '''
        Returns all columns that are not currently occupied by rooks. Primarily for testing purposes.

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

    def _get_friendly_coordinates(self):
        '''
        Obtain coordinates of user and program placed rooks.

        :return: Map containing two keys, 'user' and 'program', which each contain a list of their corresponding rook locations
            in chess notation
        '''
        rook_coordinates = {
            'user': [],
            'program': []
        }

        for idx, row in enumerate(self._rows):
            if row:
                rook_coordinates[row[1]].append(Board._pair_to_chess((row[0], idx)))

        if len(rook_coordinates['user']) == 0:
            rook_coordinates['user'] = ['None']
        if len(rook_coordinates['program']) == 0:
            rook_coordinates['program'] = ['None']

        return rook_coordinates

    @staticmethod
    def _chess_to_pair(chess_square: str) -> tuple:
        col = ord(chess_square[0]) - 97
        row = int(chess_square[1:]) - 1

        return (col, row)

    @staticmethod
    def _pair_to_chess(ordered_pair: tuple) -> str:
        col = chr(ordered_pair[0] + 97)
        row = ordered_pair[1] + 1

        return str(col) + str(row)

