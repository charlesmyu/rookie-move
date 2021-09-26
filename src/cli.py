from board import Board

board = Board()
for i in range(6):
    board.generate_rook()
print(board)