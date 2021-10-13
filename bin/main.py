from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx

from draw import draw_state
from search import tree_breadth_first_solve
from states import generate_init_state, generate_target_state


def main():
    initial_state = generate_init_state()
    target_state = generate_target_state(initial_state)

    draw_state(initial_state)

    x = tree_breadth_first_solve(initial_state, target_state)

    print(x)


if __name__ == "__main__":
    main()


