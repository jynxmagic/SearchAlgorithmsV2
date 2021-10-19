from copy import copy, deepcopy

import numpy as np


def generate_init_state():
    """graph = np.random.randint(low=1, high=10, size=(9, 9))

    x_robot, y_robot, x_target, y_target = np.random.randint(low=0, high=8, size=4)

    immoveable_cells = np.random.randint(
        low=0, high=9, size=(10, 2)
    )  # 10 immoveable cells

    for cell in immoveable_cells:
        graph[cell[0], cell[1]] = -3  # -3 represents immoveable cell
    graph[x_robot, y_robot] = -1  # robot location represented as -1
    graph[x_target, y_target] = -2  # objective location represented as -2

    return {
        "graph": graph,
        "encoded_state": [x_robot, y_robot, x_target, y_target],
        "path": [[x_robot.copy(), y_robot.copy()]],
    } INITIALLY WAS RANDOM, CHANGED FOR REPRODUCABLILITY"""

    weighted_graph = [
        [9, 1, 8, 6, 8, 9, -3, 7, 2],
        [1, 7, 2, 6, 7, 4, 8, 7, 8],
        [5, 8, -1, 1, 4, 1, 1, 6, 2],
        [-3, -3, -3, -3, 9, 1, 5, 3, 2],
        [9, 3, 7, 1, 1, 1, 1, 1, 4],
        [1, 1, 1, 1, 4, 5, 2, 3, 7],
        [8, -2, 2, 4, 6, 6, 3, 5, -3],
        [7, 5, 7, 7, 1, 5, 2, 4, 4],
        [6, 6, 7, -3, -3, 3, 9, 6, 1],
    ]

    np_weighted_graph = np.array(weighted_graph, dtype=int)

    x_robot, y_robot, x_target, y_target = np.array([2, 2, 6, 1], dtype=int)

    return {
        "graph": np_weighted_graph,
        "encoded_state": [x_robot, y_robot, x_target, y_target],
        "path": [[copy(x_robot), copy(y_robot)]],
    }


def generate_target_state(initial_state):
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
    states = []

    robot_original_location = [state["encoded_state"][0], state["encoded_state"][1]]

    for i in range(4):
        new_state = deepcopy(state)

        x, y = robot_original_location.copy()

        # movement model: N, E, S, W
        if i == 0:
            y -= 1
        elif i == 1:
            x += 1
        elif i == 2:
            y += 1
        elif i == 3:
            x -= 1

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
