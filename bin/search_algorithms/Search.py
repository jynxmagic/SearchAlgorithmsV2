import queue

from search_algorithms.Node import Node


class Search:    
    def __init__(self, init_state, goal_state, goal_location):
        self.init_state = init_state
        self.goal_state = goal_state
        self.goal_location = goal_location
        self.queue = queue.Queue()
        self.queue.put(Node(self.init_state))

    def is_goal(self, to_c):
        robot_curr_location = to_c.robot_location

        if (
            self.goal_location[0] == robot_curr_location[0]
            and self.goal_location[1] == robot_curr_location[1]
        ):
            return True
        return False
