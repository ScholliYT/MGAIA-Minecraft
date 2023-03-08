import pickle
from typing import Dict, Tuple
from glm import ivec3
from gdpc import Block
from gdpc import Editor, Transform


from dataclasses import dataclass


@dataclass
class Structure:
    name: str
    offset: ivec3
    size: ivec3
    blocks: Dict[Tuple[int, int, int], Block]



def load_structure(structure_name: str, structures_directory: str = "structures") -> Structure:
    filename = structures_directory + "/" + structure_name + ".pkl"
    print("Loading strucutre data from disk", filename)
    with open(filename, "rb") as f:
        structure = pickle.load(f)

    if not isinstance(structure, Structure):
        raise Exception("Unexpected data loaded from file " + filename)

    return structure



def build_structure(editor: Editor, structure: Structure, rotation: int) -> None:
    # adjust for rotation respecing bottom left corner aligned coordinate system of structure
    if rotation == 0:
        translation_vec = ivec3(0, 0, 0)
    elif rotation == 1:
        translation_vec = ivec3(structure.size.x - 1, 0, 0)
    elif rotation == 2:
        translation_vec = ivec3(structure.size.x - 1, 0, structure.size.z -1)
    elif rotation == 3:
        translation_vec = ivec3(0, 0, structure.size.z -1)

    
    with editor.pushTransform(Transform(translation=translation_vec)):
        with editor.pushTransform(Transform(rotation=rotation)):
            for vec, block in structure.blocks.items():
                editor.placeBlock(vec, block)