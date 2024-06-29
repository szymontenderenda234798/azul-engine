from model.player import Player
from mcts import MCTS
import random
from model.starting_player_tile import StartingPlayerTile

class MCTSPlayer(Player):
    def __init__(self, name, n_iter=5, c_param=1.4):
        super().__init__(name)
        self.mcts = MCTS(n_iter, c_param)

    def make_decision(self, state):
        action = self.mcts.search(state)
        return action