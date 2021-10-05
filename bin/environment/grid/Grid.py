from environment.grid.Piece import Piece

class Grid:
    pieces = dict()
    pieceSize = 64

    gridWidth = 1920
    gridHeight = 1080

    def generate_grid(self):
        x = y = 0
        while x < self.gridWidth:
            while y < self.gridHeight:
                x_pos = 0 if x == 0 else x / self.pieceSize # (0,1),(0,2), ...  , (0,x)
                y_pos = 0 if y == 0 else y / self.pieceSize # (1,0),(2,0), ... , (y,0) -> (x,y)

                pos = [x_pos, y_pos]
                location = [x,y]
                piece = Piece(pos,location)
                self.pieces[str(x_pos)+"x"+str(y_pos)] = piece
                y += self.pieceSize
            x += self.pieceSize
            y = 0

        return self.pieces

