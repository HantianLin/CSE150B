from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if(len(self.children) == 0):
            return True
        else:
            return False

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        if depth == 0:
            return

        parent = self.simulator.current_state() #sets the parent state
        #import pdb; pdb.set_trace()
        if node.player_type == MAX_PLAYER:
            for direction in range(4):
                self.simulator.set_state(parent[0], parent[1]) #resets it back to the parent state
                if self.simulator.move(direction): #only adds as a child if it is a valid move
                    new_node = Node(copy.deepcopy(self.simulator.current_state()), CHANCE_PLAYER)
                    node.children.append((direction, new_node))
                    self.build_tree(new_node, depth - 1)
        else: #CHANCE_PLAYER
            tiles = self.simulator.get_open_tiles()
            for tile in tiles:
                self.simulator.set_state(parent[0], parent[1]) #resets it back to the parent state
                self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                new_node = Node(copy.deepcopy(self.simulator.current_state()), MAX_PLAYER)
                node.children.append((None, new_node))
                self.build_tree(new_node, depth - 1)
        return


    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        if node is None:
            node = self.root
        if node.is_terminal():
            return (None, node.state[1])
        
        #import pdb; pdb.set_trace()
        if node.player_type == MAX_PLAYER:
            best_direction, best_score = None, float('-inf')
            for child in node.children:
                _, child_score = self.expectimax(child[1])
                if child_score > best_score:
                    best_score = child_score
                    best_direction = child[0]
            return (best_direction, best_score)
        else: # CHANCE_PLAYER
            total_score = 0
            for child in node.children:
                _, child_score = self.expectimax(child[1])
                total_score += child_score
            return (None, total_score / len(node.children))

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax2(self.root)
        return direction
