from environment.grid.Piece import Piece
class Tile(Piece):
    def __init__(self, piece, image, passable):
        self.image = image
        self.passable = passable
        super().__init__(piece.location, piece.position)
