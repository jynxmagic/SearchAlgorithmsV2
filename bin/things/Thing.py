from random import randint

from Config import Config
from images.ImageLoader import ImageLoader


class Thing:
    def __init__(self):
        maxWidth = Config.WIDTH
        maxHeight = Config.HEIGHT
        tileSize = Config.TILE_SIZE
        locationX = randint(0, int(maxWidth / tileSize) - 1)
        locationY = randint(0, int(maxHeight / tileSize) - 1)
        self.location = [locationX, locationY]
        self.position = [locationX * tileSize, locationY * tileSize]
