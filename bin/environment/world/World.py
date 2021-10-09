import numpy as np
from environment.grid.Grid import Grid
from environment.world.Tile import Tile


class World(Grid):
    tiles = dict()

    def __init__(self):
        self.grid = self.generate_grid()
        self.np_tiles = np.zeros(
            (int(self.gridWidth / 64), int(self.gridHeight / 64) + 1)
        )

    def get_grid(self):
        return self.grid

    def create_tile(self, piece, passable, image):
        print(piece.location)
        self.np_tiles[int(piece.location[0]), int(piece.location[1])] = passable
        tile = Tile(piece, image, passable)
        self.tiles[str(piece.location[0] * 6072 + piece.location[1])] = tile
