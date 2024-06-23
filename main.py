from game_engine import GameEngine
from model.human_player import HumanPlayer
from model.random_player import RandomPlayer
from model.mcts_player import MCTSPlayer

if __name__ == "__main__":
    game_engine = GameEngine(print_enabled=True, visualize=False)
    game_engine.play_game(player1=MCTSPlayer("MCTS Player"), player2=RandomPlayer("Player 2"))
    
