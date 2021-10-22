import os
from copy import copy
from time import time

import psutil
import ray
from funcs import calculate_cost, is_goal, is_in_closed_set, uniform_sort
from states import get_children_states


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
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while prio_queue.__sizeof__() != 0:
        i += 1
        prio, current_state = prio_queue.pop(0)
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Tree ucs solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )
            return [current_state, elapsed, i, cost, end_mem]

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
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while prio_queue.__sizeof__() != 0:
        i += 1
        prio, current_state = prio_queue.pop(0)
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Graph ucs solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )
            return [current_state, elapsed, i, cost, end_mem]

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
