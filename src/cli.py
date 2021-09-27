from board import Board
import sys

class CLI():
    def run_cli():
        argc = len(sys.argv)

        if(argc > 1):
            try:
                board = Board(sys.argv[1:])
                for i in range(8 - (argc-1)):
                    board.generate_rook()
                print(board)
            except ValueError as e:
                print('ValueError: ' + str(e))
            
            return

        print('\nWelcome to \u265c -ie Move!\n')
        print('Please initialize your rooks. Enter them in chess notation, separated by spaces (e.g. a1 b2 c3): \n')

        initial_pos = str(input()).split()

        algo = None
        while not algo:
            print('\nPlease enter your choice of algorithm: ')
            print('1) Random (Default)')
            print('2) Ordered\n')

            algo = input()
            print()

            if algo == '1' or algo == '\n':
                print('Random algorithm selected!\n')
                algo = 'random'
            elif algo == '2': 
                print('Ordered algorithm selected!\n')
                algo = 'ordered'
            else:
                print('Algorithm choice invalid, please try again. Please enter either 1 or 2.\n')
                algo = None

        try:
            board = Board(initial_pos, algo=algo)
            print(board)

            while board.num_rooks_left() > 0:
                print('Press enter to generate a new rook! Input "e" to exit.\n')
                if input() == 'e':
                    print('\nGoodbye!\n')
                    return
                board.generate_rook()
                print(board)

            print('No more rooks to generate. Goodbye!\n')

        except ValueError as e:
            print('ValueError: ' + str(e))
            print()

if __name__ == '__main__':
    CLI.run_cli()