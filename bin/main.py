from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx
import ray

from draw import draw_route, draw_state
from search import start_search_threads
from states import generate_init_state, generate_target_state

print("Starting Ray.. (takes a couple of seconds.)")
ray.init()


def main():
    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)
    draw_state(initial_state)

    results = start_search_threads(initial_state, target_state)

    draw_route(results["tbfs"], color="yellow")
    draw_route(results["tdfs"], color="green")
    draw_route(results["gbfs"], color="yellow")
    draw_route(results["gdfs"], color="green")
    draw_route(results["tucs"], color="purple")
    draw_route(results["gucs"], color="purple")


if __name__ == "__main__":
    main()
