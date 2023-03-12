import logging
from dataclasses import dataclass, field, replace
from typing import Dict, List

from assignment.utils.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_inner_corner_m2m,
    brickhouse_middle,
    brickhouse_roofhouse_center,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_inner_corner_m2m,
    brickhouse_roofhouse_middle,
    brickhouse_roofhouse_middle_to_flat,
    brickhouse_roofhouse_middle_to_flat_mirrored_x,
    brickhouse_small_window_flat_roof,
    empty_space_air,
)

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class StructureRotation:
    structure_name: str
    rotation: int

    def rotate(self, amount: int):
        return replace(self, rotation=(self.rotation + amount) % 4)
        

@dataclass(frozen=True)
class StructureAdjacency:
    """Store all possible other Structures that can be placed next to this structure

    Assumes that this structure is rotated by 0
    """
    structure_name: str

    # store a list of structures that can be adjacent in the specified rotation and placed above this   
    # (strucutre_name, rotation)
    y_plus: List[StructureRotation] = field(default_factory=list)
    y_minus: List[StructureRotation] = field(default_factory=list)

    x_plus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))
    x_minus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))

    z_plus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))
    z_minus: List[StructureRotation] = field(default_factory=lambda: all_rotations(empty_space_air))


    def adjecent_structrues(self, axis:str, self_rotation: int) -> List[StructureRotation]:
        
        if axis not in ("y_plus","y_minus","x_plus","x_minus","z_plus","z_minus"):
            raise ValueError("Invalid axis " + axis)

        # easy cases since everything will rotate along the y-axis
        match axis:
            case "y_plus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_plus))
            case "y_minus":
                return list(map(lambda r: r.rotate(self_rotation), self.y_minus))


        if self_rotation == 0:
            # default case with no rotations
            return getattr(self, axis)
        elif self_rotation in (1,2,3):
            rotation_axes = (self.x_plus,self.z_plus,self.x_minus,self.z_minus)
            match axis:
                case "x_plus":
                    return list(map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 0])) # self.z_minus for rotation 1
                case "z_plus":
                    return list(map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 1])) # self.x_plus for rotation 1
                case "x_minus":
                    return list(map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 2])) # self.z_plus for rotation 1
                case "z_minus":
                    return list(map(lambda r: r.rotate(self_rotation), rotation_axes[-self_rotation + 3])) # self.x_minus for rotation 1
            raise NotImplementedError(f"Axis {axis} should have been handled before")
        else: 
            raise ValueError("Rotation must be 0,1,2 or 3")




def all_rotations(structure: str):
    return [StructureRotation(structure, r) for r in range(4)]

structure_adjecencies = {
    empty_space_air: StructureAdjacency(
        structure_name=empty_space_air,
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 1).rotate(3), # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 1).rotate(2), # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_balcony, 1).rotate(3), # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 1).rotate(2), # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 1).rotate(3), # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 1).rotate(2), # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 1).rotate(3), # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 1).rotate(2), # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 1).rotate(3), # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 1).rotate(2), # from brickhouse_small_window_flat_roof.z_minus            
            StructureRotation(brickhouse_big_window_flat_roof, 1).rotate(3), # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 1).rotate(2), # from brickhouse_big_window_flat_roof.z_minus            
            StructureRotation(brickhouse_middle, 1).rotate(2), # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 1).rotate(2), # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0), # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 2), # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 3).rotate(3), # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 3).rotate(2), # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_balcony, 3).rotate(3), # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 3).rotate(2), # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 3).rotate(3), # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 3).rotate(2), # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 3).rotate(3), # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 3).rotate(2), # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 3).rotate(3), # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 3).rotate(2), # from brickhouse_small_window_flat_roof.z_minus            
            StructureRotation(brickhouse_big_window_flat_roof, 3).rotate(3), # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 3).rotate(2), # from brickhouse_big_window_flat_roof.z_minus            
            StructureRotation(brickhouse_middle, 3).rotate(2), # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 3).rotate(2), # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 2), # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 0), # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 2).rotate(3), # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 2).rotate(2), # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_balcony, 2).rotate(3), # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 2).rotate(2), # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 2).rotate(3), # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 2).rotate(2), # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 2).rotate(3), # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 2).rotate(2), # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 2).rotate(3), # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 2).rotate(2), # from brickhouse_small_window_flat_roof.z_minus            
            StructureRotation(brickhouse_big_window_flat_roof, 2).rotate(3), # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 2).rotate(2), # from brickhouse_big_window_flat_roof.z_minus            
            StructureRotation(brickhouse_middle, 2).rotate(2), # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 2).rotate(2), # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1), # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3), # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(brickhouse_entrance, 0).rotate(3), # from brickhouse_entrance.x_minus
            StructureRotation(brickhouse_entrance, 0).rotate(2), # from brickhouse_entrance.z_minus
            StructureRotation(brickhouse_balcony, 0).rotate(3), # from brickhouse_balcony.x_minus
            StructureRotation(brickhouse_balcony, 0).rotate(2), # from brickhouse_balcony.z_minus
            StructureRotation(brickhouse_corner, 0).rotate(3), # from brickhouse_corner.x_minus
            StructureRotation(brickhouse_corner, 0).rotate(2), # from brickhouse_corner.z_minus
            StructureRotation(brickhouse_roofhouse_corner, 0).rotate(3), # from brickhouse_roofhouse_corner.x_minus
            StructureRotation(brickhouse_roofhouse_corner, 0).rotate(2), # from brickhouse_roofhouse_corner.z_minus
            StructureRotation(brickhouse_small_window_flat_roof, 0).rotate(3), # from brickhouse_small_window_flat_roof.x_minus
            StructureRotation(brickhouse_small_window_flat_roof, 0).rotate(2), # from brickhouse_small_window_flat_roof.z_minus            
            StructureRotation(brickhouse_big_window_flat_roof, 0).rotate(3), # from brickhouse_big_window_flat_roof.x_minus
            StructureRotation(brickhouse_big_window_flat_roof, 0).rotate(2), # from brickhouse_big_window_flat_roof.z_minus            
            StructureRotation(brickhouse_middle, 0).rotate(2), # from brickhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle, 0).rotate(2), # from brickhouse_roofhouse_middle.z_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 3), # from brickhouse_roofhouse_middle_to_flat.x_minus
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 1), # from brickhouse_roofhouse_middle_to_flat_mirrored_x.x_plus
        ],
        y_plus=[
            *all_rotations(empty_space_air)
        ],
        y_minus=[
            *all_rotations(empty_space_air)
        ]
    ),
    brickhouse_entrance: StructureAdjacency(
        structure_name=brickhouse_entrance,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 0),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ]
    ), 
    brickhouse_balcony: StructureAdjacency(
        structure_name=brickhouse_balcony,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 0),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ]
    ), 
    brickhouse_corner: StructureAdjacency(
        structure_name=brickhouse_corner,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_balcony, 3),
            StructureRotation(brickhouse_corner, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 0),
        ]
    ), 
    brickhouse_middle: StructureAdjacency(
        structure_name=brickhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
            StructureRotation(brickhouse_balcony, 1),
            StructureRotation(brickhouse_corner, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
        ],
        x_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_balcony, 0),
            StructureRotation(brickhouse_corner, 0),
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
            *all_rotations(brickhouse_center),
            *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ]
    ),
    brickhouse_center: StructureAdjacency(
        structure_name=brickhouse_center,
        x_plus=[
            *all_rotations(brickhouse_center),
            # *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
        ],
        x_minus=[
            *all_rotations(brickhouse_center),
            # *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 3),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
        ],
        z_plus=[
            *all_rotations(brickhouse_center),
            # *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 2),
            StructureRotation(brickhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 3),
        ],
        z_minus=[
            *all_rotations(brickhouse_center),
            # *all_rotations(brickhouse_courtyard),
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_inner_corner_m2m, 2),
            StructureRotation(brickhouse_inner_corner_m2m, 1),
        ],
        y_plus=[
            *all_rotations(brickhouse_roofhouse_center)
        ]
    ),
    brickhouse_courtyard: StructureAdjacency(
        structure_name=brickhouse_courtyard,
        x_plus=[
            StructureRotation(brickhouse_middle, 1),
            # *all_rotations(brickhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_middle, 3),
            # *all_rotations(brickhouse_center),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
            # *all_rotations(brickhouse_center),
        ],
        z_minus=[
            StructureRotation(brickhouse_middle, 0),
            # *all_rotations(brickhouse_center),
        ],
        y_plus=[
            *all_rotations(brickhouse_roofhouse_courtyard)
        ]
    ),
    brickhouse_inner_corner_m2m: StructureAdjacency(
        structure_name=brickhouse_inner_corner_m2m,
        x_plus=[
            StructureRotation(brickhouse_middle, 1),
            *all_rotations(brickhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_middle, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_middle, 0),
            *all_rotations(brickhouse_center),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
        ]
    ), 
    brickhouse_roofhouse_corner: StructureAdjacency(
        structure_name=brickhouse_roofhouse_corner,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 3),
            StructureRotation(brickhouse_roofhouse_middle, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_balcony, 0),
        ]
    ),
    brickhouse_roofhouse_inner_corner_m2m: StructureAdjacency(
        structure_name=brickhouse_roofhouse_inner_corner_m2m,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        y_minus=[
            StructureRotation(brickhouse_inner_corner_m2m, 0),
        ]
    ),
    brickhouse_small_window_flat_roof: StructureAdjacency(
        structure_name=brickhouse_small_window_flat_roof,
        x_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 1),
            StructureRotation(brickhouse_small_window_flat_roof, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 3),
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 2),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_balcony, 0),
        ]
    ),
    brickhouse_big_window_flat_roof: StructureAdjacency(
        structure_name=brickhouse_big_window_flat_roof,
        x_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 1),
            StructureRotation(brickhouse_small_window_flat_roof, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_big_window_flat_roof, 3),
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 2),
        ],
        y_minus=[
            StructureRotation(brickhouse_corner, 0),
        ]
    ),
    brickhouse_roofhouse_middle: StructureAdjacency(
        structure_name=brickhouse_roofhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 3),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_corner, 0),
            StructureRotation(brickhouse_roofhouse_middle, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_courtyard),
            *all_rotations(brickhouse_roofhouse_center),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 0),
        ]
    ),
    brickhouse_roofhouse_courtyard: StructureAdjacency(
        structure_name=brickhouse_roofhouse_courtyard,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_center),
        ],
        y_minus=[
            *all_rotations(brickhouse_courtyard)
        ]
    ),
    brickhouse_roofhouse_center: StructureAdjacency(
        structure_name=brickhouse_roofhouse_center,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),            
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),                        
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),            
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),                        
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 0),            
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 3),                        
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
            *all_rotations(brickhouse_roofhouse_courtyard),
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 2),            
            StructureRotation(brickhouse_roofhouse_inner_corner_m2m, 1),                        
        ],
        y_minus=[
            *all_rotations(brickhouse_center)
        ]
    ),
    brickhouse_roofhouse_middle_to_flat: StructureAdjacency(
        structure_name=brickhouse_roofhouse_middle_to_flat,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_middle_to_flat_mirrored_x, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 3),
            StructureRotation(brickhouse_big_window_flat_roof, 3),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 3),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 3),                        
        ]
    ),
    brickhouse_roofhouse_middle_to_flat_mirrored_x: StructureAdjacency(
        structure_name=brickhouse_roofhouse_middle_to_flat_mirrored_x,
        x_minus=[
            StructureRotation(brickhouse_roofhouse_middle_to_flat, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_small_window_flat_roof, 2),
            StructureRotation(brickhouse_big_window_flat_roof, 2),
        ],
        z_minus=[
            StructureRotation(brickhouse_roofhouse_middle, 1),
            StructureRotation(brickhouse_roofhouse_corner, 1),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 1),
        ]
    ),
}



def check_symmetry(structure_adjecencies: Dict[str, StructureAdjacency]):
    """Verify that the symmetric coutnerpart for each rule is present

    Args:
        structure_adjecencies (Dict[str, StructureAdjacency]): structures and their adjecency rules

    Raises:
        Exception: if no rule was found
        Exception: if too many rules were found
    """
    self_rotation = 0
    for s_name in structure_adjecencies.keys():
        adj = structure_adjecencies[s_name]

        for axis in ("y_plus","y_minus","x_plus","x_minus","z_plus","z_minus"):
        # for axis in ("y_plus","y_minus"):
            rules: List[StructureRotation] = getattr(adj, axis)
            for rule in rules:
                if rule.structure_name not in structure_adjecencies:
                    raise KeyError(f"'{rule.structure_name}' not found in structure_adjecencies")
                
                other_adj = structure_adjecencies[rule.structure_name]
                opposite_axis = axis[:2] + ("plus" if axis[2:] == "minus" else "minus")

                other_rules: List[StructureRotation] = other_adj.adjecent_structrues(opposite_axis, rule.rotation)

                matching_rules = list(filter(lambda r: r.structure_name==s_name and r.rotation == self_rotation, other_rules))

                if len(matching_rules) == 0:
                    logger.error("%s.%s: Symmetric rule for %s not found. Expected to find correctly rotated %s in axis %s of %s. Otherrules %s", s_name, axis, rule, s_name, opposite_axis, rule.structure_name, other_rules)
                    raise Exception("Expected rule not found")
                elif len(matching_rules) > 1:
                    logger.error("%s.%s: Multiple symmetric rules for %s found: %s", s_name, axis, rule, matching_rules)
                    raise Exception("Found too many rules")


if __name__ == '__main__':
    print(structure_adjecencies[brickhouse_entrance].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)
