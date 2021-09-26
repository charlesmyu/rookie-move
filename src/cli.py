from board import Board

board = Board([(0, 0)])
for i in range(6):
    board.generate_rook()
print(board)