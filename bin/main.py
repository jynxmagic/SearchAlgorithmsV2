from copy import deepcopy
from tkinter import Canvas, Label, Tk, mainloop

from environment.WorldGenerator import WorldGenerator
from images.ImageLoader import ImageLoader
from search_algorithms.tree.TDepthFirstSearch import TDepthFirstSearch
from things.Objective import Objective
from things.Robot import Robot


def add_label(v):
    label = Label(image=v.image)
    label.photo = v.image
    label.place(x=v.position[0], y=v.position[1])


def draw_world(world, robot, objective):
    # background tiles
    for tile in world.tiles:
        key = tile
        tile = world.tiles[key]
        print(tile)
        add_label(tile)
    add_label(robot)
    add_label(objective)


def main():
    root = Tk()
    root.configure(background="#427439")
    worldgen = WorldGenerator()
    world = worldgen.create_world()

    canvas_height = 1080
    canvas_width = 1920

    w = Canvas(root, width=canvas_width, height=canvas_height)
    w.pack()

    robot = Robot()
    objective = Objective()
    draw_world(world, robot, objective)
    mainloop()

    initial_state = world.np_tiles.copy()
    initial_state[robot.location[0], robot.location[1]] = 2
    initial_state[objective.location[0], objective.location[1]] = 3

    objective_state = world.np_tiles.copy()
    objective_state[robot.location[0], robot.location[1]] = 1
    objective_state[objective.location[0], objective.location[1]] = 2

    dfs = TDepthFirstSearch(initial_state, objective_state, objective.location)
    print(dfs.solve())



if __name__ == "__main__":
    main()
