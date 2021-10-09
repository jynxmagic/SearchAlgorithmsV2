from PIL import ImageTk, Image
from tkinter import Label
from pathlib import Path
import glob


class ImageLoader:
    def _tk_loader(self, path):
        im = Image.open(path)
        resized_im = im.resize((64, 64))
        im_tk = ImageTk.PhotoImage(resized_im)
        return im_tk

    def get_robot_image(self):
        robot_fpath = (
            str(Path().resolve()) + "\\bin\images\\tiles\\robot_tiles\\robot.png"
        )
        self.robot_image = self._tk_loader(robot_fpath)
        return self.robot_image

    def get_objective_image(self):
        obj_fpath = (
            str(Path().resolve()) + "\\bin\images\\tiles\\objective_tiles\\male.png"
        )
        self.objective_image = self._tk_loader(obj_fpath)
        return self.objective_image

    def get_all_env_images(self):
        self.env_images = [
            ImageTk.PhotoImage(file=fname)
            for fname in glob.glob(
                str(Path().resolve()) + "\\bin\images\\tiles\world_tiles\*.png"
            )
        ]
        return self.env_images
