from copy import deepcopy
from time import time

import matplotlib.pyplot as plt
import networkx as nx
import ray

from draw import draw_route, draw_state
from results import generate_graphs
from search import start_search_threads
from states import generate_init_state, generate_target_state

print("Starting Ray.. (takes a couple of seconds.)")
ray.init()


def main():
    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)
    draw_state(initial_state)

    print("starting threads...")
    start_time = time()
    results = start_search_threads(initial_state, target_state)
    print("finished all threads in {}".format(time() - start_time))

    draw_route(results["tbfs"][0], color="yellow", title="Tree Breadth First Search")
    draw_route(results["gbfs"][0], color="yellow", title="Graph Breadth First Search")
    draw_route(results["tdfs"][0], color="green", title="Tree Depth First Search")
    draw_route(results["gdfs"][0], color="green", title="Graph Depth First Search")
    draw_route(results["tucs"][0], color="purple", title="Tree Uniform Cost Search")
    draw_route(results["gucs"][0], color="purple", title="Graph Uniform Cost Search")
    draw_route(results["tastar"][0], color="orange", title="Tree A* Search")
    draw_route(results["gastar"][0], color="orange", title="Graph A* Search")

    generate_graphs(results)


if __name__ == "__main__":
    main()
