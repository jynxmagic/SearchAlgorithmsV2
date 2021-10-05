from PIL import ImageTk, Image
from tkinter import Label
from pathlib import Path
import glob

class ImageLoader:

    def __init__(self):
        self.env_images = [ImageTk.PhotoImage(file=fname) for fname in glob.glob(str(Path().resolve())+"\\bin\images\\tiles\world_tiles\*.png")]
        
        robot_fpath = str(Path().resolve())+'\\bin\images\\tiles\\robot_tiles\\robot.png'

        robot_image = Image.open(robot_fpath)
        resized_r_image = robot_image.resize((64,64))
        self.robot_image = ImageTk.PhotoImage(resized_r_image)


    def getAllEnvImages(self):
        return self.env_images
    