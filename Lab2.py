import bisect, sys
import numpy as np
from math import radians, cos, sin, asin, sqrt

from SearchProblem import *
from SearchAnimator import *


INFINITY = 1.0e400
CUTOFF = "CUTOFF"


## ############################ #
## Uninformed Search Algorithms #
## ############################ #

def graph_search(problem, callback):
    """Search through the successors of a problem to find a goal.
    The argument fringe is some kind of empty container.
    If two paths reach a state, only use the best one. [Fig. 3.5]"""
    Node.nodecount = 0
    closed = {}
    fringe = []
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            callback(problem.graph, node, fringe, closed, True)
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))
            callback(problem.graph, node, fringe, closed, False)
    return None


def breadth_first_graph_search(problem, callback):
    """Search the shallowest nodes in the search tree first. [p 77]"""
    Node.nodecount = 0
    closed = {}
    fringe = FIFOQueue()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            callback(problem.graph, node, fringe, closed, True)
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))
            callback(problem.graph, node, fringe, closed, False)
    return None


def depth_first_graph_search(problem, callback):
    """Search the deepest nodes in the search tree first. [p 78]"""
    Node.nodecount = 0
    closed = {}
    fringe = Stack()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            callback(problem.graph, node, fringe, closed, True)
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))
            callback(problem.graph, node, fringe, closed, False)
    return None


def depth_limited_search(problem, limit, callback):
    """Depth-first search with a depth limit. [p 81]"""
    closed = {}
    fringe = Stack()
    fringe.append(Node(problem.initial))
    result = None
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            callback(problem.graph, node, fringe, closed, True)
            return node
        if node.depth > limit:
            result = CUTOFF
            callback(problem.graph, node, fringe, closed, False)
        elif node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))
            callback(problem.graph, node, fringe, closed, False)
    return result


def iterative_deepening_search(problem, callback):
    """Iterative deepening using depth limited search [p 81]"""
    Node.nodecount = 0
    depth = 0
    while True:
        result = depth_limited_search(problem, depth, callback)
        if result != CUTOFF:
            return result
        depth += 1


## ###################################### #
## Informed (Heuristic) Search Algorithms #
## ###################################### #

def best_first_graph_search(problem, f, callback):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search."""
    ### YOU IMPLEMENT THIS ###


def greedy_best_first_graph_search(problem, callback):
    """Best-first graph search with f(n)=h(n). [p 85]"""
    ### YOU IMPLEMENT THIS ###


def astar_search(problem, callback, h=None):
    """Best-first graph search with f(n) = g(n)+h(n). [p 85]"""
    ### YOU IMPLEMENT THIS ###


## Main loop
if __name__ == "__main__":
    algs = {
            "GS": graph_search,
            "BFS": breadth_first_graph_search,
            "DFS": depth_first_graph_search,
            "IDS": iterative_deepening_search,
            "greedy": greedy_best_first_graph_search,
            "A*": astar_search}
    animate = SearchAnimator(algs)
    animate.run()
