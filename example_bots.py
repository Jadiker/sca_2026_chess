# import everything that you need
from gen_pawn_advance import *


class CapturePawnAdvanceBot(PawnAdvanceBot):
    # An example of how you could code a bot to play Pawn Advance. This bot will always try to capture an opponent's pawn if it can, and if not, it will just make the first legal move that it finds.
    def make_move(self, chess_board: chess.Board) -> chess.Move:
        # first, figure out which color player I am
        my_color = chess_board.turn
        # then, generate all legal moves
        legal_moves = legal_pawn_advance_moves(chess_board)

        # then, see if I can capture an opponent's pawn
        for move in legal_moves:
            if is_capture_move(chess_board, move, my_color):
                # do the first capture move that I find
                return move
            
        # if there's no capture move, just do the first legal move that I find
        return legal_moves[0]
    
class RandomPawnAdvanceBot(PawnAdvanceBot):
    # This bot will just make a random legal move every turn, without any strategy.
    def make_move(self, chess_board: chess.Board) -> chess.Move:
        import random
        legal_moves = legal_pawn_advance_moves(chess_board)
        return random.choice(legal_moves)
