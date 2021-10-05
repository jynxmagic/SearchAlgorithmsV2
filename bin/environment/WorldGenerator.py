from environment.world.World import World
from random import random
from images.ImageLoader import ImageLoader

class WorldGenerator:
    images = []

    def create_world(self):
        world = World()
        grid = world.get_grid()

        self.images = ImageLoader().getAllImages()

        for piece in grid:
            piece = grid[piece]
            t=random()
            if(t<0.8):
                walkable=True
            else:
                walkable=False
            image = self.get_image(walkable)
            world.create_tile(piece, walkable, image)

        return world

    def get_image(self, walkable):
        if walkable:
            return self.images[0]
        else:
            return self.images[1]
        return self.images[0]
