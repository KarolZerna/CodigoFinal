#!/usr/bin/env python
# -*- coding: utf-8 -*-
# graphicsDisplay.py
# ------------------
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


import graphicsUtils
import math, time
from game import Directions

###########################
#  GRAPHICS DISPLAY CODE  #
###########################

# Most code by Dan Klein and John Denero written or rewritten for cs188, UC Berkeley.
# Some code from a Pacman implementation by LiveWires, and used / modified with permission.

DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = formatColor(0,0,0)
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 254.0/255.0)
INFO_PANE_COLOR = formatColor(.4,.4,0)
SCORE_COLOR = formatColor(.9, .9, .9)
PACMAN_OUTLINE_WIDTH = 2
PACMAN_CAPTURE_OUTLINE_WIDTH = 4

GHOST_COLORS = []
GHOST_COLORS.append(formatColor(.9,0,0)) # Red
GHOST_COLORS.append(formatColor(0,.3,.9)) # Blue
GHOST_COLORS.append(formatColor(.98,.41,.07)) # Orange
GHOST_COLORS.append(formatColor(.1,.75,.7)) # Green
GHOST_COLORS.append(formatColor(1.0,0.6,0.0)) # Yellow
GHOST_COLORS.append(formatColor(.4,0.13,0.91)) # Purple

TEAM_COLORS = GHOST_COLORS[:2]

GHOST_SHAPE = [
    ( 0,    0.3 ),
    ( 0.25, 0.75 ),
    ( 0.5,  0.3 ),
    ( 0.75, 0.75 ),
    ( 0.75, -0.5 ),
    ( 0.5,  -0.75 ),
    (-0.5,  -0.75 ),
    (-0.75, -0.5 ),
    (-0.75, 0.75 ),
    (-0.5,  0.3 ),
    (-0.25, 0.75 )
  ]
GHOST_SIZE = 0.65
SCARED_COLOR = formatColor(1,1,1)

GHOST_VEC_COLORS = map(colorToVector, GHOST_COLORS)

PACMAN_COLOR = formatColor(254.0/255.0,254.0/255.0,61.0/255)
PACMAN_SCALE = 0.5

# Food
FOOD_COLOR = formatColor(1,1,1)
FOOD_SIZE = 0.1

# Laser
LASER_COLOR = formatColor(1,0,0)
LASER_SIZE = 0.02

# Capsule graphics
CAPSULE_COLOR = formatColor(1,1,1)
CAPSULE_SIZE = 0.25

# Drawing walls
WALL_RADIUS = 0.15

class info_pane:
    def __init__(self, layout, grid_size):
        self.grid_size = grid_size
        self.width = (layout.width) * grid_size
        self.base = (layout.height + 1) * grid_size
        self.height = INFO_PANE_HEIGHT
        self.font_size = 24
        self.text_color = PACMAN_COLOR
        self.draw_pane()

    def to_screen(self, pos, y = None):
        """
          Translates a point relative from the bottom left of the info pane.
        """
        if y == None:
            x,y = pos
        else:
            x = pos

        x = self.grid_size + x # Margin
        y = self.base + y
        return x,y

    def draw_pane(self):
        self.score_text = text( self.to_screen(0, 0  ), self.text_color, "PUNTOS:    0", "arcadepix", self.font_size, "bold")

    def initialize_ghost_distances(self, distances):
        self.ghost_distance_text = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = text( self.to_screen(self.width/2 + self.width/8 * i, 0), GHOST_COLORS[i+1], d, "arcadepix", size, "bold")
            self.ghost_distance_text.append(t)

    def update_score(self, score):
        changeText(self.score_text, "PUNTOS: % 4d" % score)

    def text(self):
        return "RED TEAM"

    def set_team(self, is_blue):
        text = text()
        if is_blue: text = "BLUE TEAM"
        self.team_text = text( self.to_screen(300, 0  ), self.text_color, text, "arcadepix", self.font_size, "bold")

    def update_ghost_distances(self, distances):
        if len(distances) == 0: return
        if 'ghost_distance_text' not in dir(self): self.initialize_ghost_distances(distances)
        else:
            for i, d in enumerate(distances):
                changeText(self.ghost_distance_text[i], d)

    def draw_ghost(self):
        pass #Empty

    def draw_pacman(self):
        pass #Empty

    def draw_warning(self):
        pass #Empty

    def clear_icon(self):
        pass #Empty

    def update_message(self, message):
        pass #Empty

    def clear_message(self):
        pass #Empty
    
    def __del__(self):
        remove_from_screen(self.score_text)


class PacmanGraphics:
    def __init__(self, zoom=1.0, frame_time=0.0, capture=False):
        self.have_window = 0
        self.current_ghost_images = {}
        self.pacman_image = None
        self.zoom = zoom
        self.grid_size = DEFAULT_GRID_SIZE * zoom
        self.capture = capture
        self.frame_time = frame_time
        self.distribution_images = None
        
        self.is_window_open = False
        self.last_mode = None
        self.font_size = 24
        self.text_color = PACMAN_COLOR
        self.result_message = None
        self.show_training_screen = False
        self.training_message = None
        self.training_screen_count = 0
        self.start_message = None
        self.start_message1 = None
        self.start_message2 = None
        self.start_message3 = None
        self.start_message4 = None
        self.start_message5 = None
        self.start_message7 = None

        self.selection = 1

    def check_null_display(self):
        return False
    
    # TODO: Investigar la pantalla completa :
    #           http://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
    def initialize(self, state = None, mode = "pacman", is_blue = False):

        self.selection = 1
        
        print (self.last_mode, mode)
        if self.last_mode == "pacman":   # Clear pacman screen
            # not mode == "pacman"
            self.remove_static_objects(True)
            self.remove_agents()
            del self.info_pane
        
        if self.last_mode == "training" and mode != "training": # Clear training screen
            self.hide_training_message()
                
        if self.last_mode == "start":    # Clear start screen
            self.hide_start_message()
        
        #graphicsUtils.resetBindings()

        if mode == "pacman":            # Initialize pacman screen
            self.is_blue = is_blue
            self.start_graphics(state)
            self.draw_static_objects(state)
            self.draw_agent_objects(state)

            # Information
            self.previous_state = state
            
        if mode == "training":          # Initialize training screen
            if self.last_mode == "training":
                self.training_screen_count += 1
            self.show_training_message()
            
        if mode == "start":          # Initialize starting screen
            self.show_start_message()
        
        # Save last mode
        self.last_mode = mode
    
    def positions(self):
        x = self.screen_width/2-self.grid_size-200
        y = self.screen_height/2-self.grid_size-20

        self.start_message6 = text ((x,y-120), self.text_color, "PACMAN","arcadepix", self.font_size*3, "bold")

        self.start_message5 = text ((x+120,y-30), self.text_color, "Inteligente","arcadepix", self.font_size, "bold")
        x += 370
        self.start_message7 = text ((x-260,y+30), self.text_color, "ᗧ  ", "arcadepix", self.font_size, "bold")
        self.start_message8 = text ((x-250,y+30), SCARED_COLOR, " •••    •• ", "arcadepix", self.font_size, "bold")
        self.start_message9 = text ((x-240,y+30), formatColor(0,.3,.9), "    ᗣ ", "arcadepix", self.font_size, "bold")

        x -= 270
        y += 100
        self.start_message2 = text ((x+40,y), self.text_color, "Historia","arcadepix", self.font_size, "bold")
        y += 50
        self.start_message3 = text ((x+43,y), self.text_color, "Infinito","arcadepix", self.font_size, "bold")
        y += 50
        self.start_message4 = text ((x+68,y), self.text_color, "Demo","arcadepix", self.font_size, "bold")
        pos_x = x - 20
        self.start_message = text ((pos_x, y-100), self.text_color, ">","arcadepix", self.font_size, "bold")
        pos_y = y - 100


    def options (self):
        keys = []
        keys = wait_for_keys()
        if 'Return' in keys:
            yield
        if 'Escape' in keys:
            exit()

    def movements(self, pos_y, pos_x):
        keys = []
        keys = wait_for_keys()
        if 'Down' in keys:
            self.hide_start_message()
            if pos_y == y:
                pos_y = y - 100
                self.selection = 1
            else:
                pos_y += 50
                self.selection += 1
            self.start_message = text ((pos_x,pos_y), self.text_color, ">","arcadepix", self.font_size, "bold")

        if 'Up' in keys:
            self.hide_start_message()
            if pos_y == y - 100:
                pos_y = y
                self.selection = 3
            else: 
                pos_y -= 50
                self.selection -= 1
            self.start_message = text ((pos_x,pos_y), self.text_color, ">","arcadepix", self.font_size, "bold")

    def show_start_message(self):
        positions()
        keys = []
        wait_for_release()
        while True:
            options()
            movements(pos_y, pos_x)
            # Wait for release
            keys = keys_waiting() + keys_pressed()
            while len(keys) != 0:
                keys = keys_waiting() + keys_pressed()
                sleep(0.05)
        self.clear_start_screen()


    def clear_start_screen(self):

        remove_from_screen(self.start_message)
        remove_from_screen(self.start_message1)
        remove_from_screen(self.start_message2)
        remove_from_screen(self.start_message3)
        remove_from_screen(self.start_message4)
        remove_from_screen(self.start_message5)
        remove_from_screen(self.start_message6)
        remove_from_screen(self.start_message7)
        remove_from_screen(self.start_message8)
        remove_from_screen(self.start_message9)

    def hide_start_message(self):
        if self.start_message is not None:
            remove_from_screen(self.start_message)
            self.start_message = None
    
    def show_training_message(self):
        x = self.screen_width/2-self.grid_size-60
        y = self.screen_height/2-self.grid_size-5
        
        if self.training_message is None:
            self.training_message = text( (x,y), self.text_color, "TRAINING", "arcadepix", self.font_size, "bold")
            self.training_screen_count = 0
        
        if self.training_screen_count % 4 == 0:
            changeText(self.training_message, "TRAINING")
        if self.training_screen_count % 4 == 1:
            changeText(self.training_message, "TRAINING.")
        if self.training_screen_count % 4 == 2:
            changeText(self.training_message, "TRAINING..")
        if self.training_screen_count % 4 == 3:
            changeText(self.training_message, "TRAINING...")
            
        refresh()
            
    def hide_training_message(self):
        if self.training_message is not None:
            remove_from_screen(self.training_message)
            self.training_message = None
        refresh()
    
    def show_result_message(self, is_win):
        x = self.screen_width/2-self.grid_size
        y = self.screen_height/2-self.grid_size-5
        # TODO: Fondo atras del mensaje
        #self.resultMessageBackground = 
        if is_win:
            self.result_message = text( (x,y), self.text_color, "WIN", "arcadepix", self.font_size, "bold")
        else:
            self.result_message = text( (x-20,y), self.text_color, "LOSS", "arcadepix", self.font_size, "bold")
        refresh()
    
    def hide_result_message(self):
        if self.result_message is not None:
            remove_from_screen(self.result_message)
            self.result_message = None
        refresh()
        
    def to_screen(self, pos, y = None):
        """
          Translates a point relative from the bottom left of the info pane.
        """
        base = (self.layout.height + 1) * self.grid_size
        if y == None:
            x,y = pos
        else:
            x = pos

        x = self.grid_size + x # Margin
        y = base + y
        return x,y
                

    def start_graphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        if not self.is_window_open:
            self.make_window(self.width, self.height)
        self.info_pane = info_pane(layout, self.grid_size)
        self.current_state = layout

    def draw_distributions(self, state):
        walls = state.layout.walls
        dist = []
        for x in range(walls.width):
            distx = []
            dist.append(distx)
            for y in range(walls.height):
                ( screen_x, screen_y ) = self.to_screen( (x, y) )
                block = square( (screen_x, screen_y),
                                0.5 * self.grid_size,
                                color = BACKGROUND_COLOR,
                                filled = 1, behind=2)
                distx.append(block)
        self.distribution_images = dist

    def draw_static_objects(self, state):
        layout = self.layout
        self.walls_images = self.draw_walls(layout.walls)
        self.food = self.draw_food(layout.food)
        self.capsules = self.draw_capsules(layout.capsules)
        refresh()

    def draw_agent_objects(self, state):
        self.agent_images = [] # (agent_state, image)
        for index, agent in enumerate(state.agentStates):
            if agent.isPacman:
                image = self.draw_pacman(agent, index)
                self.agent_images.append( (agent, image) )
            else:
                image = self.draw_ghost(agent, index)
                self.agent_images.append( (agent, image) )
        refresh()
        
    def remove_agents(self):
        for agent, image in self.agent_images:
            for item in image:
                remove_from_screen(item)
        
    def remove_all_food(self):
        for i in range(len(self.food)):
            for j in range(len(self.food[i])):
                if self.food[i][j] is not None:
                    remove_from_screen(self.food[i][j])
                    
    def remove_all_capsules(self):
        for key in self.capsules:
            remove_from_screen(self.capsules[key])
            
    def remove_walls(self):
        for image in self.walls_images:
            remove_from_screen(image)
            
    def remove_static_objects(self, remove_walls=True):
        self.remove_all_food()
        self.remove_all_capsules()
        if remove_walls: # Prevent flash
            self.remove_walls()
        
    def reset_stage(self, state):
        self.remove_static_objects()
        self.remove_agents()
        
        self.draw_static_objects(state)
        
        self.previous_state = state
        
        refresh()

    def swap_images(self, agent_index, new_state):
        """
          Changes an image from a ghost to a pacman or vis versa (for capture)
        """
        prev_state, prev_image = self.agent_images[agent_index]
        for item in prev_image: remove_from_screen(item)
        if new_state.isPacman:
            image = self.draw_pacman(new_state, agent_index)
            self.agent_images[agent_index] = (new_state, image )
        else:
            image = self.draw_ghost(new_state, agent_index)
            self.agent_images[agent_index] = (new_state, image )
        refresh()

    def update(self, new_state):
        agent_index = new_state._agentMoved
        agent_state = new_state.agent_states[agent_index]

        if self.agent_images[agent_index][0].isPacman != agent_state.isPacman: self.swap_images(agent_index, agent_state)
        prev_state, prev_image = self.agent_images[agent_index]
        if agent_state.isPacman:
            self.animate_pacman(agent_state, prev_state, prev_image)
        else:
            self.move_ghost(agent_state, agent_index, prev_state, prev_image)
        self.agent_images[agent_index] = (agent_state, prev_image)

        if new_state._foodEaten != None:
            self.remove_food(new_state._foodEaten, self.food)
        if new_state._capsuleEaten != None:
            self.remove_capsule(new_state._capsuleEaten, self.capsules)
        self.info_pane.update_score(new_state.score)
        if 'ghostDistances' in dir(new_state):
            self.info_pane.update_ghost_distances(new_state.ghostDistances)
        #save_frame()
    
    def make_window(self, width, height):
        if not self.is_window_open:
            grid_width = (width-1) * self.grid_size
            grid_height = (height-1) * self.grid_size
            self.screen_width = 2*self.grid_size + grid_width
            self.screen_height = 2*self.grid_size + grid_height + INFO_PANE_HEIGHT

            begin_graphics(self.screen_width,
                        self.screen_height,
                        BACKGROUND_COLOR,
                        "CS188 Pacman")
            
            self.is_window_open = True
        #TODO: Esto depende de grid_size, no deberia. O habria que buscar algun comando para resize.

    def draw_pacman(self, pacman, index):
        position = self.get_position(pacman)
        screen_point = self.to_screen(position)
        endpoints = self.get_end_points(self.get_direction(pacman))

        width = PACMAN_OUTLINE_WIDTH
        outline_color = PACMAN_COLOR
        fill_color = PACMAN_COLOR

        if self.capture:
            outline_color = TEAM_COLORS[index % 2]
            fill_color = GHOST_COLORS[index]
            width = PACMAN_CAPTURE_OUTLINE_WIDTH

        return [circle(screen_point, PACMAN_SCALE * self.grid_size,
                       fill_color = fill_color, outline_color = outline_color,
                       endpoints = endpoints,
                       width = width)]

    def get_end_points(self, direction, position=(0,0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi* pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180+delta, 180-delta)
        elif (direction == 'North'):
            endpoints = (90+delta, 90-delta)
        elif (direction == 'South'):
            endpoints = (270+delta, 270-delta)
        else:
            endpoints = (0+delta, 0-delta)
        return endpoints

    def move_pacman(self, position, direction, image):
        screen_position = self.to_screen(position)
        endpoints = self.get_end_points( direction, position )
        r = PACMAN_SCALE * self.grid_size
        moveCircle(image[0], screen_position, r, endpoints)
        refresh()

    def animate_pacman(self, pacman, prev_pacman, image):
        if self.frame_time < 0:
            print ('Press any key to step forward, "q" to play')
            keys = wait_for_keys()
            if 'q' in keys:
                self.frame_time = 0.1
        if self.frame_time > 0.01 or self.frame_time < 0:
            fx, fy = self.get_position(prev_pacman)
            px, py = self.get_position(pacman)
            frames = 4.0
            for i in range(1,int(frames) + 1):
                pos = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames
                self.move_pacman(pos, self.get_direction(pacman), image)
                refresh()
                sleep(abs(self.frame_time) / frames)
        else:
            self.move_pacman(self.get_position(pacman), self.get_direction(pacman), image)
        refresh()

    def get_ghost_color(self, ghost, ghost_index):
        if ghost.scaredTimer > 0:
            return SCARED_COLOR
        else:
            return GHOST_COLORS[ghost_index]

    def draw_ghost(self, ghost, agent_index):
        pos = self.get_position(ghost)
        direction = self.get_direction(ghost)
        (screen_x, screen_y) = (self.to_screen(pos) )
        coords = []
        for (x, y) in GHOST_SHAPE:
            coords.append((x*self.grid_size*GHOST_SIZE + screen_x, y*self.grid_size*GHOST_SIZE + screen_y))

        colour = self.get_ghost_color(ghost, agent_index)
        body = polygon(coords, colour, filled = 1)
        WHITE = formatColor(1.0, 1.0, 1.0)
        BLACK = formatColor(0.0, 0.0, 0.0)

        dx = 0
        dy = 0
        if direction == 'North':
            dy = -0.2
        if direction == 'South':
            dy = 0.2
        if direction == 'East':
            dx = 0.2
        if direction == 'West':
            dx = -0.2
        left_eye = circle((screen_x+self.grid_size*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy/1.5)), self.grid_size*GHOST_SIZE*0.2, WHITE, WHITE)
        right_eye = circle((screen_x+self.grid_size*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy/1.5)), self.grid_size*GHOST_SIZE*0.2, WHITE, WHITE)
        left_pupil = circle((screen_x+self.grid_size*GHOST_SIZE*(-0.3+dx), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy)), self.grid_size*GHOST_SIZE*0.08, BLACK, BLACK)
        right_pupil = circle((screen_x+self.grid_size*GHOST_SIZE*(0.3+dx), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy)), self.grid_size*GHOST_SIZE*0.08, BLACK, BLACK)
        ghost_image_parts = []
        ghost_image_parts.append(body)
        ghost_image_parts.append(left_eye)
        ghost_image_parts.append(right_eye)
        ghost_image_parts.append(left_pupil)
        ghost_image_parts.append(right_pupil)

        return ghost_image_parts

    def move_eyes(self, pos, direction, eyes):
        (screen_x, screen_y) = (self.to_screen(pos) )
        dx = 0
        dy = 0
        if direction == 'North':
            dy = -0.2
        if direction == 'South':
            dy = 0.2
        if direction == 'East':
            dx = 0.2
        if direction == 'West':
            dx = -0.2
        moveCircle(eyes[0],(screen_x+self.grid_size*GHOST_SIZE*(-0.3+dx/1.5), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy/1.5)), self.grid_size*GHOST_SIZE*0.2)
        moveCircle(eyes[1],(screen_x+self.grid_size*GHOST_SIZE*(0.3+dx/1.5), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy/1.5)), self.grid_size*GHOST_SIZE*0.2)
        moveCircle(eyes[2],(screen_x+self.grid_size*GHOST_SIZE*(-0.3+dx), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy)), self.grid_size*GHOST_SIZE*0.08)
        moveCircle(eyes[3],(screen_x+self.grid_size*GHOST_SIZE*(0.3+dx), screen_y-self.grid_size*GHOST_SIZE*(0.3-dy)), self.grid_size*GHOST_SIZE*0.08)

    def move_ghost(self, ghost, ghost_index, prev_ghost, ghost_image_parts):
        old_x, old_y = self.to_screen(self.get_position(prev_ghost))
        new_x, new_y = self.to_screen(self.get_position(ghost))
        delta = new_x - old_x, new_y - old_y

        for ghost_image_part in ghost_image_parts:
            move_by(ghost_image_part, delta)
        refresh()

        if ghost.scaredTimer > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[ghost_index]
        edit(ghost_image_parts[0], ('fill', color), ('outline', color))
        self.move_eyes(self.get_position(ghost), self.get_direction(ghost), ghost_image_parts[-4:])
        refresh()

    def get_position(self, agent_state):
        if agent_state.configuration == None: return (-1000, -1000)
        return agent_state.get_position()

    def get_direction(self, agent_state):
        if agent_state.configuration == None: return Directions.STOP
        return agent_state.configuration.get_direction()

    def finish(self):
        end_graphics()

    def to_screen(self, point):
        ( x, y ) = point
        x = (x + 1)*self.grid_size
        y = (self.height  - y)*self.grid_size
        return ( x, y )


    def ne_quadrant(self, n_is_wall, e_is_wall, wall_color, screen, screen2, ne_is_wall):
        # NE quadrant
        if (not n_is_wall) and (not e_is_wall):
            # inner circle
            board_images.append(circle(screen2, WALL_RADIUS * self.grid_size, wall_color, wall_color, (0,91), 'arc'))
        if (n_is_wall) and (not e_is_wall):
            # vertical line
            board_images.append(line(add(screen, (self.grid_size*WALL_RADIUS, 0)), add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(-0.5)-1)), wall_color))
        if (not n_is_wall) and (e_is_wall):
            # horizontal line
            board_images.append(line(add(screen, (0, self.grid_size*(-1)*WALL_RADIUS)), add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*WALL_RADIUS)), wall_color))
        if (n_is_wall) and (e_is_wall) and (not ne_is_wall):
            # outer circle
            board_images.append(circle(add(screen2, (self.grid_size*2*WALL_RADIUS, self.grid_size*(-2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1, wall_color, wall_color, (180,271), 'arc'))
            board_images.append(line(add(screen, (self.grid_size*2*WALL_RADIUS-1, self.grid_size*(-1)*WALL_RADIUS)), add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*WALL_RADIUS)), wall_color))
            board_images.append(line(add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(-2)*WALL_RADIUS+1)), add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(-0.5))), wall_color))
    
    def nw_quadrant(self, n_is_wall, w_is_wall, wall_color, screen, screen2, nw_is_wall):
        # NW quadrant
        if (not n_is_wall) and (not w_is_wall):
            # inner circle
            board_images.append(circle(screen2, WALL_RADIUS * self.grid_size, wall_color, wall_color, (90,181), 'arc'))
        if (n_is_wall) and (not w_is_wall):
            # vertical line
            board_images.append(line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, 0)), add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(-0.5)-1)), wall_color))
        if (not n_is_wall) and (w_is_wall):
            # horizontal line
            board_images.append(line(add(screen, (0, self.grid_size*(-1)*WALL_RADIUS)), add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(-1)*WALL_RADIUS)), wall_color))
        if (n_is_wall) and (w_is_wall) and (not nw_is_wall):
            # outer circle
            board_images.append(circle(add(screen2, (self.grid_size*(-2)*WALL_RADIUS, self.grid_size*(-2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1, wall_color, wall_color, (270,361), 'arc'))
            board_images.append(line(add(screen, (self.grid_size*(-2)*WALL_RADIUS+1, self.grid_size*(-1)*WALL_RADIUS)), add(screen, (self.grid_size*(-0.5), self.grid_size*(-1)*WALL_RADIUS)), wall_color))
            board_images.append(line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(-2)*WALL_RADIUS+1)), add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(-0.5))), wall_color))
    
    def se_quadrant(self, s_is_wall, e_is_wall, wall_color, screen, screen2, se_is_wall):
        # SE quadrant
        if (not s_is_wall) and (not e_is_wall):
           # inner circle
            board_images.append(circle(screen2, WALL_RADIUS * self.grid_size, wall_color, wall_color, (270,361), 'arc'))
        if (s_is_wall) and (not e_is_wall):
            # vertical line
            board_images.append(line(add(screen, (self.grid_size*WALL_RADIUS, 0)), add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(0.5)+1)), wall_color))
        if (not s_is_wall) and (e_is_wall):
            # horizontal line
            board_images.append(line(add(screen, (0, self.grid_size*(1)*WALL_RADIUS)), add(screen, (self.grid_size*0.5+1, self.grid_size*(1)*WALL_RADIUS)), wall_color))
        if (s_is_wall) and (e_is_wall) and (not se_is_wall):
            # outer circle
            board_images.append(circle(add(screen2, (self.grid_size*2*WALL_RADIUS, self.grid_size*(2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1, wall_color, wall_color, (90,181), 'arc'))
            board_images.append(line(add(screen, (self.grid_size*2*WALL_RADIUS-1, self.grid_size*(1)*WALL_RADIUS)), add(screen, (self.grid_size*0.5, self.grid_size*(1)*WALL_RADIUS)), wall_color))
            board_images.append(line(add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(2)*WALL_RADIUS-1)), add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(0.5))), wall_color))
    
    def sw_quadrant(self, s_is_wall, w_is_wall, wall_color, screen, screen2, sw_is_wall):
        # SW quadrant
        if (not s_is_wall) and (not w_is_wall):
        # inner circle
            board_images.append(circle(screen2, WALL_RADIUS * self.grid_size, wall_color, wall_color, (180,271), 'arc'))
        if (s_is_wall) and (not w_is_wall):
            # vertical line
            board_images.append(line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, 0)), add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(0.5)+1)), wall_color))
        if (not s_is_wall) and (w_is_wall):
            # horizontal line
            board_images.append(line(add(screen, (0, self.grid_size*(1)*WALL_RADIUS)), add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(1)*WALL_RADIUS)), wall_color))
        if (s_is_wall) and (w_is_wall) and (not sw_is_wall):
            # outer circle
            board_images.append(circle(add(screen2, (self.grid_size*(-2)*WALL_RADIUS, self.grid_size*(2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1, wall_color, wall_color, (0,91), 'arc'))
            board_images.append(line(add(screen, (self.grid_size*(-2)*WALL_RADIUS+1, self.grid_size*(1)*WALL_RADIUS)), add(screen, (self.grid_size*(-0.5), self.grid_size*(1)*WALL_RADIUS)), wall_color))
            board_images.append(line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(2)*WALL_RADIUS-1)), add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(0.5))), wall_color))

    def draw_walls(self, wall_matrix):
        board_images = []
        wall_color = WALL_COLOR
        for x_num, x in enumerate(wall_matrix):
            if self.capture and (x_num * 2) < wall_matrix.width: wall_color = TEAM_COLORS[0]
            if self.capture and (x_num * 2) >= wall_matrix.width: wall_color = TEAM_COLORS[1]

            for y_num, cell in enumerate(x):
                if cell: # There's a wall here
                    pos = (x_num, y_num)
                    screen = self.to_screen(pos)
                    screen2 = self.to_screen(pos)
                    
                    # draw each quadrant of the square based on adjacent walls
                    w_is_wall = self.is_wall(x_num-1, y_num, wall_matrix)
                    e_is_wall = self.is_wall(x_num+1, y_num, wall_matrix)
                    n_is_wall = self.is_wall(x_num, y_num+1, wall_matrix)
                    s_is_wall = self.is_wall(x_num, y_num-1, wall_matrix)
                    nw_is_wall = self.is_wall(x_num-1, y_num+1, wall_matrix)
                    sw_is_wall = self.is_wall(x_num-1, y_num-1, wall_matrix)
                    ne_is_wall = self.is_wall(x_num+1, y_num+1, wall_matrix)
                    se_is_wall = self.is_wall(x_num+1, y_num-1, wall_matrix)

                    ne_quadrant(n_is_wall, e_is_wall, wall_color, screen, screen2, ne_is_wall)
                    nw_quadrant(n_is_wall, w_is_wall, wall_color, screen, screen2, nw_is_wall)
                    se_quadrant(s_is_wall, e_is_wall, wall_color, screen, screen2, se_is_wall)
                    sw_quadrant(s_is_wall, w_is_wall, wall_color, screen, screen2, sw_is_wall)

            return board_images

    def is_wall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def draw_food(self, foodMatrix ):
        food_images = []
        color = FOOD_COLOR
        for x_num, x in enumerate(foodMatrix):
            if self.capture and (x_num * 2) <= foodMatrix.width: color = TEAM_COLORS[0]
            if self.capture and (x_num * 2) > foodMatrix.width: color = TEAM_COLORS[1]
            image_row = []
            food_images.append(image_row)
            for y_num, cell in enumerate(x):
                if cell: # There's food here
                    screen = self.to_screen((x_num, y_num ))
                    dot = circle( screen,
                                  FOOD_SIZE * self.grid_size,
                                  outline_color = color, fill_color = color,
                                  width = 1)
                    image_row.append(dot)
                else:
                    image_row.append(None)
        return food_images

    def draw_capsules(self, capsules ):
        capsule_images = {}
        for capsule in capsules:
            ( screen_x, screen_y ) = self.to_screen(capsule)
            dot = circle( (screen_x, screen_y),
                              CAPSULE_SIZE * self.grid_size,
                              outline_color = CAPSULE_COLOR,
                              fill_color = CAPSULE_COLOR,
                              width = 1)
            capsule_images[capsule] = dot
        return capsule_images

    def remove_food(self, cell, food_images):
        x, y = cell
        remove_from_screen(food_images[x][y])

    def remove_capsule(self, cell, capsule_images):
        x, y = cell
        remove_from_screen(capsule_images[(x, y)])

    def draw_expanded_cells(self, cells):
        """
        Draws an overlay of expanded grid positions for search agents
        """
        n = float(len(cells))
        base_color = [1.0, 0.0, 0.0]
        self.clear_expanded_cells()
        self.expanded_cells = []
        for k, cell in enumerate(cells):
            screen_pos = self.to_screen( cell)
            cell_color = formatColor(*[(n-k) * c * .5 / n + .25 for c in base_color])
            block = square(screen_pos,
                     0.5 * self.grid_size,
                     color = cell_color,
                     filled = 1, behind=2)
            self.expanded_cells.append(block)
            if self.frame_time < 0:
                refresh()

    def clear_expanded_cells(self):
        if 'expandedCells' in dir(self) and len(self.expanded_cells) > 0:
            for cell in self.expanded_cells:
                remove_from_screen(cell)


    def updated_distributions(self, distributions):
        "Draws an agent's belief distributions"
        # copy all distributions so we don't change their state
        distributions = map(lambda x: x.copy(), distributions)
        if self.distribution_images == None:
            self.draw_distributions(self.previous_state)
        for x in range(len(self.distribution_images)):
            for y in range(len(self.distribution_images[0])):
                image = self.distribution_images[x][y]
                weights = [dist[ (x,y) ] for dist in distributions]

                if sum(weights) != 0:
                    return 0
                # Fog of war
                color = [0.0,0.0,0.0]
                colors = GHOST_VEC_COLORS[1:] # With Pacman
                if self.capture: colors = GHOST_VEC_COLORS
                for weight, gcolor in zip(weights, colors):
                    color = [min(1.0, c + 0.95 * g * weight ** .3) for c,g in zip(color, gcolor)]
                changeColor(image, formatColor(*color))
        refresh()

class FirstPersonPacmanGraphics(PacmanGraphics):
    def __init__(self, zoom = 1.0, show_ghots = True, capture = False, frame_time=0):
        PacmanGraphics.__init__(self, zoom, frame_time=frame_time)
        self.show_ghots = show_ghots
        self.capture = capture

    def initialize_graphics(self, state, is_blue = False):

        self.is_blue = is_blue
        PacmanGraphics.start_graphics(self, state)
        self.layout = state.layout

        # Draw the rest
        self.distribution_images = None  # initialize lazily
        self.draw_static_objects(state)
        self.draw_agent_objects(state)

        # Information
        self.previous_state = state

    def lookAhead(self, config, state):
        if config.get_direction() == 'Stop':
            return
        # Draw relevant ghosts
        all_ghosts = state.getGhostStates()
        visible_ghosts = state.getVisibleGhosts()
        for i, ghost in enumerate(all_ghosts):
            if ghost in visible_ghosts:
                self.draw_ghost(ghost, i)
            else:
                self.current_ghost_images[i] = None

    def get_ghost_color(self, ghost, ghost_index):
        return GHOST_COLORS[ghost_index]

    def get_position(self, ghost_state):
        if not self.show_ghots and not ghost_state.isPacman and ghost_state.get_position()[1] > 1:
            return (-1000, -1000)
        else:
            return PacmanGraphics.get_position(self, ghost_state)

def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


# Saving graphical output
# -----------------------
# Note: to make an animated gif from this postscript output, try the command:
# convert -delay 7 -loop 1 -compress lzw -layers optimize frame* out.gif
# convert is part of imagemagick (freeware)

SAVE_POSTSCRIPT = True
POSTSCRIPT_OUTPUT_DIR = 'frames'
FRAME_NUMBER = 0
import os

def save_frame():
    "Saves the current graphical output as a postscript file"
    global SAVE_POSTSCRIPT, FRAME_NUMBER, POSTSCRIPT_OUTPUT_DIR
    if not SAVE_POSTSCRIPT: return
    if not os.path.exists(POSTSCRIPT_OUTPUT_DIR): os.mkdir(POSTSCRIPT_OUTPUT_DIR)
    name = os.path.join(POSTSCRIPT_OUTPUT_DIR, 'frame_%08d.ps' % FRAME_NUMBER)
    FRAME_NUMBER += 1
    writePostscript(name) # writes the current canvas
