from board import Board

board = Board(['a1', 'b5'])
for i in range(6):
    board.generate_rook()
print(board)