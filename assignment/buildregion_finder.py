"""
Find a area that is good to build a house in a given range.


Define the search space through buildarea in XZ plane
/setbuildarea ~ ~ ~ ~100 ~ ~100
"""

import heapq
import random
import sys

from gdpc import Block, Editor, __url__
from gdpc import geometry as geo
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import Rect, addY, setY
from glm import ivec2, ivec3

from assignment.utils.buildregion import score_all_possible_buildregions


def buildPerimeter(editor, outer_rect: Rect, heights):
    """Build a wall around the build area border.

    In this function we're building a simple wall around the build area
        pillar-by-pillar, which means we can adjust to the terrain height
    """
    # HEIGHTMAP
    # Heightmaps are an easy way to get the uppermost block at any coordinate
    # There are four types available in a world slice:
    # - 'WORLD_SURFACE': The top non-air blocks
    # - 'MOTION_BLOCKING': The top blocks with a hitbox or fluid
    # - 'MOTION_BLOCKING_NO_LEAVES': Like MOTION_BLOCKING but ignoring leaves
    # - 'OCEAN_FLOOR': The top solid blocks

    
    STARTX, STARTZ = outer_rect.begin
    LASTX, LASTZ = outer_rect.last

    print("Building east-west walls...")

    for x in range(STARTX, LASTX + 1):
        # The northern wall
        y = heights[(x - STARTX, 0)]
        geo.placeCuboid(editor, (x, y - 2, STARTZ), (x, y, STARTZ), Block("granite"))
        geo.placeCuboid(editor, (x, y + 1, STARTZ), (x, y + 4, STARTZ), Block("granite_wall"))
        # The southern wall
        y = heights[(x - STARTX, LASTZ - STARTZ)]
        geo.placeCuboid(editor, (x, y - 2, LASTZ), (x, y, LASTZ), Block("red_sandstone"))
        geo.placeCuboid(editor, (x, y + 1, LASTZ), (x, y + 4, LASTZ), Block("red_sandstone_wall"))

    print("Building north-south walls...")

    for z in range(STARTZ, LASTZ + 1):
        # The western wall
        y = heights[(0, z - STARTZ)]
        geo.placeCuboid(editor, (STARTX, y - 2, z), (STARTX, y, z), Block("sandstone"))
        geo.placeCuboid(editor, (STARTX, y + 1, z), (STARTX, y + 4, z), Block("sandstone_wall"))
        # The eastern wall
        y = heights[(LASTX - STARTX, z - STARTZ)]
        geo.placeCuboid(editor, (LASTX, y - 2, z), (LASTX, y, z), Block("prismarine"))
        geo.placeCuboid(editor, (LASTX, y + 1, z), (LASTX, y + 4, z), Block("prismarine_wall"))


def get_build_area(editor):
    # Get the build area.
    try:
        buildArea = editor.getBuildArea()
    except BuildAreaNotSetError:
        print(
            "Error: failed to get the build area!\n"
            "Make sure to set the build area with the /setbuildarea command in-game.\n"
            "For example: /setbuildarea ~0 ~ ~0 ~100 ~ ~100"
        )
        sys.exit(1)

    return buildArea


def get_heights(editor, buildArea):

    print("BuildArea bottom left corner", buildArea.offset)
    print("BuildArea size", buildArea.size)


    print("Loading world slice...")
    buildRect = buildArea.toRect()
    worldSlice = editor.loadWorldSlice(buildRect, cache=True)
    print("World slice loaded!")


    # There are four types available in a world slice:
    # - 'WORLD_SURFACE': The top non-air blocks
    # - 'MOTION_BLOCKING': The top blocks with a hitbox or fluid
    # - 'MOTION_BLOCKING_NO_LEAVES': Like MOTION_BLOCKING but ignoring leaves
    # - 'OCEAN_FLOOR': The top solid blocks
    heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    return heights


def select_solution(solutions):
    # normalize terraform distance by build area
    # solution = min(solutions, key=lambda r: float(r[3])/(r[1][0]*r[1][1]))
    if not isinstance(solutions, list):
        solutions = list(solutions)

    solution_pool = []
    for size in set(map(lambda s: s[1], solutions)):
        solutions_with_size = filter(lambda s: s[1] == size, solutions)
        best_solutions_in_size = heapq.nsmallest(2, solutions_with_size, key=lambda s: s[3])
        solution_pool += best_solutions_in_size
    solution = random.choice(solution_pool)
    return solution


if __name__ == '__main__':

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
    
    buildArea = get_build_area(editor)
    heights = get_heights(editor, buildArea)

    print("Building outer wall around BuildArea")
    buildPerimeter(editor, buildArea.toRect(), heights)

    buffer=2
    solutions = score_all_possible_buildregions(heights, square_sidelenght=11, min_adjecent_squares=2, max_adjecent_squares=5, buffer=buffer)
    best_solution = select_solution(solutions)

    first = setY(buildArea.offset,0) + addY(ivec2(*best_solution[0]), best_solution[2])
    last = first + addY(ivec2(*best_solution[1]), 0)
    print("Best position to build [", first.to_tuple(), last.to_tuple(), "] of size", best_solution[1] , "requires terraforming of", best_solution[3], "blocks")
    geo.placeCuboid(editor, first, last, Block("red_wool"))

    buffer_vec = ivec3(buffer, 0, buffer)
    geo.placeCuboid(editor, first + buffer_vec, last - buffer_vec, Block("white_wool") )
