"""
Load a building block sturucte

stand at the bottom left corner of the builing block and look towards it
Building is expected to be 11x16x11
/setbuildarea ~2 ~ ~ ~11 ~16 ~10
"""

from dataclasses import dataclass
import pickle
import sys
from typing import Dict, List, Tuple
from glm import ivec3

import numpy as np

from gdpc import __url__, Editor, Block, Transform
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY

from assignment.utils.structure import Structure


# Create an editor object.
# The Editor class provides a high-level interface to interact with the Minecraft world.
editor = Editor(buffering=True)


# Check if the editor can connect to the GDMC HTTP interface.
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


structure_name = "brickhouse-middle"
filename = "structures/" + structure_name + ".pkl"
print("Loading strucutre data from disk", filename)
with open(filename, "rb") as f:
    structure = pickle.load(f)

if not isinstance(structure, Structure):
    raise Exception("Unexpected data loaded from file " + filename)


destination_pos = ivec3(-60, 0, 100)
print("Replicating building")
with editor.pushTransform(Transform(translation=destination_pos)):
    for vec, block in structure.blocks.items():
        editor.placeBlock(vec, block)
editor.flushBuffer()



