from copy import copy, deepcopy

import numpy as np


def generate_init_state(
    automatic_action_module=False, size=(8, 8), blocked_cell_count=10
):
    """Generates an initial state which is a representation of the problem.

    Args:
        automatic_action_module (boolean): whether to randomly generate an environment, or use a fixed one.
    Returns:
        [dict]: representation of the problem
    """

    if automatic_action_module:
        weighted_graph = np.random.randint(low=0, high=9, size=size, dtype=int)
        immoveable_cells = np.random.randint(
            low=0, high=size[1], size=(blocked_cell_count, 2)
        )  # 10 immoveable cells

        for cell in immoveable_cells:
            weighted_graph[cell[0], cell[1]] = -3
        x_robot, y_robot, x_target, y_target = np.random.randint(
            low=0, high=size[0], size=4
        )
        weighted_graph[x_robot, y_robot] = -1
        weighted_graph[x_target, y_target] = -2

    else:
        x_robot, y_robot, x_target, y_target = [2, 2, 6, 1]
        weighted_graph = np.array(
            [
                [9, 1, 8, 6, 8, 9, -3, 7, 2],
                [1, 7, 2, 6, 7, 4, 8, 7, 8],
                [5, 8, -1, 1, 4, 1, 1, 6, 2],
                [-3, -3, -3, -3, 9, 1, 5, 3, 2],
                [9, 3, 7, 1, 1, 1, 1, 1, 4],
                [1, 1, 1, 1, 4, 5, 2, 3, 7],
                [8, -2, 2, 4, 6, 6, 3, 5, -3],
                [7, 5, 7, 7, 1, 5, 2, 4, 4],
                [6, 6, 7, -3, -3, 3, 9, 6, 1],
            ],
            dtype=int,
        )

    return {
        "graph": weighted_graph,
        "encoded_state": np.array([x_robot, y_robot, x_target, y_target], dtype=int),
        "path": [[copy(x_robot), copy(y_robot)]],
    }


def generate_target_state(initial_state):
    """Generates a target state from a given state

    Args:
        initial_state (dict): state

    Returns:
        [dict]: target_state
    """
    target_state = deepcopy(initial_state)
    target_state["encoded_state"] = deepcopy(
        [
            initial_state["encoded_state"][2],
            initial_state["encoded_state"][3],
            initial_state["encoded_state"][2],
            initial_state["encoded_state"][3],
        ]  # encoded state is robotx,roboty,targetx,targety
    )

    return target_state


def get_children_states(state, initial_state):
    """Given a state, return all states which are 1 action away.

    Args:
        state ([dict]): Current state
        initial_state ([dict]): initial state of the problem

    Returns:
        [list]: a list of states which can be reached with a single action.
    """
    states = []

    robot_original_location = [state["encoded_state"][0], state["encoded_state"][1]]

    for i in range(4):
        new_state = deepcopy(state)

        x, y = get_action_model(robot_original_location.copy(), i)

        # bounds
        if x < 0 or y < 0:
            continue
        if x > 9 or y > 9:
            continue
        try:
            cost = initial_state["graph"][x, y]
            if (
                cost < 0 and cost != -2
            ):  # cannot move to special cells, identified by minus scalar
                continue
            new_state["encoded_state"][0] = x
            new_state["encoded_state"][1] = y
            new_state["path"].append(
                deepcopy([new_state["encoded_state"][0], new_state["encoded_state"][1]])
            )
            states.append(new_state)
        except IndexError:
            continue

    return states


def get_action_model(location, action_value):
    """A corrosponding action model on the enviornment.

    Args:
        location (list): x and y location as list
        action_value (list): new x and y location for given action_value

    Returns:
        [type]: [description]
    """
    # movement model: N, E, S, W
    [x, y] = location
    if action_value == 0:
        y -= 1
    elif action_value == 1:
        x += 1
    elif action_value == 2:
        y += 1
    elif action_value == 3:
        x -= 1

    # it's possible to make the robot go north east:
    # elif i == 4
    # x+=1
    # y-=1
    # also south east. etc.

    return [x, y]
