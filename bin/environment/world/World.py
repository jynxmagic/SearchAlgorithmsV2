from environment.grid.Grid import Grid
from environment.world.Tile import Tile

class World(Grid):
    tiles = dict()

    def __init__(self):
        self.grid = self.generate_grid()

    def get_grid(self):
        return self.grid

    def create_tile(self, piece, passable, image):
        tile = Tile(piece, image, passable)
        self.tiles[str(piece.location[0])+"x"+str(piece.location[1])] = tile