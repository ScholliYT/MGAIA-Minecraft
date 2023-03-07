#!/usr/bin/env python3



# === STRUCTURE #1
# These are the modules (libraries) we will use in this code
# We are giving these modules shorter, but distinct, names for convenience

import logging
import pickle
from random import randint
from typing import List, Tuple

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
        ED.transform @= Transform(translation=ivec3(-190, -1, 180))

        entrance_structure = load_structure("brickhouse-entrance")
        middle_structure = load_structure("brickhouse-middle")
        balcony_structure = load_structure("brickhouse-balcony")
        corner_structure = load_structure("brickhouse-corner")

        
        # same for all strucures
        strucutre_size = entrance_structure.size


        # building: List[List[Tuple[Structure, int]]] = [
        #     [(entrance_structure, 1), (entrance_structure, 2)],
        #     [(middle_structure, 0), (middle_structure, 2)],
        #     [(middle_structure, 0), (middle_structure, 2)],
        #     [(entrance_structure, 0), (entrance_structure, 3)],
        # ]

        building: List[List[Tuple[Structure, int]]] = [
            [(entrance_structure, 1), (middle_structure, 1), (entrance_structure, 2)],
            [(entrance_structure, 0), (middle_structure, 3), (entrance_structure, 3)],
        ]

        # building: List[List[Tuple[Structure, int]]] = [
        #     [(entrance_structure, 1), (middle_structure, 1), (balcony_structure, 2)],
        #     [(entrance_structure, 0), (middle_structure, 3), (corner_structure, 3)],
        # ]


        for row_idx, building_row in enumerate(reversed(building)):
            with ED.pushTransform(Transform(translation=ivec3(row_idx*strucutre_size.x, 0, 0))):
                for col_idx, (strucutre, rotation) in enumerate(building_row):
                    with ED.pushTransform(Transform(translation=ivec3(0, 0, col_idx*strucutre_size.z))):

                        # adjust for rotation respecing bottom left corner aligned coordinate system of structure
                        if rotation == 0:
                            translation_vec = ivec3(0, 0, 0)
                        elif rotation == 1:
                            translation_vec = ivec3(strucutre.size.x - 1, 0, 0)
                        elif rotation == 2:
                            translation_vec = ivec3(strucutre.size.x - 1, 0, strucutre.size.z -1)
                        elif rotation == 3:
                            translation_vec = ivec3(0, 0, strucutre.size.z -1)

                        
                        with ED.pushTransform(Transform(translation=translation_vec)):
                            with ED.pushTransform(Transform(rotation=rotation)):
                                for vec, block in strucutre.blocks.items():
                                    ED.placeBlock(vec, block)
        ED.flushBuffer()
        

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
