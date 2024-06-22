from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.random_player import RandomPlayer

if __name__ == "__main__":
    game_engine = GameEngine(print_enabled=True)
    game_engine.play_game(player1=RandomPlayer("Player 1"), player2=RandomPlayer("Player 2"))