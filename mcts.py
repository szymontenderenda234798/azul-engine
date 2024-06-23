from copy import deepcopy
import random
from node import Node
from game_engine import GameEngine
from model.random_player import RandomPlayer
import numpy as np


class MCTS:
    def __init__(self, n_iter):
        self.game_engine = GameEngine(print_enabled=False, visualize=False)
        self.n_iter = n_iter

    def search(self, initial_state):
        root = Node(initial_state, self.game_engine)

        for _ in range(self.n_iter):
            node = self._select(root)
            if not self.game_engine.is_state_terminal(node.state):
                node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)

        return root.best_child(c_param=0).action_taken

    def _select(self, node):
        while node.is_fully_expanded() and not self.game_engine.is_state_terminal(node.state):
            node = node.best_child()
        return node

    def _expand(self, node):
        actions = np.where(node.actions_to_try == 1)[0]
        random_action_index = random.choice(actions)
        action = self.game_engine.index_to_action(random_action_index)
        next_state = self.game_engine.get_next_state(deepcopy(node.state), action)
        node.actions_to_try[random_action_index] = 0
        return node.add_child(next_state, action)
    
    def _simulate(self, node):
        current_state = deepcopy(node.state)
        state = self.game_engine.finish_game_randomly(current_state)
        print("simulation over")
        return self.game_engine.get_result(state)

    def _backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent