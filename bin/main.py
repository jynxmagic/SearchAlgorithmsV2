from copy import deepcopy
from tkinter import Canvas, Label, Tk, mainloop

from Config import Config
from environment.WorldGenerator import WorldGenerator
from images.ImageLoader import ImageLoader
from search_algorithms.graph.GBreadthFirstSearch import GBreadthFirstSearch
from search_algorithms.graph.GDepthFirstSearch import GDepthFirstSearch
from search_algorithms.tree.TBreadthFirstSearch import TBreadthFirstSearch
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

def print_path(node):
    i=0
    for node in node.path():
        print(i, node.robot_location)
        i+=1

def main():
    root = Tk()
    root.configure(background="#427439")
    worldgen = WorldGenerator()
    world = worldgen.create_world()

    canvas_height = Config.HEIGHT
    canvas_width = Config.WIDTH

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

    tbreadth_first_search = TBreadthFirstSearch(initial_state, objective_state, objective.location)
    tbfs_result = tbreadth_first_search.solve()

    tdepth_first_search = TDepthFirstSearch(initial_state, objective_state, objective.location)
    tdfs_result = tdepth_first_search.solve()


    gbreadthfirstsearch = GBreadthFirstSearch(initial_state, objective_state, objective.location)
    gbfs_res = gbreadthfirstsearch.solve()

    gdepthfirstsearch = GDepthFirstSearch(initial_state, objective_state, objective.location)
    gdfs_res = gdepthfirstsearch.solve()


    sep="-------------"
    print(sep)
    print("Results:")
    print(sep)
    print("Tree Depth First Search")
    if tdfs_result is not None:
        print_path(tdfs_result)
    else:
        print("No result for Tree depth first search. (Searching in a circle)")
    print("Tree Breadth First Search")
    print_path(tbfs_result)


    print(sep)
    print("Graph breadth first search")
    print_path(gbfs_res)
    print("Graph depth first search")
    print_path(gdfs_res)


if __name__ == "__main__":
    main()
