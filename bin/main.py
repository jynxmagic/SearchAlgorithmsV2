from tkinter import *
from images.ImageLoader import ImageLoader
from environment.WorldGenerator import WorldGenerator
from things.Robot import Robot

def draw_world(world):
    #background tiles
    for tile in world.tiles:
        key = tile
        tile = world.tiles[key]

        label = Label(image=tile.image)
        label.photo = tile.image
        label.place(x=tile.position[0],y=tile.position[1])

    #robot
    robot = Robot()
    robotLabel = Label(image=robot.image)
    robotLabel.photo = robot.image
    robotLabel.place(x=robot.position[0],y=robot.position[1])

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