#!/usr/bin/env python3



# === STRUCTURE #1
# These are the modules (libraries) we will use in this code
# We are giving these modules shorter, but distinct, names for convenience

import logging
from random import randint

from termcolor import colored

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from gdpc import minecraft_tools as mt
from gdpc import editor_tools as et
from glm import ivec3


# Here, we set up Python's logging system.
# GDPC sometimes logs some errors that it cannot otherwise handle.
logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))


# === STRUCTURE #2
# These variables are global and can be read from anywhere in the code.
# NOTE: If you want to change a global value inside one of your functions,
#       you'll have to add a line of code. For an example, search 'GLOBAL'.

# Here we construct an Editor object
ED = Editor(buffering=True)


# === STRUCTURE #3

def build_farmhouse_wall(bottom_left: ivec3 = ivec3(0,0,0)):
    # Build a wall fragment in z direction
    # on the bottom left block 1x3x6
    geo.placeCuboidHollow(ED, bottom_left + ivec3(0,0,1), bottom_left + ivec3(0, 2, 5), Block("cobblestone"))
    geo.placeLine(ED, bottom_left + ivec3(0, 1, 2), bottom_left + ivec3(0,1,4), Block("glass_pane"))
    geo.placeLine(ED, bottom_left, bottom_left + (0, 2, 0), Block("oak_log"))

    # add floor
    geo.placeCuboid(ED, bottom_left + ivec3(0, -1, 0), bottom_left + ivec3(5, -1, 5), Block("oak_planks"))


    return ivec3(1,3,6)

def build_farmhouse_wall_double_pillar(bottom_left: ivec3 = ivec3(0,0,0)):
    # Build a wall fragment in z direction
    # on the bottom left block 1x3x6
    geo.placeCuboidHollow(ED, bottom_left + ivec3(0,0,1), bottom_left + ivec3(0, 2, 4), Block("cobblestone"))
    geo.placeLine(ED, bottom_left + ivec3(0, 1, 2), bottom_left + ivec3(0,1,3), Block("glass_pane"))
    geo.placeLine(ED, bottom_left, bottom_left + (0, 2, 0), Block("oak_log"))
    geo.placeLine(ED, bottom_left + (0,0,5), bottom_left + (0, 2, 5), Block("oak_log"))

    # add floor
    geo.placeCuboid(ED, bottom_left + ivec3(0, -1, 0), bottom_left + ivec3(5, -1, 5), Block("oak_planks"))


    return ivec3(1,3,6)


def build_farmhouse_corner(bottom_left: ivec3 = ivec3(0,0,0)):
    # Build a wall corner fragment in z direction
    # on the bottom left block 1x3x6
    geo.placeCuboidHollow(ED, bottom_left + ivec3(0,0,1), bottom_left + ivec3(0, 2, 5), Block("cobblestone"))
    geo.placeLine(ED, bottom_left + ivec3(0, 1, 2), bottom_left + ivec3(0,1,4), Block("glass_pane"))
    geo.placeLine(ED, bottom_left, bottom_left + (0, 2, 0), Block("oak_log"))
    geo.placeCuboidHollow(ED, bottom_left + ivec3(1,0,0), bottom_left + ivec3(5, 2, 0), Block("cobblestone"))
    geo.placeLine(ED, bottom_left + ivec3(2, 1, 0), bottom_left + ivec3(4,1,0), Block("glass_pane"))


    # add floor
    geo.placeCuboid(ED, bottom_left + ivec3(0, -1, 0), bottom_left + ivec3(5, -1, 5), Block("oak_planks"))


    return ivec3(1,3,6)

def build_farmhouse_wall_door(bottom_left: ivec3 = ivec3(0,0,0)):
    # Build a wall fragment in z direction with a door in the center
    # on the bottom left block 1x3x7

    # add floor
    geo.placeCuboid(ED, bottom_left + ivec3(0, -1, 0), bottom_left + ivec3(5, -1, 5), Block("oak_planks"))
    
    geo.placeCuboid(ED, bottom_left + ivec3(0,0,0), bottom_left + ivec3(0, 2, 1), Block("oak_log"))
    geo.placeCuboid(ED, bottom_left + ivec3(0, 0, 2), bottom_left + ivec3(0,2,2), Block("glass"))
    geo.placeCuboid(ED, bottom_left + ivec3(0, 0, 3), bottom_left + ivec3(0,2,3), Block("air"))
    ED.flushBuffer()
    ED.placeBlock(bottom_left + ivec3(0,0,3), Block("oak_door", {"facing": "east"}))
    ED.placeBlock(bottom_left + ivec3(0,2,3), Block("glass"))
    geo.placeCuboid(ED, bottom_left + ivec3(0, 0, 4), bottom_left + ivec3(0,2,4), Block("glass"))
    geo.placeCuboid(ED, bottom_left + ivec3(0,0,5), bottom_left + ivec3(0, 2, 5), Block("oak_log"))
    # geo.placeCuboid(ED, bottom_left + ivec3(0,0,5), bottom_left + ivec3(0, 2, 6), Block("oak_log"))

    

    return ivec3(1,3,7)

def main():
    try:
        print("Building prefab showcase")
        prefabs = [build_farmhouse_wall, build_farmhouse_wall_double_pillar, build_farmhouse_corner, build_farmhouse_wall_door]
        with ED.pushTransform(Transform(translation=ivec3(-80,0,120))):
            # clear area
            geo.placeCuboid(ED, ivec3(0,-1,0), ivec3(10,2,0) + len(prefabs)*ivec3(0,0,10), Block("air"))
            ED.flushBuffer()

            # all are 6x6 prefabs
            for i, prefab in enumerate(prefabs):
                with ED.pushTransform(Transform(translation=i*ivec3(0,0,10))):
                    prefab()
            ED.flushBuffer()



        print("Building house")
        ED.transform @= Transform(translation=ivec3(-120,0,150))

        SIDE_LENGHT = 3
        for i in range(SIDE_LENGHT):
            with ED.pushTransform(Transform(translation=i*ivec3(0,0,6))):
                build_farmhouse_wall()

        with ED.pushTransform():
            for n in range(3):
                ED.transform @= Transform(translation=(SIDE_LENGHT)*ivec3(0,0,6), rotation=3)
                for i in range(SIDE_LENGHT):
                    with ED.pushTransform(Transform(translation=i*ivec3(0,0,6))):
                        build_farmhouse_wall()

        with ED.pushTransform(Transform(translation=(SIDE_LENGHT//2)*ivec3(0,0,6))):
            build_farmhouse_wall_door()
        

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


# === STRUCTURE #4
# The code in here will only run if we run the file directly (not imported).
# This prevents people from accidentally running your generator.
# It is recommended to directly call a function here, because any variables
# you declare outside a function will be global.
if __name__ == '__main__':
    main()
