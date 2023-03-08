from typing import Dict, List, Tuple


from dataclasses import dataclass, field, replace

import logging

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

    x_plus: List[StructureRotation] = field(default_factory=list)
    x_minus: List[StructureRotation] = field(default_factory=list)

    z_plus: List[StructureRotation] = field(default_factory=list)
    z_minus: List[StructureRotation] = field(default_factory=list)


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



# ground floors
brickhouse_entrance = "brickhouse-entrance"
brickhouse_middle = "brickhouse-middle"
# brickhouse_balcony = "brickhouse-balcony"
# brickhouse_corner = "brickhouse-corner"
# brickhouse_center = "brickhouse-center"

# roofs
# brickhouse_small_window_flat_roof = "brickhouse-small-window-flat-roof"
# brickhouse_big_window_flat_roof = "brickhouse-big-window-flat-roof"
brickhouse_roofhouse_corner = "brickhouse-roofhouse-corner"
brickhouse_roofhouse_middle = "brickhouse-roofhouse-middle"




structure_adjecencies = {
    brickhouse_entrance: StructureAdjacency(
        structure_name=brickhouse_entrance,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
        ],
        z_plus=[
            StructureRotation(brickhouse_entrance, 3),
            StructureRotation(brickhouse_middle, 3),
        ],
        y_plus=[
            # StructureRotation(brickhouse_small_window_flat_roof, 0),
            StructureRotation(brickhouse_roofhouse_corner, 0),
        ]
    ), 
    brickhouse_middle: StructureAdjacency(
        structure_name=brickhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
            StructureRotation(brickhouse_entrance, 1),
        ],
        x_minus=[
            StructureRotation(brickhouse_entrance, 0),
            StructureRotation(brickhouse_middle, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
        ],
        y_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 0),
        ]
    ),
    brickhouse_roofhouse_corner: StructureAdjacency(
        structure_name=brickhouse_roofhouse_corner,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 3),
            StructureRotation(brickhouse_roofhouse_middle, 3),
        ],
        y_minus=[
            StructureRotation(brickhouse_entrance, 0),
        ]
    ),
    brickhouse_roofhouse_middle: StructureAdjacency(
        structure_name=brickhouse_roofhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_roofhouse_corner, 1),
            StructureRotation(brickhouse_roofhouse_middle, 0),
        ],
        x_minus=[
            StructureRotation(brickhouse_roofhouse_corner, 0),
            StructureRotation(brickhouse_roofhouse_middle, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_roofhouse_middle, 2),
        ],
        y_minus=[
            StructureRotation(brickhouse_middle, 0),
        ]
    )
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
                other_adj = structure_adjecencies[rule.structure_name]
                opposite_axis = axis[:2] + ("plus" if axis[2:] == "minus" else "minus")

                other_rules: List[StructureRotation] = other_adj.adjecent_structrues(opposite_axis, rule.rotation)

                matching_rules = list(filter(lambda r: r.structure_name==s_name and r.rotation == self_rotation, other_rules))

                if len(matching_rules) == 0:
                    logger.error("%s.%s: Symmetric rule for %s not found", s_name, axis, rule)
                    raise Exception("Expected rule not found")
                elif len(matching_rules) > 1:
                    logger.error("%s.%s: Multiple symmetric rules for %s found: %s", s_name, axis, rule, matching_rules)
                    raise Exception("Found too many rules")


if __name__ == '__main__':
    print(structure_adjecencies[brickhouse_entrance].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)




# # From self rotation = 1
# brickhouse_entrance: StructureAdjacency(
#     structure_name=brickhouse_entrance,
#     x_minus=[
#         StructureRotation(brickhouse_middle, 0),
#         StructureRotation(brickhouse_entrance, 0),
#     ],
#     z_plus=[
#         StructureRotation(brickhouse_entrance, 2),
#         StructureRotation(brickhouse_middle, 1),
#     ],
#     y_plus=[
#         # StructureRotation(brickhouse_small_window_flat_roof, 1),
#         StructureRotation(brickhouse_roofhouse_corner, 1),
#     ]
# )