from copy import deepcopy

import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state.copy()
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        idx = np.where(state == 2)
        self.robot_location = idx
        if parent:
            self.depth = parent.depth + 1

    def children_states(self):
        states = []
        location = self.robot_location
        for i in range(4):
            # movements : 0=N,1=E,2=S,3=W
            tile = self.get_tile_of_action(i)
            if tile is not None:
                new_state = self.create_new_state(self, location, tile.location)
                states.append(new_state)
        return states

    def children_nodes(self):
        nodes = []
        for i in range(4):
            tile = self.get_tile_of_action(i)
            if tile is not None:
                new_node = self.child_node(i)
                nodes.append(new_node)
        return nodes

    def create_new_state(self, old_location, new_location):
        new_state = self.state.copy()

        try:
            new_state[old_location[0], old_location[1]] = 1
            new_state[new_location[0], new_location[1]] = 2
        except IndexError:
            return new_state
        return new_state

    def get_tile_of_action(self, action):
        location = self.robot_location
        x, y = deepcopy(location)
        if action == 0:
            y -= 1
        elif action == 1:
            x += 1
        elif action == 2:
            y += 1
        elif action == 3:
            x -= 1

        try:
            return (x, y)
        except IndexError:
            return None

    def child_node(self, action):
        original_location = deepcopy(self.robot_location)
        action_result_location = self.get_tile_of_action(action)
        next_state = self.create_new_state(original_location, action_result_location)
        next_node = Node(next_state, self, action, self.path_cost + 1)
        return next_node

    def path(self):
        node = self
        path = []
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))
