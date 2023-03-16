import heapq
import math
import random

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from gdpc.vector_tools import addY, setY
from glm import ivec2, ivec3

from assignment.brickhouse import build_brickhouse, random_building, wfc_state_to_minecraft_blocks
from assignment.buildregion_finder import get_build_area, get_heights, select_solutioin
from assignment.utils.buildregion import score_all_possible_buildregions
from assignment.utils.wave_function_collaplse_util import (
    print_state,
)


def main():
    ED = Editor(buffering=True)

    try:

        buildArea = get_build_area(ED)
        heights = get_heights(ED, buildArea)

        buffer=2
        square_sidelenght = 11
        min_adjecent_structures=3
        max_adjecent_structures=6
        solutions = list(score_all_possible_buildregions(heights, 
                                                         square_sidelenght=square_sidelenght, 
                                                         min_adjecent_squares=min_adjecent_structures, 
                                                         max_adjecent_squares=max_adjecent_structures, 
                                                         buffer=buffer))
        solution = select_solutioin(solutions)       
        region_origin, region_size, region_y, distance = solution

        first = setY(buildArea.offset,0) + addY(ivec2(*region_origin), region_y)
        last = first + addY(ivec2(*region_size), 0) - ivec3(1,0,1)
        print("Best position to build [", first.to_tuple(), last.to_tuple(), "] of size", 
              region_size, "requires terraforming of", distance, "blocks")
        
        # geo.placeCuboid(ED, first, last, Block("red_wool"))
        buffer_vec = ivec3(buffer, 0, buffer)
        # geo.placeCuboid(ED, first + buffer_vec, last - buffer_vec, Block("white_wool") )
        ED.flushBuffer()

        building_size = (2+(region_size[0]-2*buffer)//11, 2, 2+(region_size[1]-2*buffer)//11)
        print("Computing house of size", building_size)
        wfc = random_building(building_size)
        print_state(wfc)
        state_without_air = [[[s for s in ys[1:-1]] for ys in xs] for xs in wfc.collapsed_state()[1:-1]]
        building = wfc_state_to_minecraft_blocks(state_without_air)

        print("Building house")
        ED.transform @= Transform(translation=first + buffer_vec + ivec3(0, -1, 0))
        # remove outer layer of air blocks
        build_brickhouse(editor=ED, building=building, place_air=False)

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")

if __name__ == '__main__':
    main()
