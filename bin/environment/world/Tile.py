from environment.grid.Piece import Piece


class Tile(Piece):
    def __init__(self, piece, image, cost):
        self.image = image
        self.cost = cost
        super().__init__(piece.location, piece.position)
