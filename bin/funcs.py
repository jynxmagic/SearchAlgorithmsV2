from copy import deepcopy

import numpy as np


def is_goal(current_state, target_state):
    """Determine if the current_state is the target_state

    Args:
        current_state ([dict]): dict containing values descriptive of current state
        target_state ([dict]): dict containing values descriptive of target state

    Returns:
        [boolean]: True if current_state is target_state
    """
    if (
        current_state["encoded_state"][0] == target_state["encoded_state"][2]
        and current_state["encoded_state"][1] == target_state["encoded_state"][3]
    ):
        return True
    return False


def is_in_closed_set(location, closed_set):
    """Determine if a 1-dimensional array is within a 2-dimensional array.

    Args:
        location ([type]): a 1 dimensional array i.e [x,y]
        closed_set ([type]): a 2 dimensional array i.e [[x1,y1],[x2,y2]...[xn,yn]]

    Returns:
        [boolean]: True if location can be found within closed_set
    """
    x, y = location
    for to_test in closed_set:
        if to_test[0] == x and to_test[1] == y:
            return True
    return False


def uniform_sort(arr):
    """Sort an array based on the first value of a tuple (SORT_BY_SCORE, VALUE)

    Args:
        arr ([tuple]): tuple to sort array by

    Returns:
        arr: sorted array
    """
    return sorted(arr, key=lambda x: x[0])


def manhattan_distance(l0, l1):
    """Calculate the distance between 2 locations on an xy graph.

    Args:
        l0 ([xy array]): location of the robot on a 2d graph as [x,y]
        l1 ([xy array]): location of the target on a 2d graph as [x,y]

    Returns:
        [type]: [description]
    """
    diff_x = abs(l0[0] - l1[0])
    diff_y = abs(l0[1] - l1[1])
    return diff_x + diff_y


def calculate_cost(path, graph):
    """Calculate the cost of a given path on a weighted graph.

    Args:
        path (array): List of xy co-ordinates on the graph, example: [[0,1],[0,2],[...],[9,9]]
        graph (array): Weighted Graph

    Returns:
        integer: cumulative cost of all nodes on a path.
    """
    cost = 0
    for node in path:
        cost += graph[node[0], node[1]]
    return cost
