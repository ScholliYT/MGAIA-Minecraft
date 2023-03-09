from typing import List

from gdpc import Block, Editor, Transform
from gdpc import geometry as geo
from glm import ivec3

from assignment.utils.structure import Structure, build_structure, load_structure
from assignment.utils.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_middle,
    brickhouse_roofhouse_center,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_middle,
    brickhouse_small_window_flat_roof,
)


def build_strucutre_showcase(editor: Editor, structures: List[Structure], space_between_structures = 3):
    
    # same for all strucures
    strucutre_size = structures[0].size

    geo.placeCuboid(editor, 
                    ivec3(0,0,0), 
                    ivec3(4*(strucutre_size.x+2*space_between_structures), 16, len(structures)*(strucutre_size.z+space_between_structures)),
                    Block("air"))
    
    editor.flushBuffer()

    for rotation in range(4):
        with editor.pushTransform(Transform(translation=ivec3(rotation*(strucutre_size.x+2*space_between_structures), 0, 0))):
            for structure_idx, structure in enumerate(structures):
                with editor.pushTransform(Transform(translation=ivec3(0, 0, structure_idx*(strucutre_size.z+space_between_structures)))):
                    build_structure(editor, structure, rotation)
                    
    editor.flushBuffer()


def main():
    ED = Editor(buffering=True)

    try:
        ED.transform @= Transform(translation=ivec3(0, 0, 100))

        structures = [
            load_structure(brickhouse_entrance),
            load_structure(brickhouse_middle),
            load_structure(brickhouse_balcony),
            load_structure(brickhouse_corner),
            load_structure(brickhouse_courtyard),
            load_structure(brickhouse_roofhouse_corner),
            load_structure(brickhouse_roofhouse_middle),
            load_structure(brickhouse_roofhouse_courtyard),
            load_structure(brickhouse_center),
            load_structure(brickhouse_roofhouse_center),
            load_structure(brickhouse_small_window_flat_roof),
            load_structure(brickhouse_big_window_flat_roof),
        ]

        print("Building structure showcase")
        build_strucutre_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == '__main__':
    main()
