from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx
import ray

from draw import draw_route, draw_state
from search import start_search_threads
from states import generate_init_state, generate_target_state

print("Starting Ray.. (takes a couple of seconds.)")
ray.init(address="auto")


def main():
    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)
    draw_state(initial_state)

    results = start_search_threads(initial_state, target_state)

    draw_route(results["tbfs"], color="yellow", title="Tree Breadth First Search")
    draw_route(results["gbfs"], color="yellow", title="Graph Breadth First Search")
    draw_route(results["tdfs"], color="green", title="Tree Depth First Search")
    draw_route(results["gdfs"], color="green", title="Graph Depth First Search")
    draw_route(results["tucs"], color="purple", title="Tree Uniform Cost Search")
    draw_route(results["gucs"], color="purple", title="Graph Uniform Cost Search")
    draw_route(results["tastar"], color="orange", title="Tree A* Search")
    draw_route(results["gastar"], color="orange", title="Graph A* Search")

if __name__ == "__main__":
    main()
