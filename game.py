"""
Final interface for the game, calls all the modules.
"""

import time
import osmanager
from frame import Frame
from player import Player
from background import Background
from firebeam import FireBeam
from boss import Boss

FRAME_RATE = 16

# Create the Objects and put them in an array

FRAME = Frame()
PLAYER = Player()
BACKGROUND = Background()
TIMESTEP = 0

# The parts of the game
OBJECTS = [BACKGROUND, PLAYER]
ENDGAME_TIME = 10

while True:
    # Get the input to all the objects
    if time.time() > FRAME.previous_render_time + 1 / (2 * FRAME_RATE):
        FRAME.broadcast_input(OBJECTS)
    if time.time() > FRAME.previous_render_time + 1 / FRAME_RATE:
        # Update and Render
        TIMESTEP += 1
        FRAME.broadcast_timestep(OBJECTS)
        FRAME.broadcast_render(OBJECTS)
        osmanager.clrscr()
        FRAME.render()
        # Initialize the new FireBeams and Collision Detect
        if TIMESTEP < ENDGAME_TIME:
            NEW_FIREBEAM = FireBeam.spawn((FRAME.rows, FRAME.cols))
            if NEW_FIREBEAM is not False:
                OBJECTS.append(NEW_FIREBEAM)
        if TIMESTEP > PLAYER.last_died + 4:
            for obj in OBJECTS:
                if isinstance(obj, FireBeam) and obj.detect_collision(PLAYER):
                    FRAME.player_die()
                    PLAYER.last_died = TIMESTEP
        # Initialize the Boss Enemy
        if TIMESTEP == ENDGAME_TIME + 5:
            BOSS = Boss((FRAME.rows, FRAME.cols), PLAYER)
            OBJECTS.append(BOSS)
