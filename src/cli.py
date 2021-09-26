from board import Board

board = Board([(0, 0)])
for i in range(7):
    board.generate_rook()
print(board)