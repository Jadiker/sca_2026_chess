# This imports everything that you need
from gen_pawn_advance import *

'''
If you do str(chess_board), it will print out something like:

8  . . . . . . . .
7  . . . . . . . .
6  . . . . . . . .
5  . . . . . . p .
4  P . P . P . P .
3  . . P . . . . P
2  . . . . . . . .
1  . . . . . . . .

   a b c d e f g h

where P represents a white pawn, p represents a black pawn, and . represents an empty square. The numbers on the left represent the ranks (1-8) and the letters on the bottom represent the files (a-h). So in the example above, there is a white pawn on a4, c4, e4, g4, and h3, and there is a black pawn on f5.


Useful functions:

legal_pawn_advance_moves(board: chess.Board) -> list[chess.Move]
    Returns a list of all legal moves that the current player can make in the given board state

chess_board.copy() -> chess.Board
    Returns a copy of the given chess board. This is useful because if you want to test a move to see what it would do, you can copy the board and then test the move out without modifying the original board.

chess_board.push(move)
    Modifies the given chess board by making the given move on it. A move is a string like "e2e4" which means move the piece on e2 to e4. You should usually get moves from the list of legal moves.

chess_board.turn -> chess.Color
    Returns the color of the current player (either chess.WHITE or chess.BLACK)

chess.square(file_index: int, rank_index: int) -> chess.Square
    Returns the square corresponding to the given file and rank indices. The file index is a number from 0 to 7 corresponding to the files a-h, and the rank index is a number from 0 to 7 corresponding to the ranks 1-8. So for example, chess_board.square(0, 0) would return the square a1, chess_board.square(7, 7) would return the square h8, chess_board.square(3, 4) would return the square d5, etc.

chess_board.piece_at(square: chess.Square) -> chess.Piece or None
    Returns the piece at the given square, or None if there is no piece at that square. You can check the piece type with chess_piece.piece_type (which will be chess.PAWN for pawns) and the piece color with chess_piece.color (which will be chess.WHITE for white pieces and chess.BLACK for black pieces).

chess_piece.color -> chess.Color
    Gives the color of the given chess piece (either chess.WHITE or chess.BLACK)

count_pawns(board: chess.Board, color: chess.Color) -> int
    Returns the number of pawns of the given color that are currently on the board. This can be useful for evaluating how well you're doing in the game.


Examples:

(See example_bots.py for more examples of how to code a bot.)

Here's how you could figure out if you have a pawn on f7:
def do_i_have_a_pawn_on_f7(chess_board: chess.Board) -> bool:
    # first, figure out what color player I am
    my_color = chess_board.turn

    # then, get the square corresponding to f7
    # f is the 5th letter of the alphabet, so its file index is 5. 7 is the 7th rank, so its rank index is 6 (since the rank index starts at 0).
    f7_square = chess.square(5, 6)

    # then, get the piece at that square
    piece_on_f7 = chess_board.piece_at(f7_square)

    # if the piece is None, then there's no piece there, so I don't have a pawn on f7
    if piece_on_f7 is None:
        return False
    else:
        # if there is a piece there, then check if it's my color
        piece_on_f7_color = piece_on_f7.color
        if piece_on_f7_color == my_color:
            return True
        else:
            return False

This can be generalized to check if a certain player has a pawn on a certain square:
def does_player_have_a_pawn_on_square(chess_board: chess.Board, color: chess.Color, square: chess.Square) -> bool:
    piece_on_square = chess_board.piece_at(square)
    if piece_on_square is None:
        return False
    else:
        if piece_on_square.color == color:
            return True
        else:
            return False

So then with this function defined, you could refactor the function to determine if you have a pawn on f7 to be:
def do_i_have_a_pawn_on_f7(chess_board: chess.Board) -> bool
    my_color = chess_board.turn
    f7_square = chess.square(5, 6)
    return does_player_have_a_pawn_on_square(chess_board, my_color, f7_square)
'''

class YourPawnAdvanceBot(PawnAdvanceBot):
    def make_move(self, chess_board: chess.Board) -> chess.Move:
        # Implement your strategy here! See example_bots.py for some ideas and functions you can use to help you code your bot.

        # By default, this bot just makes the first legal move that it finds
        # You should delete the code below and replace it with your own idea
        legal_moves = legal_pawn_advance_moves(chess_board)
        first_legal_move = legal_moves[0]
        return first_legal_move
