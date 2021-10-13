from queue import LifoQueue, PriorityQueue, Queue

import ray
from ray import remote

from funcs import is_goal, is_in_closed_set, uniform_sort
from states import get_children_states

# remote defines the function as being multithreaded.
# each search is multithreaded so that all can run simultaneously
# with ray.


def start_search_threads(initial_state, target_state):
    tbfs_ref = tree_breadth_first_solve.remote(initial_state, target_state)
    tdfs_ref = tree_depth_first_solve.remote(initial_state, target_state)
    gbfs_ref = graph_breadth_first_solve.remote(initial_state, target_state)
    gdfs_ref = graph_depth_first_solve.remote(initial_state, target_state)
    tucs_ref = tree_uniform_cost_solve.remote(initial_state, target_state)
    gucs_ref = graph_uniform_cost_solve.remote(initial_state, target_state)

    # ray.get forces main thread to stop until results.
    # all child threads are still running simultaenously though
    return {
        "tbfs": ray.get(tbfs_ref),
        "tdfs": ray.get(tdfs_ref),
        "gbfs": ray.get(gbfs_ref),
        "gdfs": ray.get(gdfs_ref),
        "tucs": ray.get(tucs_ref),
        "gucs": ray.get(gucs_ref),
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


@remote
def tree_uniform_cost_solve(initial_state, target_state):

    # uniform cost will go round on a cheap circle in a TREE only - limit implemented.

    # manual priority queue rather than queue.PriorityQueue()
    # due to NumPy and Python priority
    # queue not working togther.
    # see: https://stackoverflow.com/questions/42236820/adding-numpy-array-to-a-heap-queue

    prio_queue = []
    prio_queue.append((0, initial_state))

    i = 0
    while not prio_queue.__sizeof__() == 0:
        i += 1
        prio, current_state = prio_queue.pop(0)
        if is_goal(current_state, target_state) or i == 100:
            return current_state

        for child_state in get_children_states(current_state, initial_state):
            uniform_cost = (
                prio  # total path cost to current location
                + initial_state["graph"][  # action cost
                    child_state["robot_location"][0], child_state["robot_location"][1]
                ]
            )
            prio_queue.append(
                (uniform_cost, child_state)
            )  # prio is lowest uniform cost
            prio_queue = uniform_sort(prio_queue)


@remote
def graph_uniform_cost_solve(initial_state, target_state):
    prio_queue = []
    prio_queue.append((0, initial_state))

    closed_set = []

    while not prio_queue.__sizeof__ == 0:
        prio, current_state = prio_queue.pop(0)
        closed_set.append(current_state["robot_location"])

        if is_goal(current_state, target_state):
            return current_state

        for child_state in get_children_states(current_state, initial_state):

            if not is_in_closed_set(child_state["robot_location"], closed_set):
                uniform_cost = (
                    prio  # total path cost to current location
                    + initial_state["graph"][  # action cost
                        child_state["robot_location"][0],
                        child_state["robot_location"][1],
                    ]
                )
                prio_queue.append((uniform_cost, child_state))
                prio_queue = uniform_sort(prio_queue)
