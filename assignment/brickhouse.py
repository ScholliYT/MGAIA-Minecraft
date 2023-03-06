#!/usr/bin/env python3



# === STRUCTURE #1
# These are the modules (libraries) we will use in this code
# We are giving these modules shorter, but distinct, names for convenience

import logging
import pickle
from random import randint

from termcolor import colored

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from gdpc import minecraft_tools as mt
from gdpc import editor_tools as et
from glm import ivec3

from assignment.utils.structure import Structure, load_structure


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


def main():
    try:
        # print("Building prefab showcase")
        # prefabs = [build_entrance]
        # with ED.pushTransform(Transform(translation=ivec3(-60,0,180))):
        #     # clear area
        #     geo.placeCuboid(ED, ivec3(0,-1,0), ivec3(10,2,0) + len(prefabs)*ivec3(0,0,10), Block("air"))
        #     ED.flushBuffer()

        #     # all are 6x6 prefabs
        #     for i, prefab in enumerate(prefabs):
        #         with ED.pushTransform(Transform(translation=i*ivec3(0,0,10))):
        #             prefab()
        #     ED.flushBuffer()



        print("Building house")
        ED.transform @= Transform(translation=ivec3(-110, -1, -70))

        structure_name = "brickhouse-entrance"
        structure = load_structure(structure_name)


        print("Replicating building")
        
        with ED.pushTransform(Transform(rotation=0)):
            for vec, block in structure.blocks.items():
                ED.placeBlock(vec, block)
        ED.flushBuffer()

        with ED.pushTransform(Transform(translation=ivec3(2*structure.size.x-1, 0, 0))):
            with ED.pushTransform(Transform(rotation=1)):
                for vec, block in structure.blocks.items():
                    ED.placeBlock(vec, block)
        ED.flushBuffer()

        with ED.pushTransform(Transform(translation=ivec3(2*structure.size.x-1, 0, 2*structure.size.z-1))):
            with ED.pushTransform(Transform(rotation=2)):
                for vec, block in structure.blocks.items():
                    ED.placeBlock(vec, block)
        ED.flushBuffer()

        with ED.pushTransform(Transform(translation=ivec3(0, 0, 2*structure.size.z-1))):
            with ED.pushTransform(Transform(rotation=3)):
                for vec, block in structure.blocks.items():
                    ED.placeBlock(vec, block)
        ED.flushBuffer()

        # SIDE_LENGHT = 3
        # for i in range(SIDE_LENGHT):
        #     with ED.pushTransform(Transform(translation=i*ivec3(0,0,6))):
        #         build_farmhouse_wall()

        # with ED.pushTransform():
        #     for n in range(3):
        #         ED.transform @= Transform(translation=(SIDE_LENGHT)*ivec3(0,0,6), rotation=3)
        #         for i in range(SIDE_LENGHT):
        #             with ED.pushTransform(Transform(translation=i*ivec3(0,0,6))):
        #                 build_farmhouse_wall()

        # with ED.pushTransform(Transform(translation=(SIDE_LENGHT//2)*ivec3(0,0,6))):
        #     build_farmhouse_wall_door()
        

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
