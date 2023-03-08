from typing import List, Tuple


from gdpc import geometry as geo
from gdpc import Editor, Transform, Block
from glm import ivec3

from assignment.utils.structure import Structure, load_structure, build_structure


# === STRUCTURE



def build_strucutre_showcase(editor: Editor, structures: List[Structure], space_between_structures = 3):
    
    # same for all strucures
    strucutre_size = structures[0].size

    geo.placeCuboid(editor, 
                    ivec3(0,0,0), 
                    ivec3(4*(strucutre_size.x+2*space_between_structures), 25, len(structures)*(strucutre_size.z+space_between_structures)),
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
            load_structure("brickhouse-entrance"),
            load_structure("brickhouse-middle"),
            load_structure("brickhouse-balcony"),
            load_structure("brickhouse-corner"),
            load_structure("brickhouse-center"),
            load_structure("brickhouse-small-window-flat-roof"),
            load_structure("brickhouse-big-window-flat-roof"),
            load_structure("brickhouse-roofhouse-corner"),
            load_structure("brickhouse-roofhouse-middle"),
        ]

        print("Building structure showcase")
        build_strucutre_showcase(editor=ED, structures=structures)

        print("Done!")

    except KeyboardInterrupt: # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")


if __name__ == '__main__':
    main()
