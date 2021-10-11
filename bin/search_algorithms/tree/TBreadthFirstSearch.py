import queue

from search_algorithms.Node import Node
from search_algorithms.Search import Search


class TBreadthFirstSearch(Search):
    def solve(self):
        while not self.queue.empty():
            n = self.queue.get()
            print(n.robot_location)
            if self.is_goal(n):
                return n
            for node in n.children_nodes():
                self.queue.put(node)
        return None

