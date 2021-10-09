from things.Thing import Thing
from images.ImageLoader import ImageLoader


class Objective(Thing):
    def __init__(self):
        self.image = ImageLoader().get_objective_image()
        super().__init__()
