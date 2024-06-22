from model.factory import Factory
from model.tile_bag import TileBag
from model.central_factory import CentralFactory
from model.starting_player_tile import StartingPlayerTile
from model.box_lid import BoxLid
from model.random_player import RandomPlayer
from model.state import State

class GameEngine:
    def __init__(self, print_enabled=False):
        self.print_enabled = print_enabled

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

    def play_round(self, state):
        while True:
            state = self.play_turn(state)
            # Check for end of round condition
            if all(not factory.tiles for factory in state.factories) and not state.central_factory.tiles:
                state = self.end_round(state)
                return state  # End the round

    
    def play_turn(self, state):
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
        if state.game_over:
            for player in state.players:
                player.score += player.score_end_game_points()  # Assuming this method returns the end game points
        return state

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
