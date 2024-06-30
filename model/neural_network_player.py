from model.player import Player
from nn_interface import NNInterface

class NeuralNetworkPlayer(Player):

    def __init__(self, name, nn):
        super().__init__(name)
        self.nn = nn
        self.nn_interface = NNInterface()

    def make_decision(self, state):
        """
        Uses the neural network to make a decision based on the current game state.
        """
        input_data = self.nn_interface.game_state_to_network_input(state)
        output = self.nn.activate(input_data)
        valid_moves = self.nn_interface.game_engine.get_valid_moves(state)
        selected_action_index = self.nn_interface.select_action_from_network_output(output, valid_moves)
        factory_index, selected_color, pattern_line_index = self.nn_interface.game_engine.index_to_action(selected_action_index)
        return factory_index, selected_color, pattern_line_index