# featureExtractors.py
# --------------------
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


"Feature extractors for Pacman game states"

from game import Directions, Actions
import util
from typing import Union

class FeatureExtractor:
    def get_features(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def get_features(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def get_features(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closest_food(pos, food, ghosts, walls, area_coords=[], pills_coords=[]):
    """
    closest_food -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fbd_coords = []
    for ghost in ghosts:
        fbd_coords.append((int(ghost[0]), int(ghost[1])))
    

    fringe = [(pos[0], pos[1], 0)]
    expanded = set(fbd_coords)    
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        # check if there's a ghost at location too
        if (food[pos_x][pos_y] or (int(pos_x), int(pos_y)) in pills_coords) and (int(pos_x), int(pos_y)) not in area_coords:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

def coord_vect_sub(coord, vect):
    if vect is None:
        return (-1,-1)
    else:
        return (int(coord[0]-vect[0]), int(coord[1]-vect[1]))

def get_closest_intersection(pos, walls, fbd_coords=[]):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set(fbd_coords)
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # check if there's an intersection at this location
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        if len(nbrs) > 3: #left, right, stop || up, down, stop
            return (dist, (int(pos_x), int(pos_y)))
        # otherwise spread out from the location to its neighbours
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))

    # no intersections found
    return None

def distance_to_coord(pos, coord, walls, fbd_coords=[]):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set(fbd_coords)
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find the coord at this location then exit
        if (pos_x, pos_y) == (int(coord[0]), int(coord[1])):
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # coord not found
    return None

def distance_to_coords(pos, coords, walls, fbd_coords=[]):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set(fbd_coords)
    coords = map((lambda coord: (int(coord[0]), int(coord[1]))), coords)
    distances = {}
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find the coord at this location then exit
        if (int(pos_x), int(pos_y)) in coords:
            distances[(int(pos_x), int(pos_y))] = dist
            if len(distances) == len(coords):
                break
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))

    return [distances[coord] for coord in coords if coord in distances]

def distance_to_closest_coord(pos, coords, walls):
    return min(distance_to_coords(pos, coords, walls))

def closest_coord(pos, coords, walls):
    import operator
    dst = distance_to_coords(pos, coords, walls)
    min_index, min_value = min(enumerate(dst), key=operator.itemgetter(1))
    return (int(coords[min_index][0]), int(coords[min_index][1]))

def is_scared(state, ghost):
    return state.getGhostStateFromPosition(ghost).is_scared()

def get_safe_intersections(pos, ghosts, walls, fbd_coords=[]):
    # set in -1 the ghosts dist value and add them to the starting queue, after pacman
    f = (lambda g_pos: (g_pos[0], g_pos[1], -1, 0))
    fringe = Union[[(pos[0], pos[1], 0, 0)], map(f, ghosts)]
    expanded = set(fbd_coords)
    intersections = []
    while fringe:
        pos_x, pos_y, dist, ints_cross = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))

        # check if there's an intersection at this location
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)

        # dist != -1 == is not a ghost
        if len(nbrs) > 3 and dist != -1: #left, right, stop || up, down, stop
            ints_cross += 1
            intersections.append((int(pos_x), int(pos_y), dist, ints_cross))

        # spread out from the location to its neighbours
        for nbr_x, nbr_y in nbrs:
            if dist == -1:
                fringe.append((nbr_x, nbr_y, -1, ints_cross))
            else:
                fringe.append((nbr_x, nbr_y, dist+1, ints_cross))

    # return intersections, if any
    if len(intersections) > 1:
        return intersections

    # no intersections found
    return []

def safer_route_distance(pos, ghosts, walls, past_coord):
    from operator import itemgetter
    att2use = 3
    safe_intscs = get_safe_intersections(pos, ghosts, walls, [past_coord])
    if len(safe_intscs) == 0:
        return 0
    else:
        return max(safe_intscs,key=itemgetter(att2use))[att2use]

def get_coords_area(coords, rad):
    area = set([])
    for pos in coords:
        pos = (int(pos[0]), int(pos[1]))
        for i in range(rad+1):
            area.add((pos[0]-i,pos[1]))
            area.add((pos[0]+i,pos[1]))
            area.add((pos[0],pos[1]-i))
            area.add((pos[0],pos[1]+i))
            area.add((pos[0]-i,pos[1]-i))
            area.add((pos[0]-i,pos[1]+i))
            area.add((pos[0]+i,pos[1]-i))
            area.add((pos[0]+i,pos[1]+i))
    return list(area)

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """
    past_action = None
    initial_food = 0
    
    # Detectar cuando se encuentre en un tunel: Dar la distancia a la salida mas cercana hacia donde se este mirando?
    # TODO: Si el entrenamiento da por debajo de 100 puntos en los primeros 10 episodios, reiniciar.

    def get_features(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()
        capsules = map((lambda coord: (int(coord[0]), int(coord[1]))), capsules)

        features = util.Counter()

        features["bias"] = 1.0

        if self.initial_food == 0:
            self.initial_food = food.count()
        ifood = self.initial_food

        # NOTA: En el paper se sugiere un atributo que indique si se preserva la misma direccion que antes. Intente implementarlo pero cuando se usa el Pacman en algun momento da una accion "None".
        #if self.past_action == action:
        #    features["stay-in-direction"] = 1.0
        #else:
        #    features["stay-in-direction"] = 0.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        ns_ghosts = [g for g in ghosts if not is_scared(state, g)]

        # count the number of ghosts 1-step away
        ghosts_besides = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts if not is_scared(state, g))
        features["#-of-ghosts-1-step-away"] = ghosts_besides
        
        # calculate distances
        #NOTA: getCoords limita el area de la que el pacman se aleja alrededor de un fantasma
        area = get_coords_area(ns_ghosts, int(round(2*pow(food.count()/float(ifood),2))))
        food_dist = closest_food((next_x, next_y), food, ns_ghosts, walls, area, capsules)
        ns_ghosts_dist = distance_to_coords((next_x, next_y), ns_ghosts, walls)

        
        # if there is no danger of ghosts then add the food feature
        #(not ghosts_besides and food[next_x][next_y]) and
        is_food_next = food[next_x][next_y] or (next_x, next_y) in capsules
        if (len(ns_ghosts_dist) == 0 or food_dist < min(ns_ghosts_dist))/2 and (is_food_next):
            features["eats-food"] = 1.0            

            # Distance to scared ghosts
            #for gi in range(len(ghostsDists)):
            #    if is_scared(state, ghosts[gi]):
            #        features["distance-to-scared-ghost-"+str(gi+1)] = (float(ghostsDists[gi]) / (walls.width * walls.height))

        # Distance to closest capsule
        #capsules_dists = distance_to_coords((next_x, next_y), capsules, walls)
        #if len(capsules_dists) != 0:
        #    features["distance-to-closest-capsule"] = min(capsules_dists) / (walls.width * walls.height)
        
        # Distance to ghosts
        gi = 0
        for g in ghosts:
            if not is_scared(state, g):
                features["ghost-"+str(gi+1)+"-distance"] = (float(ns_ghosts_dist[gi]) / (walls.width * walls.height))
                gi += 1

        # Distance to closest intersection
        #if action != 'Stop':
        #    closestIntersection = get_closest_intersection((next_x, next_y), walls, action)
        #    if closestIntersection is not None:
        #        features["closest-intersection-distance"] = closestIntersection[0] / (walls.width * walls.height)
        
        # b(c): Distancia entre el fantasma mas cercano y la interseccion mas cercana (con respecto a ese fantasma)

        # Ghost danger
        #a = walls.width + walls.height
        #not_scared_ghosts = [g for g in ghosts if not is_scared(state, g)]
        #if action != 'Stop' and len(not_scared_ghosts) > 1:
        #    closestGhostCoords = closest_coord((next_x, next_y), ghosts, walls)
        #    closestIntersection = get_closest_intersection((next_x, next_y), walls, action)
        #    if closestIntersection is not None:
        #        ghost2intersection = distance_to_coord(closestGhostCoords, closestIntersection[1], walls)
        #        features["ghost-danger"] = (a + closestIntersection[0] - ghost2intersection) / float(a)
            #print features["ghost-danger"]


        # Distance to closest food
        if food_dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(food_dist) / (walls.width * walls.height)

        features.divideAll(10.0)

        self.past_action = action
        return features
