# graphicsGridworldDisplay.py
# ---------------------------
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


import util, graphicsUtils

class GraphicsGridworldDisplay:

    def __init__(self, gridworld, size=120, speed=1.0):
        self.gridworld = gridworld
        self.size = size
        self.speed = speed

    def start(self):
        setup(self.gridworld, size=self.size)

    def pause(self):
        wait_for_keys()

    def display_values(self, agent, current_state = None, message = 'Agent Values'):
        values = util.Counter()
        policy = {}
        states = self.gridworld.getStates()
        for state in states:
            values[state] = agent.getValue(state)
            policy[state] = agent.getPolicy(state)
        draw_values(self.gridworld, values, policy, current_state, message)
        sleep(0.05 / self.speed)

    def display_null_values(self, current_state = None, message = ''):
        values = util.Counter()
        states = self.gridworld.getStates()
        for state in states:
            values[state] = 0.0
        draw_null_values(self.gridworld, current_state,'')
        # draw_values(self.gridworld, values, policy, current_state, message)
        sleep(0.05 / self.speed)

    def display_q_values(self, agent, current_state = None, message = 'Agent Q-Values'):
        q_values = util.Counter()
        states = self.gridworld.getStates()
        for state in states:
            for action in self.gridworld.getPossibleActions(state):
                q_values[(state, action)] = agent.getQValue(state, action)
        draw_q_values(self.gridworld, q_values, current_state, message)
        sleep(0.05 / self.speed)

BACKGROUND_COLOR = formatColor(0,0,0)
EDGE_COLOR = formatColor(1,1,1)
OBSTACLE_COLOR = formatColor(0.5,0.5,0.5)
TEXT_COLOR = formatColor(1,1,1)
MUTED_TEXT_COLOR = formatColor(0.7,0.7,0.7)
LOCATION_COLOR = formatColor(0,0,1)

WINDOW_SIZE = -1
GRID_SIZE = -1
GRID_HEIGHT = -1
MARGIN = -1

def setup(gridworld, title = "Gridworld Display", size = 120):
    global GRID_SIZE, MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT
    grid = gridworld.grid
    GRID_SIZE = size
    GRID_HEIGHT = grid.height
    MARGIN = GRID_SIZE * 0.75
    screen_width = (grid.width - 1) * GRID_SIZE + MARGIN * 2
    screen_height = (grid.height - 0.5) * GRID_SIZE + MARGIN * 2

    begin_graphics(screen_width,
                   screen_height,
                   BACKGROUND_COLOR, title=title)

def draw_null_values(gridworld, current_state = None, message = ''):
    grid = gridworld.grid
    blank()
    for x in range(grid.width):
        for y in range(grid.height):
            state = (x, y)
            grid_type = grid[x][y]
            is_exit = (str(grid_type) != grid_type)
            is_current = (current_state == state)
            if grid_type == '#':
                draw_square(x, y, 0, 0, 0, None, None, True, False, is_current)
            else:
                draw_null_square(gridworld.grid, x, y, False, is_exit, is_current)
    pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
    text( pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")



def grid_world_actions(values, policy):
    value = values[state]
    action = None
    if (policy != None) and (state in policy):
        action = policy[state]
        actions = gridworld.getPossibleActions(state)
    if (action not in actions) and ('exit' in actions):
        action = 'exit'
    val_string = '%.2f' % value
    draw_square(x, y, value, min_value, max_value, val_string, action, False, is_exit, is_current)

def draw_values(gridworld, values, policy, current_state = None, message = 'State Values'):
    grid = gridworld.grid
    blank()
    for x in range(grid.width):
        for y in range(grid.height):
            state = (x, y)
            grid_type = grid[x][y]
            is_current = (current_state == state)
            if grid_type == '#':
                draw_square(x, y, 0, 0, 0, None, None, True, False, is_current)
            else:
                grid_world_actions(values, policy)
               
    pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
    text( pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")

def draw_q_values(gridworld, q_values, current_state = None, message = 'State-Action Q-Values'):
    grid = gridworld.grid
    blank()
    state_cross_actions = [[(state, action) for action in gridworld.getPossibleActions(state)] for state in gridworld.getStates()]
    q_states = reduce(lambda x,y: x+y, state_cross_actions, [])
    q_value_list = [q_values[(state, action)] for state, action in q_states] + [0.0]
    min_value = min(q_value_list)
    max_value = max(q_value_list)
    for x in range(grid.width):
        for y in range(grid.height):
            state = (x, y)
            grid_type = grid[x][y]
            is_exit = (str(grid_type) != grid_type)
            is_current = (current_state == state)
            actions = gridworld.getPossibleActions(state)
            if actions == None or len(actions) == 0:
                actions = [None]
            q = util.Counter()
            val_strings = {}
            for action in actions:
                v = q_values[(state, action)]
                q[action] += v
                val_strings[action] = '%.2f' % v
            if grid_type == '#':
                draw_square(x, y, 0, 0, 0, None, None, True, False, is_current)
            elif is_exit:
                action = 'exit'
                value = q[action]
                val_string = value
                draw_square(x, y, value, min_value, max_value, val_string, action, False, is_exit, is_current)
            else:
                draw_square_q(x, y, q, min_value, max_value, val_strings, actions, is_current)
    pos = to_screen(((grid.width - 1.0) / 2.0, - 0.8))
    text( pos, TEXT_COLOR, message, "Courier", -32, "bold", "c")


def blank():
    clear_screen()

def draw_null_square(grid,x, y, is_obstacle, is_terminal, is_current):

    square_color = get_color(0, -1, 1)

    if is_obstacle:
        square_color = OBSTACLE_COLOR

    (screen_x, screen_y) = to_screen((x, y))
    square( (screen_x, screen_y),
                   0.5* GRID_SIZE,
                   color = square_color,
                   filled = 1,
                   width = 1)

    square( (screen_x, screen_y),
                   0.5* GRID_SIZE,
                   color = EDGE_COLOR,
                   filled = 0,
                   width = 3)

    if is_terminal and not is_obstacle:
        square( (screen_x, screen_y),
                     0.4* GRID_SIZE,
                     color = EDGE_COLOR,
                     filled = 0,
                     width = 2)
        text( (screen_x, screen_y),
               TEXT_COLOR,
               str(grid[x][y]),
               "Courier", -24, "bold", "c")
    if not is_obstacle and is_current:
        circle( (screen_x, screen_y), 0.1*GRID_SIZE, LOCATION_COLOR, fillColor=LOCATION_COLOR )

    #   text( (screen_x, screen_y), text_color, valStr, "Courier", 24, "bold", "c")

def draw_square(x, y, val, min, max, val_str, action, is_obstacle, is_terminal, is_current):

    square_color = get_color(val, min, max)

    if is_obstacle:
        square_color = OBSTACLE_COLOR

    (screen_x, screen_y) = to_screen((x, y))
    square( (screen_x, screen_y),
                   0.5* GRID_SIZE,
                   color = square_color,
                   filled = 1,
                   width = 1)
    square( (screen_x, screen_y),
                   0.5* GRID_SIZE,
                   color = EDGE_COLOR,
                   filled = 0,
                   width = 3)
    if is_terminal and not is_obstacle:
        square( (screen_x, screen_y),
                     0.4* GRID_SIZE,
                     color = EDGE_COLOR,
                     filled = 0,
                     width = 2)


    if action == 'north':
        polygon( [(screen_x, screen_y - 0.45*GRID_SIZE), (screen_x+0.05*GRID_SIZE, screen_y-0.40*GRID_SIZE), (screen_x-0.05*GRID_SIZE, screen_y-0.40*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
    if action == 'south':
        polygon( [(screen_x, screen_y + 0.45*GRID_SIZE), (screen_x+0.05*GRID_SIZE, screen_y+0.40*GRID_SIZE), (screen_x-0.05*GRID_SIZE, screen_y+0.40*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
    if action == 'west':
        polygon( [(screen_x-0.45*GRID_SIZE, screen_y), (screen_x-0.4*GRID_SIZE, screen_y+0.05*GRID_SIZE), (screen_x-0.4*GRID_SIZE, screen_y-0.05*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)
    if action == 'east':
        polygon( [(screen_x+0.45*GRID_SIZE, screen_y), (screen_x+0.4*GRID_SIZE, screen_y+0.05*GRID_SIZE), (screen_x+0.4*GRID_SIZE, screen_y-0.05*GRID_SIZE)], EDGE_COLOR, filled = 1, smoothed = False)


    text_color = TEXT_COLOR

    if not is_obstacle and is_current:
        circle( (screen_x, screen_y), 0.1*GRID_SIZE, outlineColor=LOCATION_COLOR, fillColor=LOCATION_COLOR )

    if not is_obstacle:
        text( (screen_x, screen_y), text_color, val_str, "Courier", -30, "bold", "c")

def square_actions(actions):
    for action in actions:
        wedge_color = get_color(q_vals[action], min_val, max_val)
        if action == 'north':
            polygon( (center, nw, ne), wedge_color, filled = 1, smoothed = False)
            #text(n, text_color, val_str, "Courier", 8, "bold", "n")
        if action == 'south':
            polygon( (center, sw, se), wedge_color, filled = 1, smoothed = False)
            #text(s, text_color, val_str, "Courier", 8, "bold", "s")
        if action == 'east':
            polygon( (center, ne, se), wedge_color, filled = 1, smoothed = False)
            #text(e, text_color, val_str, "Courier", 8, "bold", "e")
        if action == 'west':
            polygon( (center, nw, sw), wedge_color, filled = 1, smoothed = False)
            #text(w, text_color, val_str, "Courier", 8, "bold", "w")

def square_actions_text(actions):
    for action in actions:
        text_color = TEXT_COLOR
        if q_vals[action] < max(q_vals.values()): text_color = MUTED_TEXT_COLOR
        val_str = ""
        if action in val_strs:
            val_str = val_strs[action]
        h = -20
        if action == 'north':
            #polygon( (center, nw, ne), wedge_color, filled = 1, smooth = 0)
            text(n, text_color, val_str, "Courier", h, "bold", "n")
        if action == 'south':
            #polygon( (center, sw, se), wedge_color, filled = 1, smooth = 0)
            text(s, text_color, val_str, "Courier", h, "bold", "s")
        if action == 'east':
            #polygon( (center, ne, se), wedge_color, filled = 1, smooth = 0)
            text(e, text_color, val_str, "Courier", h, "bold", "e")
        if action == 'west':
            #polygon( (center, nw, sw), wedge_color, filled = 1, smooth = 0)
            text(w, text_color, val_str, "Courier", h, "bold", "w")

def draw_square_q(x, y, q_vals, min_val, max_val, val_strs, best_actions, is_current):
    (screen_x, screen_y) = to_screen((x, y))
    nw = (screen_x-0.5*GRID_SIZE, screen_y-0.5*GRID_SIZE)
    ne = (screen_x+0.5*GRID_SIZE, screen_y-0.5*GRID_SIZE)
    se = (screen_x+0.5*GRID_SIZE, screen_y+0.5*GRID_SIZE)
    sw = (screen_x-0.5*GRID_SIZE, screen_y+0.5*GRID_SIZE)
    actions = q_vals.keys()
    square_actions(actions)
    square( (screen_x, screen_y),
                   0.5* GRID_SIZE,
                   color = EDGE_COLOR,
                   filled = 0,
                   width = 3)
    line(ne, sw, color = EDGE_COLOR)
    line(nw, se, color = EDGE_COLOR)

    if is_current:
        circle( (screen_x, screen_y), 0.1*GRID_SIZE, LOCATION_COLOR, fillColor=LOCATION_COLOR )
    square_actions_text(actions)
    


def get_color(val, min_val, max):
    r, g = 0.0, 0.0
    if val < 0 and min_val < 0:
        r = val * 0.65 / min_val
    if val > 0 and max > 0:
        g = val * 0.65 / max
    return formatColor(r,g,0.0)


def square(pos, size, color, filled, width):
    x, y = pos
    dx, dy = size, size
    return polygon([(x - dx, y - dy), (x - dx, y + dy), (x + dx, y + dy), (x + dx, y - dy)], outlineColor=color, fillColor=color, filled=filled, width=width, smoothed=False)


def to_screen(point):
    ( gamex, gamey ) = point
    x = gamex*GRID_SIZE + MARGIN
    y = (GRID_HEIGHT - gamey - 1)*GRID_SIZE + MARGIN
    return ( x, y )

def to_grid(point):
    (x1, y1) = point
    x = int ((y1 - MARGIN + GRID_SIZE * 0.5) / GRID_SIZE)
    y = int ((x1 - MARGIN + GRID_SIZE * 0.5) / GRID_SIZE)
    print (point, "-->", (x, y))
    return (x, y)
