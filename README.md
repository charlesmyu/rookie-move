# &#9820;-ie Move
Rookie Move takes a chess board with random rooks placed on it, and places more rooks such that none of them collide. This was created in response to the rook placement coding challenge provided by Tesla. 

## Getting Started 
1. Make sure you are in the `rookie-move` directory
2. Run the interactive program by using `py rookie-move.py` on Windows, or `python rookie-move.py` on Unix
3. Follow the instructions and have fun!

If you would like to use the program using arguments, run Rookie Move by using `py rookie-move.py <initial position> ...` where `<initial position>` is a number of initial positions for rooks in chess notation. For example, one could run `py rookie-move.py a1 b2 c3`, which would place rooks initially at `a1`, `b2`, and `c3`. The program will then populate as many rooks as it can fit without having any that collide.

### Sample Input/Output
Input: `py rookie-move.py a6 d2 h5`  
Output: 
```
✯ ----------------✯  
| · · · · · · ♖ · |  
| · · ♖ · · · · · |  
| ♜ · · · · · · · |  
| · · · · · · · ♜ |  
| · · · ♖ · · · · |  
| · · · · · ♖ · · |  
| · ♜ · · · · · · |  
| · · · · ♖ · · · |  
✯ ----------------✯  

User Initialized Rooks (White): b2, h5, a6
Program Generated Rooks (Black): e1, f3, d4, c7, g8
```

Input: `py rookie-move.py`  
Output:
```
Welcome to ♜-ie Move!

Please initialize your rooks. Enter them in chess notation, separated by spaces (e.g. a1 b2 c3):

>> a6 d2 h5

Please enter your choice of algorithm:
1) Random (Default)
2) Ordered

>> 1

Random algorithm selected!


✯ ----------------✯
| · · · · · · · ·  |
| · · · · · · · ·  |
| ♜ · · · · · · · |
| · · · · · · · ♜ |
| · · · · · · · ·  |
| · · · · · · · ·  |
| · · · ♜ · · · · |
| · · · · · · · ·  |
✯ ----------------✯

User Initialized Rooks (White): d2, h5, a6
Program Generated Rooks (Black): None

Press enter to generate a new rook! Input "e" to exit.

>> <enter>


✯ ----------------✯
| · · · · · · · ·  |
| · · · · ♖ · · · |
| ♜ · · · · · · · |
| · · · · · · · ♜ |
| · · · · · · · ·  |
| · · · · · · · ·  |
| · · · ♜ · · · · |
| · · · · · · · ·  |
✯ ----------------✯

User Initialized Rooks (White): d2, h5, a6
Program Generated Rooks (Black): e7

Press enter to generate a new rook! Input "e" to exit.

>> e

Goodbye!
```

## Testing
All tests reside in `test_board.py`. To run tests, use `py -m unittest` (or `python -m unittest` on Unix). 

## Design Decisions
I approached this problem trying to keep scalability and performance at top of mind. In this case, I took scalability to be a potential increase in board size (and thus number of rooks placed).  

To achieve this, I designed the data structures of the `Board` object to faciliate `O(1)` position generations, so that large numbers of rook locations could be generated without performance detriments. This was possible through the use of an array to track existing rooks (`self._rows`). Since each row and column can only contain a single rook, I used each entry in the array to represent a row in the board, and the value of each entry to represent the column the rook occupied, if any.  

I then used two queues (`self._free_rows`, `self._free_cols`) to store any unoccupied rows and columns. Since any pair of unoccupied row and column form a valid rook placement, I simply removed an entry from each queue upon generation of a rook placement, enabling constant time position generation.  

I also implemented two distinct 'algorithms' for generating the rook placements. The ordered algorithm generates positions in a predictable sequence, where the valid square closest to the upper right of the board is used. On the other hand, the random algorithm randomizes the position generated, selecting from any of the valid combinations on the board. This was accomplished by randomizing the queues during initialization, such that the entries removed on generation each time would be random.  

In the spirit of considering scalability, I incorporated the ability to manipulate the size of the chessboard into the `Board` class (although I did not expose this functionality to the CLI). This allows the user to flexibly modify the board used, and either scale it up to a size larger than 8x8, or to a size smaller than 8x8. At the moment, the board's width is limited to 26 spaces due to limiations with chess notation, although this could be solved by a different notation or an extended chess notation in the future if needed. 

## A Quick Note on Chess Notation
In case you are not familiar, chess notation is a method of notating squares on a chess board, where the letter specifies the column, and the number specifies the row. These are indexed from the bottom left corner, starting at `a1`. For example, `d5` would refer to the 4th square to the right, and the 5th square up.  

If you have any questions about this program, please don't hesitate to contact me at `charles.yu@uwaterloo.ca`!