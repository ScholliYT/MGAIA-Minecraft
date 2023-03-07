"""
Load a building block sturucte

stand in front of the bottom left corner of the builing block and look towards it
Building is expected to be 11x16x11
/setbuildarea ~1 ~ ~ ~11 ~16 ~10
"""

import pickle
import sys


from gdpc import __url__, Editor
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError

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



print("Loading world slice...")
buildRect = buildArea.toRect()
worldSlice = editor.loadWorldSlice(buildRect, cache=True)
print("World slice loaded!")


print("Sturcutre bottom left corner", buildArea.offset)
print("Strucutre size", buildArea.size)
print("Structure blocks", buildArea.volume)

structure = Structure(name="brickhouse-big-window-flat-roof", offset=buildArea.offset, size=buildArea.size, blocks={})
print("Scanning structure", structure.name)
for block_global in buildArea.inner:
    vec = block_global - buildArea.offset
    structure.blocks[vec] = worldSlice.getBlockGlobal(block_global)

filename = "structures/" + structure.name + ".pkl"
print("Saving strucutre data to disk", filename)
with open(filename, "wb") as f:
    pickle.dump(structure, f)

