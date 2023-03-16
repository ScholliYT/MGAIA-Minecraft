from typing import List

from assignment.utils.structure_adjacency import StructureRotation
from assignment.utils.structures import (
    empty_space_air,
)
from assignment.utils.wave_function_collapse import WaveFunctionCollapse


def print_state(wfc: WaveFunctionCollapse):
    for y in range(wfc.state_space_size[1]):
        print("Layer y="+str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            print(wfc.state_space[x][y])


def collapse_to_air_on_outer_rectangle(wfc: WaveFunctionCollapse):
    for x in range(wfc.state_space_size[0]):
        last = wfc.state_space_size[2]-1
        wfc.collapse_cell_to_state([x,0,0], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([x,0,last], StructureRotation(empty_space_air, 0))

    for z in range(wfc.state_space_size[2]):
        last = wfc.state_space_size[0]-1
        wfc.collapse_cell_to_state([0,0,z], StructureRotation(empty_space_air, 0))
        wfc.collapse_cell_to_state([last,0,z], StructureRotation(empty_space_air, 0))
