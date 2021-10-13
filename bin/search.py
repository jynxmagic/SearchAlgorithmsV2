from queue import Queue

from funcs import is_goal
from states import get_children_states


def tree_breadth_first_solve(initial_state, target_state):
    fifo_queue = Queue()
    fifo_queue.put(initial_state)

    while not fifo_queue.empty():
        current_state = fifo_queue.get()

        print(current_state)

        if is_goal(current_state, target_state):
            return current_state

        for child_states in get_children_states(current_state, initial_state):
            fifo_queue.put(child_states)
