import numpy as np
from enums.tile_color import TileColor
from model.starting_player_tile import StartingPlayerTile
from game_engine import GameEngine

class NNInterface:
    def __init__(self, enable_generation_logging=False):
        self.enable_generation_logging = enable_generation_logging
        self.game_engine = GameEngine(print_enabled=False, visualize=False)

    def game_state_to_network_input(self, state):
        """
        Transforms the current game state into the input format required by the neural network.
        """
        binary_array = []
        binary_array.extend(self.player_board_to_network_input(state.current_player.board))
        if state.current_player == state.player1:
            binary_array.extend(self.player_board_to_network_input(state.player2.board))
        else:
            binary_array.extend(self.player_board_to_network_input(state.player1.board))
        binary_array.extend(self.factories_to_network_input(state.factories))
        binary_array.extend(self.central_factory_to_network_input(state.central_factory))
        return binary_array

    def player_board_to_network_input(self, player_board):
        binary_array = []
        binary_array.extend(self.pattern_lines_to_network_input(player_board.pattern_lines))
        binary_array.extend(self.wall_to_network_input(player_board.wall))
        binary_array.extend(self.floor_line_to_network_input(player_board.floor_line))
        return binary_array

    def pattern_lines_to_network_input(self, pattern_lines):
        """
        Transforms the pattern line state into the input format required by the neural network.
        """
        binary_array = []

        # Iterate through each pattern line
        for line_index, line in enumerate(pattern_lines):
            # First, add 6 neurons for the first slot (5 for color, 1 for empty)
            if len(line) > 0 and line[0] is not None:  # If there's at least one tile in the line
                for color in TileColor:  # Add 1 for the tile's color, 0 for others
                    binary_array.append(1 if line[0].color == color else 0)
                binary_array.append(0)  # This line is not empty
            else:  # If the line is empty
                binary_array.extend([0, 0, 0, 0, 0, 1])  # All colors are 0, 'empty' neuron is 1
                
            # Now, add 1 neuron for each additional slot in the line, indicating occupancy
            for slot_index in range(1, line_index + 1):
                binary_array.append(1 if line[slot_index] is not None else 0)
                    
        return binary_array
    
    def wall_to_network_input(self, wall):
        """
        Transforms the wall state into a binary input format required by the neural network.
        Each spot on the 5x5 wall grid is represented by a binary value, resulting in a
        25-entry array. A value of 1 indicates that a tile is present in that spot, while 0
        indicates an empty spot.
        """
        binary_array = []

        # Assuming the wall is a 5x5 list of lists, with each inner list representing a row.
        for row in wall:
            for tile in row:
                binary_array.append(1 if tile is not None else 0)

        return binary_array
    
    def floor_line_to_network_input(self, floor_line):
        """
        Transforms the floor line state into the input format required by the neural network.
        """
        binary_array = []

        # Add 1 neuron for each tile in the floor line, indicating occupancy
        for i in range(8):
            binary_array.append(1 if i < len(floor_line) else 0)

        return binary_array
    
    def factories_to_network_input(self, factories):
        """
        Transforms the factories state into the input format required by the neural network.
        """
        binary_array = []

        for factory in factories:
            tiles = len(factory.tiles)
            if tiles > 0:
                for i in range(4):
                    if i < tiles:
                        for color in TileColor:
                            binary_array.append(1 if factory.tiles[i].color == color else 0)
                    else:
                        binary_array.extend([0, 0, 0, 0, 0])
            else:
                binary_array.extend([0] * 20)

        return binary_array
    
    def central_factory_to_network_input(self, central_factory):
        """
        Transforms the central factory state into the input format required by the neural network.
        """
        binary_array = []
        buffer = 0
        tiles = len(central_factory.tiles)
        if tiles == 0:
            binary_array.extend([0] * 136)
        else:
            if isinstance(central_factory.tiles[0], StartingPlayerTile):
                binary_array.append(1)
                tiles -= 1
                buffer = 1
            else:
                binary_array.append(0)
            for i in range(27):
                if i < tiles:
                    for color in TileColor:
                        binary_array.append(1 if central_factory.tiles[i + buffer].color == color else 0)
                else:
                    binary_array.extend([0] * 5)

        return binary_array
    
    def softmax(self, x):
        """
        Compute the softmax of a 1D array.
        """
        e_x = np.exp(x - np.max(x))  # Subtract max value for numerical stability
        return e_x / e_x.sum()

    def select_action_from_network_output(self, network_output, valid_moves):
        """
        Apply softmax to the network output, select an action based on the probabilities,
        and return the index of the selected action.
        """

        masked_output = np.where(valid_moves, network_output, -np.inf)  # Mask invalid moves

        # Apply softmax to get probabilities
        probabilities = self.softmax(masked_output)

        # Ensure probabilities sum to 1 after masking invalid moves
        probabilities /= probabilities.sum()

        # Select an index based on the probabilities
        selected_index = np.random.choice(len(probabilities), p=probabilities)

        return selected_index