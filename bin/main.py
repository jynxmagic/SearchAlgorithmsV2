from time import time

import ray
from draw import draw_state
from results import generate_graphs
from searches.a_star_search import graph_astar_solve, tree_astar_solve
from searches.breadth_first_search import (
    graph_breadth_first_solve,
    tree_breadth_first_solve,
)
from searches.depth_first_search import graph_depth_first_solve, tree_depth_first_solve
from searches.uniform_cost_search import (
    graph_uniform_cost_solve,
    tree_uniform_cost_solve,
)
from states import generate_init_state, generate_target_state


def start_search_threads(initial_state, target_state):
    """Start all threads to search for target state

    Args:
        initial_state ([dict]): Starting state of the problem
        target_state ([dict]): Finished state of the problem

    Returns:
        dict: solved problems
    """
    tbfs_ref = tree_breadth_first_solve.remote(
        initial_state, target_state
    )  # remote means multi-threaded
    tdfs_ref = tree_depth_first_solve.remote(initial_state, target_state)
    gbfs_ref = graph_breadth_first_solve.remote(initial_state, target_state)
    gdfs_ref = graph_depth_first_solve.remote(initial_state, target_state)
    tucs_ref = tree_uniform_cost_solve.remote(initial_state, target_state)
    gucs_ref = graph_uniform_cost_solve.remote(initial_state, target_state)
    tastar_ref = tree_astar_solve.remote(initial_state, target_state)
    gastar_ref = graph_astar_solve.remote(initial_state, target_state)

    # ray.get forces main thread to stop until results.
    # all child threads are still running simultaenously though
    # could iterate over an array to start threads.
    print("Waiting for searches to find solutions... (Loading...)")
    return {
        "tbfs": ray.get(tbfs_ref),
        "tdfs": ray.get(tdfs_ref),
        "gbfs": ray.get(gbfs_ref),
        "gdfs": ray.get(gdfs_ref),
        "tucs": ray.get(tucs_ref),
        "gucs": ray.get(gucs_ref),
        "tastar": ray.get(tastar_ref),
        "gastar": ray.get(gastar_ref),
    }


def main():
    """Main Entry point to the program.
    1. Generate Initial state and target state.
    2. Calculate routes from initial state to target state.
    3. Draw routes using tkinter.
    4. Generate graphs displaying results with matplotlib.
    """

    print("Starting Ray.. (takes a couple of seconds.)")
    ray.init()
    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)
    draw_state(initial_state)

    print("starting threads...")
    start_time = time()
    results = start_search_threads(initial_state, target_state)
    print("finished all threads in {}".format(time() - start_time))

    # probably should use iteration here too,
    # though each method call is slightly different
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
