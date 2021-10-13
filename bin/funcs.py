from copy import deepcopy

import numpy as np


def is_goal(current_state, target_state):
    robot_curr_location = current_state["robot_location"]
    robot_target_location = target_state["robot_location"]

    if (
        robot_curr_location[0] == robot_target_location[0]
        and robot_curr_location[1] == robot_target_location[1]
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
