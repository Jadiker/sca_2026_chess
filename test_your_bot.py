'''
Use this script to test how your bot performs.

Uppercase P = white pawns
Lowercase p = black pawns
'''
from gen_pawn_advance import *
# choose one of these as the enemy bot to test against
from example_bots import RandomPawnAdvanceBot, CapturePawnAdvanceBot
from your_bot import YourPawnAdvanceBot


your_bot = YourPawnAdvanceBot()
# Use either `enemy_bot = RandomPawnAdvanceBot()` or `enemy_bot = CapturePawnAdvanceBot()` depending on which bot you want to test against
# Surprisingly, RandomPawnAdvanceBot is actually a stronger opponent than CapturePawnAdvanceBot
enemy_bot = RandomPawnAdvanceBot()
# How many games you want the bots to play against each other.
games_to_play = 300

wins = 0
losses = 0
ties = 0
for game_index in range(games_to_play):
    print(f"Starting game {game_index + 1}...")
    # choose the first player randomly
    first_player = random.choice([your_bot, enemy_bot])
    if first_player == your_bot:
        print("Your bot is playing as white and goes first!")
        second_player = enemy_bot
    else:
        print("Your bot is playing as black and goes second!")
        second_player = your_bot


    # set up the game
    current_player = first_player
    board = make_pawn_advance_board()
    result = pawn_advance_result(board)
    # keep playing the game until there's a result (win for white, win for black, or tie)
    while result is None:
        if current_player == your_bot:
            bot_name = "Your bot"
        else:
            bot_name = "Enemy bot"

        print(f"{bot_name}'s turn:")
        print(board)
        # make a move on the copy of the board so that the bot can't accidentally mess with the real board
        move = current_player.make_move(board.copy())
        if move in legal_pawn_advance_moves(board):
            # make the move on the real board
            board.push(move)
            # see if there's a winner (or tie) after that move
            result = pawn_advance_result(board)
            print(f"{bot_name} made move: {move}")
        else:
            print(f"{bot_name} made an illegal move: {move}.")
            # if a bot makes an illegal move, they lose immediately
            if your_bot == current_player:
                if your_bot == first_player:
                    result = BLACK_WINNER
                else:
                    result = WHITE_WINNER
            else:
                # enemy bot made an illegal move
                if enemy_bot == first_player:
                    result = BLACK_WINNER
                else:
                    result = WHITE_WINNER


    # display the results
    print(board)
    if (result == WHITE_WINNER and your_bot == first_player) or (result == BLACK_WINNER and your_bot == second_player):
        print("Your bot won!")
        wins += 1
    elif result == TIE_WINNER:
        print("The game ended in a tie!")
        ties += 1
    else:
        print("Your bot lost!")
        losses += 1

print(f"After {games_to_play} games, your bot had {wins} wins ({round(wins/games_to_play*100, 2)}%), {losses} losses ({round(losses/games_to_play*100, 2)}%), and {ties} ties ({round(ties/games_to_play*100, 2)}%).")

def compute_probability(wins: int, losses: int, ties: int) -> float:
    # Written by ChatGPT
    """Return P(your bot is better than enemy bot).

    Assumptions:
    - Each game is independent.
    - The win/loss/tie probabilities are fixed.
    - Prior over (win, loss, tie) probabilities is uniform Dirichlet(1, 1, 1).
    - "Better" means true win probability > true loss probability.
    - Ties are treated as neutral evidence.
    """

    if wins < 0 or losses < 0 or ties < 0:
        raise ValueError("wins, losses, and ties must be nonnegative")

    import math

    # Posterior:
    # p_win, p_loss, p_tie ~ Dirichlet(wins + 1, losses + 1, ties + 1)
    #
    # Ignoring ties:
    # q = p_win / (p_win + p_loss) ~ Beta(wins + 1, losses + 1)
    #
    # We want P(q > 0.5).

    a = wins + 1
    b = losses + 1

    # For q ~ Beta(a, b):
    # P(q > 0.5) = sum_{k=0}^{a-1} C(a+b-1, k) * 0.5^(a+b-1)
    n = a + b - 1

    favorable = sum(math.comb(n, k) for k in range(a))
    total = 2 ** n

    return favorable / total

print(f"Based on the results, we estimate that the probability that your bot is better than the enemy bot is approximately {round(compute_probability(wins, losses, ties) * 100, 4)}%")
