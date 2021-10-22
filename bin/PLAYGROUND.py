import ray
from search import graph_astar_solve, graph_uniform_cost_solve
from states import generate_init_state, generate_target_state


def massive_astar():
    init_state = generate_init_state(
        automatic_action_module=True, size=(40, 40), blocked_cell_count=30
    )

    target_state = generate_target_state(init_state)

    results = ray.get(graph_astar_solve.remote(init_state, target_state))

    print(results)

def massive_ucs():
    init_state = generate_init_state(
        automatic_action_module=True, size=(40,40), blocked_cell_count=30
    )

    target_state = generate_target_state(init_state)

    results = ray.get(graph_uniform_cost_solve.remote(init_state, target_state))
    print(results)


def main():
    ray.init()
    massive_astar()
    massive_ucs()


if __name__ == "__main__":
    main()
