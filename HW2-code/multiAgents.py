

# --------------
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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor)
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ###food score##########
        if successorGameState.isWin():
            return float("inf")

        newFood=newFood.asList()
        cloestFood=100000
        for food in newFood:
            dist=util.manhattanDistance(newPos, food)
            if dist< cloestFood:
                cloestFood = dist
        foodsocre=cloestFood
        ######ghostscore#######
        ghostscore=0
        for i in newGhostStates:
            ghostpos=i.getPosition()
            ghostscore+=util.manhattanDistance(ghostpos, newPos)
            if util.manhattanDistance(ghostpos, newPos)==1:
                ghostscore+=-float("inf")
        #######capsulescore#########
        capscore = 1
        if newPos in currentCapsules:
            capscore-= 100

        score=successorGameState.getScore()-foodsocre+ghostscore-capscore+sum(newScaredTimes)
        if action == Directions.STOP:
            score -= 10
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, state):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def maxaction(state,depth):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state),'no move'

            action=state.getLegalActions()
            score=[]
            for i in action:
                nextstate=state.generateSuccessor(self.index, i)
                v=minaction(nextstate,depth,1)
                score.append(v)
            bestscore=max(score)
            bestIndex=0
            for i in range(len(score)):
                if score[i]==bestscore:
                    bestIndex=i
            return bestscore,action[bestIndex]

        def minaction(state,depth,agentIndex):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            score=[]
            bestaction=Directions.STOP
            ghostNum=state.getNumAgents()-1
            action=state.getLegalActions(agentIndex)
            if agentIndex==ghostNum:
                for i in action:
                    nextstate=state.generateSuccessor(agentIndex,i)
                    v=maxaction(nextstate,depth-1)
                    score.append(v)
            else:
                for i in action:
                    nextstate=state.generateSuccessor(agentIndex, i)
                    v=minaction(nextstate,depth,agentIndex+1)
                    score.append(v)
            bestscore=min(score)
            for i in range(len(score)):
                if score[i]==bestscore:
                    bestIndex=i
            return bestscore,action[bestIndex]

        bestscore, bestaction=maxaction(state,self.depth)
        return bestaction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxvalue(gameState, a, b,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -float('inf')
            action=gameState.getLegalActions(0)
            for i in action:
                v = max(v,minvalue(gameState.generateSuccessor(0,i), a, b,1,depth))
                if v > b :
                    return v
                a = max(a, v)
            return v

        def minvalue(gameState,a,b,agentIndex,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = float('inf')
            ghostNum=gameState.getNumAgents()-1

            action=gameState.getLegalActions(agentIndex)
            for i in action:
                nextstate=gameState.generateSuccessor(agentIndex, i)
                if agentIndex==ghostNum:
                    v=min(v,maxvalue(gameState.generateSuccessor(agentIndex,i), a, b,depth-1))
                    if v<a:
                        return v
                    b=min(b,v)
                else:
                    v=min(v,minvalue(gameState.generateSuccessor(agentIndex,i), a, b,agentIndex+1,depth))
                    if v<a:
                        return v
                    b=min(b,v)
            return v

        bestaction=Directions.STOP
        ghostNum=gameState.getNumAgents()-1
        action=gameState.getLegalActions(0)
        score=-float('inf')
        a=-float('inf')
        b=float('inf')

        for i in action:
            nextstate=gameState.generateSuccessor(0,i)
            prescore=score
            score=max(score, minvalue(nextstate, a,b,1,self.depth))
            if score>prescore:
                bestaction=i
            if score>=b:
                return bestaction
            a=max(a,score)
        return bestaction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectedvalue(gameState,agentIndex,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            ghostNum=gameState.getNumAgents()-1
            action=gameState.getLegalActions(agentIndex)
            value=0
            for i in action:
                if agentIndex==ghostNum:
                    value += maxvalue(gameState.generateSuccessor(agentIndex,i),depth-1)
                else:
                    value += expectedvalue(gameState.generateSuccessor(agentIndex,i),agentIndex+1,depth)
            #print value / len(action)
            return value / len(action)


        def maxvalue(gameState,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            action=gameState.getLegalActions(0)
            bestaction = Directions.STOP
            v=-(float("inf"))
            for i in action:
                prescore=v
                v=max(v,expectedvalue(gameState.generateSuccessor(0,i),1,depth))
            return v

        if gameState.isWin() or gameState.isLose() or self.depth == 0:
            return self.evaluationFunction(gameState)
        score = -(float("inf"))
        action=gameState.getLegalActions(0)
        bestaction = Directions.STOP
        for i in action:
            prescore=score
            score = max(score, expectedvalue(gameState.generateSuccessor(0,i),1,self.depth))
            if score>prescore:
                bestaction=i
        return bestaction





        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      In the begin, is the current sate is win we return Inf, if the current state is lose, we return -Inf.

      Then we will calculate the score.
      First, we calculate the food score. We find out the closest food on the current position and assign it to foodscore.
      Secondly, we calculate the ghost score, which is the closest ghost gistance based on manhattan Distance.
      if the distance between current position and ghost is smaller than 2, we consider it to be extremely dangerous,
      and we will plus -Inf to the ghostscore.
      Thirdly, we calculate the capsule score, which is the closest distance between capsule and current distance.

      Our final score to the current position is the scoreEvaluationFunction(currentGameState) plus the max of
      ghost score and 2, which means if the position to the ghost is less than 2, it is dangerous.
      We plus this value because the higher the ghost score the safer capman will be.
      Then we will subtract the square of food score and capsule, because if capman is more close to food or capsule,
      the score of the current position should be higher.
      After that , we will also subtract the number of food remains and the number of capsules remains.

      The final score is the score we assign to the current position.
    """
    "*** YOUR CODE HERE ***"

    Pos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood() #food available from current state
    currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
    GhostStates = currentGameState.getGhostStates()


    "*** YOUR CODE HERE ***"
    ###food score##########
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    Food=currentFood.asList()
    cloestFood=float("inf")
    for food in Food:
        dist=util.manhattanDistance(Pos, food)
        if dist< cloestFood:
            cloestFood = dist
    foodsocre=cloestFood
    ######ghostscore#######
    ghostscore=0
    for i in GhostStates:
        ghostpos=i.getPosition()
        preghostscore=ghostscore
        ghostscore=min(util.manhattanDistance(ghostpos, Pos),preghostscore)
        #ghostscore=max(ghostscore,2)
        if util.manhattanDistance(ghostpos, Pos)<=2:
            ghostscore+=-float("inf")

    #######capsulescore#########
    capscore = 0
    for i in  currentCapsules:
        #cappos=i.getPosition()
        precapscore=capscore
        capscore=min(util.manhattanDistance(i, Pos),precapscore)

    score=scoreEvaluationFunction(currentGameState)-len(currentCapsules)-foodsocre+max(2,ghostscore)-len(Food)**2-capscore
    #+sum(newScaredTimes)

    return score
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
