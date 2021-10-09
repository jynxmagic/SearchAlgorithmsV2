from random import randint
from images.ImageLoader import ImageLoader


class Thing:
    def __init__(self):
        maxWidth = 1920
        maxHeight = 1080
        tileSize = 64
        locationX = randint(0, int(maxWidth / 64) - 1)
        locationY = randint(0, int(maxHeight / 64) - 1)
        self.location = [locationX, locationY]
        self.position = [locationX * 64, locationY * 64]
