from PIL import ImageTk, Image
from tkinter import Label
from pathlib import Path
import glob

class ImageLoader:

    def __init__(self):
        self.images = [ImageTk.PhotoImage(file=fname) for fname in glob.glob(str(Path().resolve())+"\images\\tiles\*.png")]

    def getAllImages(self):
        return self.images
    