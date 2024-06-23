import math
import numpy as np
from game_engine import GameEngine

class Node:
    def __init__(self, state, game_engine, parent=None):
        self.state = state
        self.game_engine = game_engine
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.actions_to_try = self.game_engine.get_valid_moves(self.state)

    def is_fully_expanded(self):
        return np.all(self.actions_to_try == 0)

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def add_child(self, state, action_index):
        child_node = Node(state, self.game_engine, parent=self)
        self.children.append(child_node)
        self.actions_to_try[action_index] = 0
        return child_node