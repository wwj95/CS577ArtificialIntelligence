# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"


    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    state=problem.getStartState()
    node={}
    node["parent"]=None
    node["action"]=None
    node["state"]=state

    visted_list=[]
    s=util.Stack()
    s.push(node)

    while not s.isEmpty():
        node=s.pop()
        visted_list.append(node['state'])
        if problem.isGoalState(node['state']):
            break
        else:
            successor=problem.getSuccessors(node['state'])
            for child in successor:
                if child[0] not in visted_list :
                    child_node={}
                    child_node['parent']=node
                    child_node['action']=child[1]
                    child_node['state']=child[0]
                    s.push(child_node)

    route=[]
    while node["parent"]:
        route.insert(0,node['action'])
        node=node["parent"]

    return route

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    state=problem.getStartState()

    node={}
    node["parent"]=None
    node["action"]=None
    node["state"]=state


    visted_list=[]

    q=util.Queue()
    q.push(node)
    visted_list.append(node['state'])

    while not q.isEmpty():
        node=q.pop()


        if problem.isGoalState(node['state']):
            break
        else:
            successor=problem.getSuccessors(node['state'])
            for child in successor:
                if child[0] not in visted_list:
                    child_node={}
                    child_node['parent']=node
                    child_node['action']=child[1]
                    child_node['state']=child[0]
                    q.push(child_node)
                    visted_list.append(child_node['state'])

    route=[]
    while node["parent"]:
        route.insert(0,node['action'])
        node=node["parent"]

    return route

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    state=problem.getStartState()
    node={}
    node["parent"]=None
    node["action"]=None
    node["state"]=state
    node['cost']=1

    visted_list=[]
    q=util.PriorityQueue()
    q.push(node,node['cost'])


    while not q.isEmpty():
        node=q.pop()
        visted_list.append(node['state'])
        if problem.isGoalState(node['state']):
            break
        else:
            successor=problem.getSuccessors(node['state'])

            for child in successor:
                child_node={}
                child_node['parent']=node
                child_node['action']=child[1]
                child_node['state']=child[0]
                child_node['cost']=node['cost']+child[2]
                if child[0] not in visted_list :
                    q.push(child_node,child_node['cost'])
                    visted_list.append(child_node['state'])
                if problem.isGoalState(child[0]):
                    child_node={}
                    child_node['parent']=node
                    child_node['action']=child[1]
                    child_node['state']=child[0]
                    child_node['cost']=node['cost']+child[2]
                    q.push(child_node,child_node['cost'])
    route=[]
    while node["parent"]:
        route.insert(0,node['action'])
        node=node["parent"]


    return route

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    state=problem.getStartState()
    node={}
    node["parent"]=None
    node["action"]=None
    node['cost']=0

    #print node['state']
    node['h']=heuristic(state,problem)
    state=problem.getStartState()
    node["state"]=state
    #print node['state']
    visted_list=[]
    q=util.PriorityQueue()
    q.push(node,node['cost']+node['h'])
    visted_list.append(node['state'])
    while not q.isEmpty():
        node=q.pop()
        if problem.isGoalState(node['state']):
            break
        else:
            successor=problem.getSuccessors(node['state'])
            for child in successor:
                if child[0] not in visted_list:
                    #print child[0]
                    child_node={}
                    child_node['parent']=node
                    child_node['action']=child[1]
                    child_node['cost']=node['cost']+child[2]
                    child_node['state']=child[0]
                    child_node['h']=heuristic(child_node['state'],problem)
                    child_node['state']=child[0]
                    q.push(child_node,child_node['cost']+child_node['h'])

                    visted_list.append(child_node['state'])
                if problem.isGoalState(child[0]):
                    child_node={}
                    child_node['parent']=node
                    child_node['action']=child[1]
                    child_node['cost']=node['cost']+child[2]
                    child_node['state']=child[0]
                    child_node['h']=heuristic(child_node['state'],problem)
                    child_node['state']=child[0]
                    q.push(child_node,child_node['cost']+child_node['h'])
                #print visted_list

    route=[]
    while node["parent"]:
        route.insert(0,node['action'])
        node=node["parent"]
    #print route
    return route





    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
