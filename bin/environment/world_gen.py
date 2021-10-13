import numpy as np


def generate_init_state():
    graph = np.random.randint(low=0, high=20, size=(10,10))

    x_robot, y_robot, x_target, y_target = np.random.randint(low=0, high=10, size=4)

    graph[x_robot, y_robot] = -1 #robot location represented as -1
    graph[x_target, y_target] = -2 #objective location represented as -2

    return {
        "graph":graph,
        "robot_init_location":[x_robot, y_robot],
        "objective_location":[x_target, y_target]
    }


x = generate_init_state()

print(x)
