import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from enums.tile_color import TileColor
from model.starting_player_tile import StartingPlayerTile  # Assuming this is the class for the starting player tile

class Visualizer:
    def __init__(self):
        # Map TileColor to actual colors
        self.color_map = {
            TileColor.BLUE: 'blue',
            TileColor.YELLOW: 'yellow',
            TileColor.RED: 'red',
            TileColor.BLACK: 'black',
            TileColor.WHITE: 'white',
            'None': 'grey'  # For empty spots
        }
        self.starting_player_tile_color = 'orange'  # Define color for starting player tile

    def draw_factory(self, ax, factory, position):
        x, y = position
        factory_radius = 1
        ax.add_patch(Circle((x, y), factory_radius, edgecolor='black', facecolor='lightgrey'))
        for i, tile in enumerate(factory.tiles):
            tile_color = self.color_map.get(tile.color, 'grey')
            angle = i * (360 / len(factory.tiles))
            tile_x = x + 0.5 * factory_radius * np.cos(np.radians(angle))
            tile_y = y + 0.5 * factory_radius * np.sin(np.radians(angle))
            ax.add_patch(Circle((tile_x, tile_y), 0.2, color=tile_color))

    def draw_central_factory(self, ax, central_factory, position):
        x, y = position
        central_factory_radius = 2
        ax.add_patch(Circle((x, y), central_factory_radius, edgecolor='black', facecolor='lightgrey'))
        for i, tile in enumerate(central_factory.tiles):
            if isinstance(tile, StartingPlayerTile):
                tile_color = self.starting_player_tile_color
            else:
                tile_color = self.color_map.get(tile.color, 'grey')
            angle = i * (360 / len(central_factory.tiles))
            tile_x = x + 0.75 * central_factory_radius * np.cos(np.radians(angle))
            tile_y = y + 0.75 * central_factory_radius * np.sin(np.radians(angle))
            ax.add_patch(Circle((tile_x, tile_y), 0.2, color=tile_color))

    def draw_pattern_lines(self, ax, pattern_lines, position):
        x, y = position
        for i, line in enumerate(pattern_lines):
            for j in range(i + 1):
                tile = line[j] if j < len(line) else None
                tile_color = self.color_map.get(tile.color, 'grey') if tile else 'grey'
                edgecolor = 'black' if tile else 'lightgrey'
                ax.add_patch(Rectangle((x + j * 0.5, y - i * 0.5), 0.5, 0.5, edgecolor=edgecolor, facecolor=tile_color))

    def draw_wall(self, ax, wall, wall_pattern, position):
        x, y = position
        for i, row in enumerate(wall):
            for j, tile in enumerate(row):
                tile_color = self.color_map.get(tile.color, 'grey') if tile else 'grey'
                pattern_color = self.color_map[wall_pattern[i][j]]
                if not tile:
                    ax.add_patch(Rectangle((x + j * 0.5, y - i * 0.5), 0.5, 0.5, edgecolor='black', facecolor=pattern_color, alpha=0.3))
                else:
                    ax.add_patch(Rectangle((x + j * 0.5, y - i * 0.5), 0.5, 0.5, edgecolor='black', facecolor=tile_color))

    def draw_floor_line(self, ax, floor_line, position):
        x, y = position
        max_floor_tiles = 7
        for i in range(max_floor_tiles):
            if i < len(floor_line):
                tile = floor_line[i]
                if isinstance(tile, StartingPlayerTile):
                    tile_color = self.starting_player_tile_color
                else:
                    tile_color = self.color_map.get(tile.color, 'grey')
            else:
                tile_color = 'grey'
            ax.add_patch(Rectangle((x + i * 0.5, y), 0.5, 0.5, edgecolor='black', facecolor=tile_color))

    def draw_score(self, ax, score, position):
        x, y = position
        rows = 5
        cols = 20
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                color = 'darkgrey' if index < score else 'lightgrey'
                ax.add_patch(Rectangle((x + col * 0.2, y - row * 0.2), 0.2, 0.2, edgecolor='black', facecolor=color))

    def draw_player_board(self, ax, board, score, position):
        pattern_lines_pos = (position[0], position[1])
        wall_pos = (position[0] + 3.5, position[1])
        floor_line_pos = (position[0], position[1] - 3)
        score_pos = (position[0], position[1] - 4.5)
        self.draw_pattern_lines(ax, board.pattern_lines, pattern_lines_pos)
        self.draw_wall(ax, board.wall, board.wall_pattern, wall_pos)
        self.draw_floor_line(ax, board.floor_line, floor_line_pos)
        self.draw_score(ax, score, score_pos)

    def draw_game_state(self, state):
        fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 18)
        
        # Draw factories
        factory_positions = [(2, 15), (5, 15), (8, 15), (11, 15), (14, 15)]
        for i, factory in enumerate(state.factories):
            self.draw_factory(ax, factory, factory_positions[i])
        
        # Draw central factory
        self.draw_central_factory(ax, state.central_factory, (8, 11))
        
        # Draw player 1 board
        self.draw_player_board(ax, state.player1.board, state.player1.score, (1, 7))
        
        # Draw player 2 board
        self.draw_player_board(ax, state.player2.board, state.player2.score, (9, 7))
        
        plt.axis('off')
        plt.show()  # Display the plot to the user

    def create_rgb_array(self, state):
        fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 18)
        
        # Draw factories
        factory_positions = [(2, 15), (5, 15), (8, 15), (11, 15), (14, 15)]
        for i, factory in enumerate(state.factories):
            self.draw_factory(ax, factory, factory_positions[i])
        
        # Draw central factory
        self.draw_central_factory(ax, state.central_factory, (8, 11))
        
        # Draw player 1 board
        self.draw_player_board(ax, state.player1.board, state.player1.score, (1, 7))
        
        # Draw player 2 board
        self.draw_player_board(ax, state.player2.board, state.player2.score, (9, 7))
        
        plt.axis('off')

        # Convert plot to RGB array
        fig.canvas.draw()
        width, height = fig.canvas.get_width_height()
        rgb_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        rgb_array = rgb_array.reshape((height, width, 3))
        plt.close(fig)
        return rgb_array
