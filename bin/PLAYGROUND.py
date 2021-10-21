from time import time

import numpy as np
import ray
from draw import draw_state
from numpy.lib.function_base import copy
from ray.worker import init
from search import graph_astar_solve
from states import generate_target_state


def generate_state(size, blocked_cell_count):
    weighted_graph = np.random.randint(low=0, high=9, size=size, dtype=int)

    x_robot, y_robot, x_target, y_target = np.random.randint(
        low=0, high=size[0], size=4
    )

    immoveable_cells = np.random.randint(
        low=0, high=size[1], size=(blocked_cell_count, 2)
    )  # 10 immoveable cells

    for cell in immoveable_cells:
        weighted_graph[cell[0], cell[1]] = -3

    weighted_graph[x_robot, y_robot] = -1
    weighted_graph[x_target, y_target] = -2

    return {
        "graph": weighted_graph,
        "encoded_state": np.array([x_robot, y_robot, x_target, y_target]),
        "path": [[copy(x_robot), copy(y_robot)]],
    }


def massive_astar():
    init_state = generate_state((40, 40), 30)

    target_state = generate_target_state(init_state)

    draw_state(target_state, with_actions=False)

    results = ray.get(graph_astar_solve.remote(init_state, target_state))

    draw_state(results[0], with_actions=True)


def massive_astar_no_draw():
    init_state = generate_state((1000, 1000), 100)

    target_state = generate_target_state(init_state)

    print("starting large search")
    s_time = time()
    results = ray.get(graph_astar_solve.remote(init_state, target_state))
    f_time = time() - s_time
    print(f_time)
    print(results)


def main():
    ray.init()
    massive_astar_no_draw()


if __name__ == "__main__":
    main()
