"""
Build a building block sturucte
"""

import pickle
import sys

from gdpc import Editor, Transform, __url__
from gdpc.exceptions import InterfaceConnectionError
from glm import ivec3

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


structure_name = "brickhouse-roofhouse-middle-to-flat"
filename = "structures/" + structure_name + ".pkl"
print("Loading strucutre data from disk", filename)
with open(filename, "rb") as f:
    structure = pickle.load(f)

if not isinstance(structure, Structure):
    raise Exception("Unexpected data loaded from file " + filename)


destination_pos = ivec3(-70, 10, 223)
print("Replicating building")
with editor.pushTransform(Transform(translation=destination_pos, rotation=0)):
    for vec, block in structure.blocks.items():
        # vec = (-vec[0], vec[1], vec[2]) # mirror at axis
        editor.placeBlock(vec, block)
editor.flushBuffer()



