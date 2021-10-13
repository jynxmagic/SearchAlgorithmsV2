from queue import LifoQueue, Queue

import ray
from ray import remote

from funcs import is_goal, is_in_closed_set
from states import get_children_states

# remote defines the function as being multithreaded.
# each search is multithreaded so that all can run simultaneously
# with ray.


def start_search_threads(initial_state, target_state):
    tbfs_ref = tree_breadth_first_solve.remote(initial_state, target_state)
    tdfs_ref = tree_depth_first_solve.remote(initial_state, target_state)
    gbfs_ref = graph_breadth_first_solve.remote(initial_state, target_state)
    gdfs_ref = graph_depth_first_solve.remote(initial_state, target_state)

    # ray.get forces main thread to stop until results
    return {
        "tbfs": ray.get(tbfs_ref),
        "tdfs": ray.get(tdfs_ref),
        "gbfs": ray.get(gbfs_ref),
        "gdfs": ray.get(gdfs_ref),
    }


@remote
def tree_breadth_first_solve(initial_state, target_state):
    fifo_queue = Queue()
    fifo_queue.put(initial_state)

    while not fifo_queue.empty():
        current_state = fifo_queue.get()
        if is_goal(current_state, target_state):
            return current_state

        for child_states in get_children_states(current_state, initial_state):
            fifo_queue.put(child_states)


@remote
def tree_depth_first_solve(initial_state, target_state):
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    i = 0
    while not lifo_queue.empty():
        i += 1
        current_state = lifo_queue.get()
        if is_goal(current_state, target_state) or i == 100:
            return current_state

        for child_states in get_children_states(current_state, initial_state):
            lifo_queue.put(child_states)


@remote
def graph_breadth_first_solve(initial_state, target_state):
    fifo_queue = Queue()
    fifo_queue.put(initial_state)

    closed_set = []
    while not fifo_queue.empty():
        current_state = fifo_queue.get()
        closed_set.append(current_state["robot_location"])
        if is_goal(current_state, target_state):
            return current_state

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(child_state["robot_location"], closed_set):
                fifo_queue.put(child_state)


@remote
def graph_depth_first_solve(initial_state, target_state):
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    closed_set = []
    while not lifo_queue.empty():
        current_state = lifo_queue.get()
        closed_set.append(current_state["robot_location"])
        if is_goal(current_state, target_state):
            return current_state

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(child_state["robot_location"], closed_set):
                lifo_queue.put(child_state)
