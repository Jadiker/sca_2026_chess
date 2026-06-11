# YOU DO NOT NEED TO READ OR UNDERSTAND THIS CODE AT ALL
# Implementation of the Pawn Advance chess variant, where each player starts with 8 pawns and the goal is to get a pawn to the other side of the board or capture all of the opponent's pawns.
# En Passant is not allowed, and games end in a tie if a player has no legal moves on their turn (even if they still have pawns left).

import chess
import random # not used, but nice to have imported for other scripts

WHITE_WINNER = "White"
BLACK_WINNER = "Black"
TIE_WINNER = "Tie"

# either WHITE_WINNER, BLACK_WINNER, TIE_WINNER, or None if the game is still ongoing
WinnerColor = str | None

class LabeledBoard(chess.Board):
    def __str__(self) -> str:
        rows: list[str] = []

        for rank in range(7, -1, -1):
            pieces: list[str] = []

            for file in range(8):
                square = chess.square(file, rank)
                piece = self.piece_at(square)
                pieces.append(piece.symbol() if piece else ".")

            rows.append(f"{rank + 1}  " + " ".join(pieces))

        rows.append("")
        rows.append("   a b c d e f g h")
        return "\n".join(rows)


def make_pawn_advance_board() -> LabeledBoard:
    board = LabeledBoard(None)

    for column in range(8):
        board.set_piece_at(chess.square(column, 1), chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(chess.square(column, 6), chess.Piece(chess.PAWN, chess.BLACK))

    board.turn = chess.WHITE
    board.clear_stack()
    return board


def count_pawns(board: chess.Board, color: chess.Color) -> int:
    count = 0

    for square in chess.SQUARES:
        if board.piece_at(square) == chess.Piece(chess.PAWN, color):
            count += 1

    return count


def is_forward_move(board: chess.Board, move: chess.Move, color: chess.Color) -> bool:
    from_file = chess.square_file(move.from_square)
    from_rank = chess.square_rank(move.from_square)
    to_file = chess.square_file(move.to_square)
    to_rank = chess.square_rank(move.to_square)

    direction = 1 if color == chess.WHITE else -1
    start_rank = 1 if color == chess.WHITE else 6

    if from_file != to_file:
        return False

    if board.piece_at(move.to_square) is not None:
        return False

    if to_rank - from_rank == direction:
        return True

    if from_rank == start_rank and to_rank - from_rank == 2 * direction:
        middle_square = chess.square(from_file, from_rank + direction)
        return board.piece_at(middle_square) is None

    return False

def is_enemy_piece(board: chess.Board, square_name: str) -> bool:
    square = chess.parse_square(square_name)
    piece = board.piece_at(square)

    if piece is None:
        # empty square, not an enemy piece
        return False

    if piece.color == board.turn:
        # piece belongs to the current player: not an enemy piece
        return False
    else:
        # piece belongs to the opponent: it's an enemy piece
        return True
    
def is_my_piece(board: chess.Board, square_name: str) -> bool:
    square = chess.parse_square(square_name)
    piece = board.piece_at(square)

    if piece is None:
        # empty square, not my piece
        return False

    if piece.color == board.turn:
        # piece belongs to the current player: it's my piece
        return True
    else:
        # piece belongs to the opponent: not my piece
        return False


def is_capture_move(board: chess.Board, move: chess.Move, color: chess.Color) -> bool:
    from_file = chess.square_file(move.from_square)
    from_rank = chess.square_rank(move.from_square)
    to_file = chess.square_file(move.to_square)
    to_rank = chess.square_rank(move.to_square)

    direction = 1 if color == chess.WHITE else -1

    if abs(to_file - from_file) != 1:
        return False

    if to_rank - from_rank != direction:
        return False

    captured_piece = board.piece_at(move.to_square)
    return captured_piece == chess.Piece(chess.PAWN, not color)


def is_legal_pawn_advance_move(board: chess.Board, move: chess.Move) -> bool:
    piece = board.piece_at(move.from_square)

    if piece != chess.Piece(chess.PAWN, board.turn):
        return False

    if move.promotion is not None:
        return False

    return is_forward_move(board, move, board.turn) or is_capture_move(board, move, board.turn)


def legal_pawn_advance_moves(board: chess.Board) -> list[chess.Move]:
    moves: list[chess.Move] = []

    for from_square in chess.SQUARES:
        piece = board.piece_at(from_square)

        if piece != chess.Piece(chess.PAWN, board.turn):
            continue

        from_file = chess.square_file(from_square)
        from_rank = chess.square_rank(from_square)
        direction = 1 if board.turn == chess.WHITE else -1

        possible_squares: list[chess.Square] = []

        one_step_rank = from_rank + direction
        two_step_rank = from_rank + 2 * direction

        if 0 <= one_step_rank <= 7:
            possible_squares.append(chess.square(from_file, one_step_rank))

        if 0 <= two_step_rank <= 7:
            possible_squares.append(chess.square(from_file, two_step_rank))

        for file_change in [-1, 1]:
            capture_file = from_file + file_change
            capture_rank = from_rank + direction

            if 0 <= capture_file <= 7 and 0 <= capture_rank <= 7:
                possible_squares.append(chess.square(capture_file, capture_rank))

        for to_square in possible_squares:
            move = chess.Move(from_square, to_square)

            if is_legal_pawn_advance_move(board, move):
                moves.append(move)

    return moves


def pawn_reached_end(board: chess.Board) -> chess.Color | None:
    for square in chess.SquareSet(chess.BB_RANK_8):
        if board.piece_at(square) == chess.Piece(chess.PAWN, chess.WHITE):
            return chess.WHITE

    for square in chess.SquareSet(chess.BB_RANK_1):
        if board.piece_at(square) == chess.Piece(chess.PAWN, chess.BLACK):
            return chess.BLACK

    return None


def pawn_advance_result(board: chess.Board) -> WinnerColor:
    # set winner if a pawn reached the end of the board
    winner = pawn_reached_end(board)
    if winner is not None:
        # there's a winner due to a pawn reaching the end of the board
        if winner == chess.WHITE:
            return "White"
        else:
            return "Black"
    else:
        # no pawn has reached the end of the board
        # check other end game conditions
        if count_pawns(board, chess.WHITE) == 0:
            return "Black"
        elif count_pawns(board, chess.BLACK) == 0:
            return "White"

    if len(legal_pawn_advance_moves(board)) == 0:
        return "Tie"

    return None


def try_move(board: chess.Board, move_text: str) -> tuple[bool, str]:
    try:
        move = chess.Move.from_uci(move_text)
    except ValueError:
        return False, "Invalid move format. Use moves like e2e4 or d7d5."

    if not is_legal_pawn_advance_move(board, move):
        return False, "Illegal move."

    board.push(move)

    result = pawn_advance_result(board)
    if result is not None:
        if result == "Tie":
            return True, "Tie game!"
        elif result == "White":
            return True, "White wins!"
        else:
            return True, "Black wins!"

    return True, "Move played."

# abstract class for bot implementation
# takes in a board, outputs a move
class PawnAdvanceBot:
    def make_move(self, chess_board: chess.Board) -> chess.Move:
        raise NotImplementedError("Your bot needs to figure out how to make a move!")

# If you run this code, you can play a game of Pawn Advance against yourself in the terminal. Just enter moves (like e2e4) and see how the game unfolds!
# the `if __name__ == "__main__":` makes it so that when other scripts import this file, they don't accidentally start a game in the terminal just by running an import
if __name__ == "__main__":
    board = make_pawn_advance_board()

    while True:
        print(board)
        print("Turn:", "White" if board.turn == chess.WHITE else "Black")
        print("Legal moves:", [move.uci() for move in legal_pawn_advance_moves(board)])

        move_text = input("Move: ")
        ok, message = try_move(board, move_text)
        print(message)
        print()

        if "wins" in message or "Tie" in message:
            break # this command makes the code stop running the while loop
