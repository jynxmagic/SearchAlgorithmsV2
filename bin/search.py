from queue import LifoQueue, Queue
from time import time

import ray
from funcs import is_goal, is_in_closed_set, manhattan_distance, uniform_sort
from states import get_children_states

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


@ray.remote
def tree_breadth_first_solve(initial_state, target_state):
    """Use BFS to search for target state"""
    fifo_queue = Queue()
    fifo_queue.put(initial_state)

    start_time = time()
    i = 0

    fifo_queue.__sizeof__
    while not fifo_queue.empty():
        i += 1
        current_state = fifo_queue.get()
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Tree bfs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_states in get_children_states(current_state, initial_state):
            fifo_queue.put(child_states)


@ray.remote
def tree_depth_first_solve(initial_state, target_state):
    """Use DFS to search for target state"""
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    start_time = time()
    i = 0
    while not lifo_queue.empty():
        i += 1
        current_state = lifo_queue.get()
        if is_goal(current_state, target_state) or i == 100:
            elapsed = time() - start_time
            print(
                "Tree dfs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_states in get_children_states(current_state, initial_state):
            lifo_queue.put(child_states)


@ray.remote
def graph_breadth_first_solve(initial_state, target_state):
    """Use BFS to search for target state"""
    fifo_queue = Queue()
    fifo_queue.put(initial_state)

    closed_set = []

    start_time = time()
    i = 0
    while not fifo_queue.empty():
        i += 1
        current_state = fifo_queue.get()
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Graph bfs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                closed_set,
            ):
                fifo_queue.put(child_state)


@ray.remote
def graph_depth_first_solve(initial_state, target_state):
    """Use DFS to search for target state"""
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    closed_set = []

    start_time = time()
    i = 0
    while not lifo_queue.empty():
        i += 1
        current_state = lifo_queue.get()
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Graph dfs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                closed_set,
            ):
                lifo_queue.put(child_state)


@ray.remote
def tree_uniform_cost_solve(initial_state, target_state):
    """Use ucs to search for target state."""
    # 1. uniform cost will go round on a cheap circle... repetetively... (until cost of going closer to objective is less than
    # cost of running in a circle) in a TREE only. While not limited, this can still cause issues.

    # 2. manual priority queue rather than queue.PriorityQueue()
    # due to NumPy and Python priority
    # queue not working togther.
    # see: https://stackoverflow.com/questions/42236820/adding-numpy-array-to-a-heap-queue

    prio_queue = []
    prio_queue.append((0, initial_state))

    start_time = time()
    i = 0
    while prio_queue.__sizeof__() != 0:
        i += 1
        prio, current_state = prio_queue.pop(0)
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Tree ucs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):
            uniform_cost = (
                prio  # total path cost to current location
                + initial_state["graph"][  # action cost
                    child_state["encoded_state"][0], child_state["encoded_state"][1]
                ]
            )
            prio_queue.append(
                (uniform_cost, child_state)
            )  # prio is lowest uniform cost
            prio_queue = uniform_sort(prio_queue)


@ray.remote
def graph_uniform_cost_solve(initial_state, target_state):
    """Use UCS to search for target state"""
    prio_queue = []
    prio_queue.append((0, initial_state))

    closed_set = []

    start_time = time()
    i = 0
    while prio_queue.__sizeof__() != 0:
        i += 1
        prio, current_state = prio_queue.pop(0)
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Graph ucs solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):

            if not is_in_closed_set(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                closed_set,
            ):
                uniform_cost = (
                    prio  # total path cost to current location
                    + initial_state["graph"][  # action cost
                        child_state["encoded_state"][0],
                        child_state["encoded_state"][1],
                    ]
                )
                prio_queue.append((uniform_cost, child_state))
                prio_queue = uniform_sort(prio_queue)


@ray.remote
def tree_astar_solve(initial_state, target_state):
    """Use A* to search for target state"""
    prio_queue = []
    prio_queue.append((0, initial_state))

    start_time = time()
    i = 0
    while prio_queue.__sizeof__() != 0:
        i += 1
        prio, current_state = prio_queue.pop(0)

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Tree A* solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )
            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):
            movement_cost = initial_state["graph"][
                child_state["encoded_state"][0], child_state["encoded_state"][1]
            ]

            heuristic_cost = manhattan_distance(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                [initial_state["encoded_state"][2], initial_state["encoded_state"][3]],
            )

            astar_cost = movement_cost + heuristic_cost  # g+h

            prio_queue.append((astar_cost, child_state))
            prio_queue = uniform_sort(prio_queue)


@ray.remote
def graph_astar_solve(initial_state, target_state):
    """Use A* to search for target state."""
    prio_queue = []
    prio_queue.append((0, initial_state))

    closed_set = []

    start_time = time()
    i = 0
    while prio_queue.__sizeof__() != 0:
        i += 1
        _, current_state = prio_queue.pop(0)
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            print(
                "Graph A* solved in {}ms, {} iterations".format(int(elapsed * 1000), i)
            )

            return [current_state, elapsed, i]

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                closed_set,
            ):
                movement_cost = initial_state["graph"][
                    child_state["encoded_state"][0], child_state["encoded_state"][1]
                ]

                heuristic_cost = manhattan_distance(
                    [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                    [
                        initial_state["encoded_state"][2],
                        initial_state["encoded_state"][3],
                    ],
                )

                astar_cost = movement_cost + heuristic_cost  # g+h
                prio_queue.append((astar_cost, child_state))
                prio_queue = uniform_sort(prio_queue)
