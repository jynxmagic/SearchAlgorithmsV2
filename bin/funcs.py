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
