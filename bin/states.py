from copy import deepcopy

import numpy as np


def generate_init_state():
    graph = np.random.randint(low=0, high=20, size=(9, 9))

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
        "robot_location": [x_robot, y_robot],
        "objective_location": [x_target, y_target],
        "path": [[x_robot.copy(), y_robot.copy()]],
    }


def generate_target_state(initial_state):
    target_state = deepcopy(initial_state)
    target_state["robot_location"] = deepcopy(target_state["objective_location"])
    target_state["graph"][
        initial_state["objective_location"][0], initial_state["objective_location"][1]
    ] = -1

    return target_state


def get_children_states(state, initial_state):
    states = []

    robot_original_location = state["robot_location"]
    old_movement_cost = initial_state["graph"][
        robot_original_location[0], robot_original_location[1]
    ]

    for i in range(4):
        new_state = deepcopy(state)
        try:
            new_state["graph"][
                robot_original_location[0], robot_original_location[1]
            ] = old_movement_cost  # revert old location to orig. value
        except IndexError:
            continue

        x, y = robot_original_location.copy()
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
            v = initial_state["graph"][x, y]
            if v < 0 and v != -2:  # cannot move to special cells
                continue
            new_state["graph"][x, y] = -1
            new_state["robot_location"][0] = x
            new_state["robot_location"][1] = y
            new_state["path"].append(deepcopy(new_state["robot_location"]))
            states.append(new_state)
        except IndexError:
            continue

    return states
