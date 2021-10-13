import queue

from search_algorithms.Node import Node
from search_algorithms.Search import Search


class TDepthFirstSearch(Search):
    def solve(self):
        self.queue = queue.LifoQueue()
        self.queue.put(Node(self.init_state))

        i = 0
        while not self.queue.empty():
            if i > 1000:
                # the tree runs forever in depth first
                print(
                    "Failed to find result with Tree Depth First Search (likely infinite loop)."
                )
                return None
            i += 1
            n = self.queue.get()
            print(n.robot_location)
            if self.is_goal(n):
                return n
            for node in n.children_nodes():
                self.queue.put(node)
        return None
