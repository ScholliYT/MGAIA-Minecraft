
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
from assignment.brickhouse import build_brickhouse

from assignment.utils.structure import Structure, load_structure

import pickle
import sys
from typing import Dict, List, Tuple
from glm import ivec2, ivec3

import numpy as np

from gdpc import __url__, Editor, Block, Transform
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY, setY, Rect
from gdpc import geometry as geo
from assignment.utils.buildregion import score_all_possible_buildregions



# Here, we set up Python's logging system.
# GDPC sometimes logs some errors that it cannot otherwise handle.
logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))



def main():
    editor = Editor(buffering=True)


    try:
        editor.checkConnection()
    except InterfaceConnectionError:
        print(
            f"Error: Could not connect to the GDMC HTTP interface at {editor.host}!\n"
            "To use GDPC, you need to use a \"backend\" that provides the GDMC HTTP interface.\n"
            "For example, by running Minecraft with the GDMC HTTP mod installed.\n"
            f"See {__url__}/README.md for more information."
        )
        sys.exit(1)


    # Get the build area.
    try:
        buildArea = editor.getBuildArea()
    except BuildAreaNotSetError:
        print(
            "Error: failed to get the build area!\n"
            "Make sure to set the build area with the /setbuildarea command in-game.\n"
            "For example: /setbuildarea ~0 0 ~0 ~64 200 ~64"
        )
        sys.exit(1)

    try:
        print("Loading world slice...")
        buildRect = buildArea.toRect()
        worldSlice = editor.loadWorldSlice(buildRect, cache=True)
        print("World slice loaded!")



        print("Finding optimal spot to build")

        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        buffer=2

        solutions = score_all_possible_buildregions(heights, square_sidelenght=11, min_adjecent_squares=2, max_adjecent_squares=5, buffer=buffer)
        best_solution = min(solutions, key=lambda r: r[3])

        first = setY(buildArea.offset,0) + addY(ivec2(*best_solution[0]), best_solution[2])
        last = first + addY(ivec2(*best_solution[1]), 0)
        area_size = best_solution[1]

        buffer_vec = ivec3(buffer, 0, buffer)
        first += buffer_vec
        last -= buffer_vec
        area_size = tuple(np.array(area_size) - 2*buffer)
        print("Best position to build [", first.to_tuple(), last.to_tuple(), "] of size", area_size, "requires terraforming of", best_solution[3], "blocks")

        print("Building house")
        with editor.pushTransform(Transform(translation=first)):
            build_brickhouse(editor=editor)

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")

if __name__ == '__main__':
    main()
