import queue

from search_algorithms.Node import Node
from search_algorithms.Search import Search


class GBreadthFirstSearch(Search):
    def solve(self):
        self.queue = queue.Queue()
        self.queue.put(Node(self.init_state))
        closed_set = []

        while not self.queue.empty():
            n = self.queue.get()
            if n not in closed_set:
                closed_set.append(n)
                print(n.robot_location)
                if self.is_goal(n):
                    return n
                for node in n.children_nodes():
                    self.queue.put(node)
        return None
