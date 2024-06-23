from model.box_lid import BoxLid
from model.tile_bag import TileBag
from model.central_factory import CentralFactory
from model.player_board import PlayerBoard
from model.factory import Factory
from enums.tile_color import TileColor

class State:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.factories = [Factory() for _ in range(5)]
        self.central_factory = CentralFactory()
        self.box_lid = BoxLid()
        self.player1.board = PlayerBoard(self.box_lid)
        self.player2.board = PlayerBoard(self.box_lid)
        self.tile_bag = TileBag(self.box_lid)
        self.current_player = player1
        self.round_number = 1
        self.players = [player1, player2]
        self.game_over = False
        self.winner = None
