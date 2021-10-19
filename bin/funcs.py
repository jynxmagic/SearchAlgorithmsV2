from copy import deepcopy

import numpy as np


def is_goal(current_state, target_state):
    if (
        current_state["encoded_state"][0] == target_state["encoded_state"][2]
        and current_state["encoded_state"][1] == target_state["encoded_state"][3]
    ):
        return True
    return False


def is_in_closed_set(location, closed_set):
    x, y = location
    for to_test in closed_set:
        if to_test[0] == x and to_test[1] == y:
            return True
    return False


def uniform_sort(arr):
    return sorted(arr, key=lambda x: x[0])


def manhattan_distance(l0, l1):
    diff_x = abs(l0[0] - l1[0])
    diff_y = abs(l0[1] - l1[1])
    return diff_x + diff_y
