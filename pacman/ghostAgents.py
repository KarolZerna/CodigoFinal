# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getOriginalLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scared_flee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scared_flee = prob_scared_flee

    def getDistribution( self, state ):
        # Read variables from state
        ghost_state = state.getGhostState( self.index )
        legal_actions = state.getOriginalLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        is_scared = ghost_state.scaredTimer > 0

        speed = 1
        if is_scared: speed = 0.5

        action_vectors = [Actions.directionToVector( a, speed ) for a in legal_actions]
        new_positions = [( pos[0]+a[0], pos[1]+a[1] ) for a in action_vectors]
        pacman_position = state.getPacmanPosition()

        # Select best actions given the state
        distances_to_pacman = [manhattanDistance( pos, pacman_position ) for pos in new_positions]
        if is_scared:
            best_score = max( distances_to_pacman )
            best_prob = self.prob_scared_flee
        else:
            best_score = min( distances_to_pacman )
            best_prob = self.prob_attack
        best_actions = [action for action, distance in zip( legal_actions, distances_to_pacman ) if distance == best_score]

        # Construct distribution
        dist = util.Counter()
        for a in best_actions: dist[a] = best_prob / len(best_actions)
        for a in legal_actions: dist[a] += ( 1-best_prob ) / len(legal_actions)
        dist.normalize()
        return dist

class KeyboardTrainingGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scared_flee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scared_flee = prob_scared_flee

    def getDistribution( self, state ):
        # Read variables from state
        ghost_state = state.getGhostState( self.index )
        legal_actions = state.getOriginalLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        is_scared = ghost_state.scaredTimer > 0

        speed = 1
        if is_scared: speed = 0.5

        action_vectors = [Actions.directionToVector( a, speed ) for a in legal_actions]
        new_positions = [( pos[0]+a[0], pos[1]+a[1] ) for a in action_vectors]
        pacman_position = state.getPacmanPosition()

        # Select best actions given the state
        distances_to_pacman = [manhattanDistance( pos, pacman_position ) for pos in new_positions]
        if is_scared:
            best_score = max( distances_to_pacman )
            best_prob = self.prob_scared_flee
        else:
            best_score = min( distances_to_pacman )
            best_prob = self.prob_attack
        best_actions = [action for action, distance in zip( legal_actions, distances_to_pacman ) if distance == best_score]

        # Construct distribution
        dist = util.Counter()
        for a in best_actions: dist[a] = best_prob / len(best_actions)
        for a in legal_actions: dist[a] += ( 1-best_prob ) / len(legal_actions)
        dist.normalize()
        return dist

class KeyboardGhost( GhostAgent ):
        """
        A ghost controlled by the keyboard.
        """
        WEST_KEY  = ''
        EAST_KEY  = ''
        NORTH_KEY = ''
        SOUTH_KEY = ''
        STOP_KEY = ''

        def __init__( self, index = 0 ):            
            self.index = index
            self.keys = []

            # Binding of keys
            # Up to 4 players
            if self.index == 1:
                self.NORTH_KEY = 'Up'
                self.WEST_KEY  = 'Left'
                self.SOUTH_KEY = 'Down'
                self.EAST_KEY  = 'Right'
                self.STOP_KEY = 'Space'

            if self.index == 2:
                self.NORTH_KEY = 'w'
                self.WEST_KEY  = 'a'
                self.SOUTH_KEY = 's'
                self.EAST_KEY  = 'd'
                self.STOP_KEY = 'q'

            if self.index == 3:
                self.NORTH_KEY = 't'
                self.WEST_KEY  = 'f'
                self.SOUTH_KEY = 'g'
                self.EAST_KEY  = 'h'
                self.STOP_KEY = 'r'

            if self.index == 4:
                self.NORTH_KEY = 'i'
                self.WEST_KEY  = 'j'
                self.SOUTH_KEY = 'k'
                self.EAST_KEY  = 'l'
                self.STOP_KEY = 'u'

            self.init()

        def init( self ):
            self.lastMove = Directions.STOP

        def getAction( self, state):
            from graphicsUtils import keys_waiting
            from graphicsUtils import keys_pressed
            from string import lower

            keys = keys_pressed()
            if keys != []:
                self.keys = map((lambda s: lower(s) if len(s) == 1 else s), keys)

            legal = state.getLegalActions(self.index)
            move = self.getMove(legal)

            if move == Directions.STOP and self.lastMove in legal:
                # Try to move in the same direction as before
                move = self.lastMove
            self.lastMove = move
            return move

        def getMove(self, legal):
            move = Directions.STOP
            if   (self.WEST_KEY in self.keys) and Directions.WEST in legal:  move = Directions.WEST
            if   (self.EAST_KEY in self.keys) and Directions.EAST in legal: move = Directions.EAST
            if   (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
            if   (self.SOUTH_KEY in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
            return move
