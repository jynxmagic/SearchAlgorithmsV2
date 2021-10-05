from tkinter import *
from images.ImageLoader import ImageLoader
from environment.WorldGenerator import WorldGenerator


def draw_world(world):
    #background tiles
    for tile in world.tiles:
        key = tile
        tile = world.tiles[key]

        print(tile.location[0])
        label = Label(image=tile.image)
        label.place(x=tile.position[0],y=tile.position[1])
    

root = Tk()
root.configure(background="#427439")
worldgen = WorldGenerator()
world = worldgen.create_world()


canvas_height=1080
canvas_width=1920

w = Canvas(root, 
           width=canvas_width,
           height=canvas_height)
w.pack()

draw_world(world)



mainloop()