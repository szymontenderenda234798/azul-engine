from model.starting_player_tile import StartingPlayerTile
from model.state import State
from visualizer import Visualizer
from enums.tile_color import TileColor
import numpy as np
from model.random_player import RandomPlayer

class GameEngine:
    def __init__(self, print_enabled=False, visualize=False):
        self.print_enabled = print_enabled
        self.visualize = visualize
        self.visualizer = Visualizer()

        self.factory_count = 5
        self.color_count = 5
        self.pattern_lines = 6
        self.action_space_size = (self.factory_count + 1) * self.color_count * self.pattern_lines

    def setup_game(self, player1, player2):
        state = State(player1=player1, player2=player2)
        for factory in state.factories:
            factory.add_tiles(state.tile_bag.draw_tiles(4))
        return state
    
    def play_game(self, player1, player2):
        if self.print_enabled:
            print("Starting the game...")
            state = self.setup_game(player1=player1, player2=player2)
        while not state.game_over:
            if self.print_enabled:
                print(f"\n-------------------------------------\nRound {state.round_number}\n-------------------------------------")
            state = self.play_round(state)
        self.print_final_scores(state)
        return state

    def play_round(self, state):
        while True:
            state = self.play_turn(state)
            # Check for end of round condition
            if self.check_if_round_is_over(state):
                state = self.end_round(state)
                return state  # End the round
            
    def check_if_round_is_over(self, state):
        return all(not factory.tiles for factory in state.factories) and not state.central_factory.tiles

    
    def play_turn(self, state):
        if self.visualize:
            self.visualizer.draw_game_state(state)
        self.count_tiles_in_game(state)
        if self.print_enabled:
            print(f"\n-------------------------------------\n{state.current_player.name}'s turn\n-------------------------------------")
        self.print_game_state(state)
        factory_index, selected_color, pattern_line_index = state.current_player.make_decision(state)

        selected_factory = state.central_factory if factory_index == -1 else state.factories[factory_index]
        
        if any(isinstance(tile, StartingPlayerTile) for tile in selected_factory.tiles):
            if self.print_enabled:
                print("Starting player marker taken!")
            selected_factory.starting_player_marker_taken = True
            for tile in selected_factory.tiles:
                if isinstance(tile, StartingPlayerTile):
                    selected_factory.tiles.remove(tile)
                    break
            state.current_player.board.place_starting_player_tile_on_floor_line()

        # Applying the decisions
        selected_tiles = selected_factory.remove_and_return_tiles_of_color(selected_color)
        remaining_tiles = selected_factory.get_and_clear_remaining_tiles()
        state.central_factory.add_tiles(remaining_tiles)
        state.current_player.place_tile_in_pattern_line(selected_color, pattern_line_index, len(selected_tiles))
        if self.print_enabled:
            print(f"{state.current_player.name} placed {len(selected_tiles)} {selected_color.name} tiles in pattern line {pattern_line_index + 1}.")

        state = self.move_current_player(state)
        self.count_tiles_in_game(state)
        return state
    
    def finish_game_randomly(self, state):
        while not state.game_over:
            state = self.play_round_randomly(state)
        self.print_final_scores(state)
        return state
    
    def play_round_randomly(self, state):
        while True:
            state = self.play_turn_randomly(state)
            # Check for end of round condition
            if self.check_if_round_is_over(state):
                state = self.end_round(state)
                return state
        
    def play_turn_randomly(self, state):
        factory_index, selected_color, pattern_line_index = self.make_random_decision(state)

        selected_factory = state.central_factory if factory_index == -1 else state.factories[factory_index]
        
        if any(isinstance(tile, StartingPlayerTile) for tile in selected_factory.tiles):
            if self.print_enabled:
                print("Starting player marker taken!")
            selected_factory.starting_player_marker_taken = True
            for tile in selected_factory.tiles:
                if isinstance(tile, StartingPlayerTile):
                    selected_factory.tiles.remove(tile)
                    break
            state.current_player.board.place_starting_player_tile_on_floor_line()

        # Applying the decisions
        selected_tiles = selected_factory.remove_and_return_tiles_of_color(selected_color)
        remaining_tiles = selected_factory.get_and_clear_remaining_tiles()
        state.central_factory.add_tiles(remaining_tiles)
        state.current_player.place_tile_in_pattern_line(selected_color, pattern_line_index, len(selected_tiles))
        if self.print_enabled:
            print(f"{state.current_player.name} placed {len(selected_tiles)} {selected_color.name} tiles in pattern line {pattern_line_index + 1}.")

        state = self.move_current_player(state)
        self.count_tiles_in_game(state)
        return state
    
    def make_random_decision(self, state):
        random_player = RandomPlayer("random placeholder decision maker")
        factory_index, selected_color, pattern_line_index = random_player.make_decision(state)
        return factory_index, selected_color, pattern_line_index
    
    def get_next_state(self, state, action):
        factory_index, selected_color, pattern_line_index = action

        selected_factory = state.central_factory if factory_index == -1 else state.factories[factory_index]

        if any(isinstance(tile, StartingPlayerTile) for tile in selected_factory.tiles):
            if self.print_enabled:
                print("Starting player marker taken!")
            selected_factory.starting_player_marker_taken = True
            for tile in selected_factory.tiles:
                if isinstance(tile, StartingPlayerTile):
                    selected_factory.tiles.remove(tile)
                    break
            state.current_player.board.place_starting_player_tile_on_floor_line()

        # Applying the decisions
        selected_tiles = selected_factory.remove_and_return_tiles_of_color(selected_color)
        remaining_tiles = selected_factory.get_and_clear_remaining_tiles()
        state.central_factory.add_tiles(remaining_tiles)
        state.current_player.place_tile_in_pattern_line(selected_color, pattern_line_index, len(selected_tiles))
        if self.print_enabled:
            print(f"{state.current_player.name} placed {len(selected_tiles)} {selected_color.name} tiles in pattern line {pattern_line_index + 1}.")

        state = self.move_current_player(state)
        self.count_tiles_in_game(state)
        return state
    
    def end_round(self, state):
        """Handle the end of a round: Move tiles, score points, and check game over condition."""
        if self.print_enabled:
            print(f"\n-------------------------------------\nEND OF ROUND {state.round_number}\n-------------------------------------")
        for player in state.players:
            if self.print_enabled:
                print(f"\n{player.name} board before moving, but after last move:")
                player.board.print_board()        
        if self.print_enabled:
            print(f"\n-------------------------------------\nSCORING AND MOVING TO WALL\n-------------------------------------")
        for player in state.players:
            self.count_tiles_in_game(state)
            score = player.move_tiles_to_wall_and_score()  # Assuming this method returns the score for the round
            self.count_tiles_in_game(state)
            player.score += score  # Assuming each player has a 'score' attribute
            if self.print_enabled:
                print(f"\n{player.name} scored {score} points this round.")
                print(f"{player.name} board after moving:")
                player.board.print_board()
        state.round_number += 1
        self.count_tiles_in_game(state)
        state = self.check_game_over(state)
        state = self.set_new_starting_player(state)
        state = self.refresh_factories(state)
        state = self.game_over_score_and_setting_winner(state)
        return state
    
    def game_over_score_and_setting_winner(self, state):
        if state.game_over:
            highest_score = -float('inf')
            winner = None
            for player in state.players:
                player.score += player.score_end_game_points()  # Assuming this method returns the end game points
                if self.print_enabled:
                    print(f"\n{player.name} scored {player.score} points.")
                if player.score > highest_score:
                    highest_score = player.score
                    winner = player
            state.winner = winner
            if self.print_enabled:
                print(f"\nThe winner is {winner.name} with a score of {highest_score}!")
        return state

            
    def is_state_terminal(self, state):
        return state.game_over
    
    def get_result(self, state):
        if state.winner is not None:
            return 1 if state.winner == state.current_player else -1
        pass

    def check_game_over(self, state):
        for player in state.players:
            if player.has_completed_row_on_wall():
                state.game_over = True
        return state

    def print_game_state(self, state):
        if self.print_enabled:
            print("\nCurrent Game State:\n")

        # Show available factories
        for i, factory in enumerate(state.factories, start=1):
            if self.print_enabled:
                print(f"Factory {i}: {[tile.name for tile in factory.tiles]}")
        # Show the central factory
        if self.print_enabled:
            print(f"Central Factory: {[tile.name for tile in state.central_factory.tiles]}\n")

        # Show players' boards
        if self.print_enabled:
            for player in state.players:
                player.print_board()
                print("")  # Extra newline for spacing

    def move_current_player(self, state):
        state.current_player = state.player1 if state.current_player == state.player2 else state.player2
        return state


    def set_new_starting_player(self, state):
        for player in state.players:
            if player.has_starting_player_tile():
                state.current_player = player                
        return state

    def refresh_factories(self, state):
        """Refill the factories with tiles from the tile bag for the new round."""
        state.central_factory.clear()  # Clear the central factory for the new round
        state.central_factory.add_starting_player_tile()  # Add the starting player tile to the central factory
        for factory in state.factories:
            factory.add_tiles(state.tile_bag.draw_tiles(4))
        return state

    def print_final_scores(self, state):
        """Print the final scores of all players."""
        if self.print_enabled:
            print(f"\n-------------------------------------\nFINAL SCORES\n-------------------------------------")
            for player in state.players:
                print(f"{player.name}: {player.score} points")
        
        # Determine the winner (could be multiple in case of a tie)
        highest_score = max(player.score for player in state.players)
        winners = [player.name for player in state.players if player.score == highest_score]
        if self.print_enabled:
            if len(winners) > 1:
                print(f"Tie between: {', '.join(winners)}")
            else:
                print(f"Winner: {winners[0]}")

    def count_tiles_in_game(self, state):
        """Count the number of tiles in the factories, central factory, tile bag, and players' boards."""
        factory_tile_count = sum(len(factory.tiles) for factory in state.factories)
        central_factory_tile_count = len([tile for tile in state.central_factory.tiles if not isinstance(tile, StartingPlayerTile)])
        tile_bag_tile_count = len(state.tile_bag.tiles)
        box_lid_tile_count = len(state.box_lid.tiles)
        players_tile_count = sum(player.board.count_placed_tiles() for player in state.players)
        tile_count_sum = factory_tile_count + central_factory_tile_count + tile_bag_tile_count + players_tile_count + box_lid_tile_count

        if tile_count_sum != 100:
            raise ValueError("Total tile count is not 100.")

        return tile_count_sum
    
    def get_valid_moves(self, state):
        valid_moves = [False] * self.action_space_size  # 5 factories * 5 colors * 5 pattern lines + 5 factories * 5 colors + 1 central factory * 5 colors

        # Check factories and central factory
        for factory_index, factory in enumerate(state.factories + [state.central_factory]):
            for color_index, color in enumerate(TileColor):
                if any(tile.color == color for tile in factory.tiles):
                # Check if the color can be placed in any of the pattern lines
                    not_fully_occupied_lines_indeces = state.current_player.board.get_not_fully_occupied_pattern_lines()
                    for pattern_line_index in not_fully_occupied_lines_indeces:
                        pattern_line = state.current_player.board.pattern_lines[pattern_line_index]
                        if all(tile is None or tile.color == color for tile in pattern_line):
                            action_index = self.action_to_index(factory_index, color_index, pattern_line_index)
                            valid_moves[action_index] = True
                    action_index = self.action_to_index(factory_index, color_index, 5)
                    valid_moves[action_index] = True

        assert len(valid_moves) == self.action_space_size
        return np.array([int(valid) for valid in valid_moves])
    
    def action_to_index(self, factory_index, color_index, pattern_line_index):
        if factory_index == -1:  # Central factory
            factory_index = self.factory_count  # Use the last index for central factory
        # print(f"Action: Take {list(TileColor)[color_index].name} tiles from factory {factory_index + 1 if factory_index != self.factory_count else 'central'} and place them in pattern line {pattern_line_index + 1}")
        return factory_index * self.color_count * self.pattern_lines + color_index * self.pattern_lines + pattern_line_index
    
    def action_to_index(self, factory_index, color_index, pattern_line_index):
        if factory_index == -1:  # Central factory
            factory_index = self.factory_count  # Use the last index for central factory
        # print(f"Action: Take {list(TileColor)[color_index].name} tiles from factory {factory_index + 1 if factory_index != self.factory_count else 'central'} and place them in pattern line {pattern_line_index + 1}")
        return factory_index * self.color_count * self.pattern_lines + color_index * self.pattern_lines + pattern_line_index
    
    def index_to_action(self, index):
        factory_index = index // (self.color_count * self.pattern_lines)
        color_index = (index // self.pattern_lines) % self.color_count
        pattern_line_index = index % self.pattern_lines
        if factory_index == self.factory_count:  # Central factory
            factory_index = -1
        # print("INDEX TO ACTION METHOD")
        # print("The player took tiles of color", list(TileColor)[color_index].name, "from factory", factory_index + 1 if factory_index != -1 else 'central', "and placed them in pattern line", pattern_line_index + 1)
        return factory_index, list(TileColor)[color_index], pattern_line_index