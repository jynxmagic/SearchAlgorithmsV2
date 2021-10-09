from random import random

from images.ImageLoader import ImageLoader

from environment.world.World import World


class WorldGenerator:
    images = []

    def create_world(self):
        world = World()
        grid = world.get_grid()

        self.images = ImageLoader().get_all_env_images()

        print(self.images)

        for piece in grid:
            piece = grid[piece]
            t = random()
            if t < 0.8:
                cost = 1
            else:
                cost = 0
            image = self.get_image(cost)
            world.create_tile(piece, cost, image)

        return world

    def get_image(self, walkable):
        if walkable == 1:
            return self.images[0]
        else:
            return self.images[1]
