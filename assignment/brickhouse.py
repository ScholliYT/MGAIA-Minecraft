from typing import List, Tuple


from gdpc import Editor, Transform
from glm import ivec3

from assignment.utils.structure import Structure, load_structure, build_structure


# === STRUCTURE



def build_brickhouse(editor: Editor):
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
        with editor.pushTransform(Transform(translation=ivec3(row_idx*strucutre_size.x, 0, 0))):
            for col_idx, (structure, rotation) in enumerate(building_row):
                with editor.pushTransform(Transform(translation=ivec3(0, 0, col_idx*strucutre_size.z))):
                    build_structure(editor, structure, rotation)
                    
    editor.flushBuffer()


def main():
    ED = Editor(buffering=True)

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


        ED.transform @= Transform(translation=ivec3(-210, -1, 250))

        print("Building house")
        build_brickhouse(editor=ED)

        
        

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
