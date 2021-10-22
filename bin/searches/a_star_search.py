import os
from copy import copy
from time import time

import psutil
import ray
from funcs import (
    calculate_cost,
    is_goal,
    is_in_closed_set,
    manhattan_distance,
    uniform_sort,
)
from states import get_children_states


@ray.remote
def tree_astar_solve(initial_state, target_state):
    """Use A* to search for target state"""
    prio_queue = []
    prio_queue.append((0, initial_state))

    start_time = time()
    i = 0
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while prio_queue.__sizeof__() != 0:
        i += 1
        _, current_state = prio_queue.pop(0)

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Tree A* solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )
            return [current_state, elapsed, i, cost, end_mem]

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
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while prio_queue.__sizeof__() != 0:
        i += 1
        _, current_state = prio_queue.pop(0)
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )

        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Graph A* solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )

            return [current_state, elapsed, i, cost, end_mem]

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
