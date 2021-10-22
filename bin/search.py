import ray

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

# remote defines the function as being multithreaded.
# each search is multithreaded so that all can run simultaneously
# with ray.


def start_search_threads(initial_state, target_state):
    """Start all threads to search for target state

    Args:
        initial_state ([dict]): Starting state of the problem
        target_state ([dict]): Finished state of the problem

    Returns:
        dict: solved problems
    """
    tbfs_ref = tree_breadth_first_solve.remote(initial_state, target_state)
    tdfs_ref = tree_depth_first_solve.remote(initial_state, target_state)
    gbfs_ref = graph_breadth_first_solve.remote(initial_state, target_state)
    gdfs_ref = graph_depth_first_solve.remote(initial_state, target_state)
    tucs_ref = tree_uniform_cost_solve.remote(initial_state, target_state)
    gucs_ref = graph_uniform_cost_solve.remote(initial_state, target_state)
    tastar_ref = tree_astar_solve.remote(initial_state, target_state)
    gastar_ref = graph_astar_solve.remote(initial_state, target_state)

    # ray.get forces main thread to stop until results.
    # all child threads are still running simultaenously though
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














