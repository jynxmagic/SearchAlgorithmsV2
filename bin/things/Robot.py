from images.ImageLoader import ImageLoader
from things.Thing import Thing


class Robot(Thing):
    def __init__(self):
        self.image = ImageLoader().get_robot_image()
        super().__init__()
