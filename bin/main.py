from time import time

import ray
from draw import draw_state
from results import generate_graphs
from search import start_search_threads
from states import generate_init_state, generate_target_state

print("Starting Ray.. (takes a couple of seconds.)")
ray.init()


def main():
    """Main Entry point to the program.
    1. Generate Initial state and target state.
    2. Calculate routes from initial state to target state.
    3. Draw routers using tkinter.
    4. Generate graphs displaying results with matplotlib.
    """

    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)
    draw_state(initial_state)

    print("starting threads...")
    start_time = time()
    results = start_search_threads(initial_state, target_state)
    print("finished all threads in {}".format(time() - start_time))

    draw_state(
        results["tbfs"][0],
        color="yellow",
        with_actions=True,
        title="Tree Breadth First Search",
    )
    draw_state(
        results["gbfs"][0],
        color="yellow",
        with_actions=True,
        title="Graph Breadth First Search",
    )
    draw_state(
        results["tdfs"][0],
        color="green",
        with_actions=True,
        title="Tree Depth First Search",
    )
    draw_state(
        results["gdfs"][0],
        color="green",
        with_actions=True,
        title="Graph Depth First Search",
    )
    draw_state(
        results["tucs"][0],
        color="purple",
        with_actions=True,
        title="Tree Uniform Cost Search",
    )
    draw_state(
        results["gucs"][0],
        color="purple",
        with_actions=True,
        title="Graph Uniform Cost Search",
    )
    draw_state(
        results["tastar"][0], color="orange", with_actions=True, title="Tree A* Search"
    )
    draw_state(
        results["gastar"][0], color="orange", with_actions=True, title="Graph A* Search"
    )

    generate_graphs(results)


if __name__ == "__main__":
    main()
