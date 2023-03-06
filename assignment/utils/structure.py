import pickle
from typing import Dict, Tuple
from glm import ivec3
from gdpc import Block


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

