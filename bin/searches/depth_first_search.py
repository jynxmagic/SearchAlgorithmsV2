import os
from copy import copy
from queue import LifoQueue
from time import time

import psutil
import ray
from funcs import calculate_cost, is_goal, is_in_closed_set
from states import get_children_states


@ray.remote
def graph_depth_first_solve(initial_state, target_state):
    """Use DFS to search for target state"""
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    closed_set = []

    start_time = time()
    i = 0
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while not lifo_queue.empty():
        i += 1
        current_state = lifo_queue.get()
        closed_set.append(
            [current_state["encoded_state"][0], current_state["encoded_state"][1]]
        )
        if is_goal(current_state, target_state):
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Graph dfs solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )
            return [current_state, elapsed, i, cost, end_mem]

        for child_state in get_children_states(current_state, initial_state):
            if not is_in_closed_set(
                [child_state["encoded_state"][0], child_state["encoded_state"][1]],
                closed_set,
            ):
                lifo_queue.put(child_state)

@ray.remote
def tree_depth_first_solve(initial_state, target_state):
    """Use DFS to search for target state"""
    lifo_queue = LifoQueue()
    lifo_queue.put(initial_state)

    start_time = time()
    i = 0
    process = psutil.Process(os.getpid())
    start_mem = copy(process.memory_info().rss)
    while not lifo_queue.empty():
        i += 1
        current_state = lifo_queue.get()
        if is_goal(current_state, target_state) or i == 100:
            elapsed = time() - start_time
            end_mem = copy(process.memory_info().rss) - start_mem
            cost = calculate_cost(current_state["path"], current_state["graph"])
            print(
                "Tree dfs solved in {}ms, {} iterations, with a cost of {}, using {} bytes of memory".format(
                    int(elapsed * 1000), i, cost, end_mem
                )
            )
            return [current_state, elapsed, i, cost, end_mem]

        for child_states in get_children_states(current_state, initial_state):
            lifo_queue.put(child_states)
