import queue

from search_algorithms.tree.Node import Node


class TDepthFirstSearch:
    def __init__(self, init_state, goal_state, goal_location):
        self.init_state = init_state
        self.goal_state = goal_state
        self.goal_location = goal_location

    def solve(self):
        fifo_queue = queue.Queue()
        fifo_queue.put(Node(self.init_state))
        
        while not fifo_queue.empty():
            n = fifo_queue.get()
            print(n.robot_location)
            if self.is_goal(n):
                return n
            for node in n.children_nodes():
                fifo_queue.put(node)
        return None

    def is_goal(self, to_c):
        robot_curr_location = to_c.robot_location

        if (
            self.goal_location[0] == robot_curr_location[0]
            and self.goal_location[1] == robot_curr_location[1]
        ):
            return True
        return False
