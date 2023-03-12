structure_adjecencies = {
    brickhouse_middle: StructureAdjacency(
        structure_name=brickhouse_middle,
        x_plus=[
            StructureRotation(brickhouse_middle, 0),
        ],
        x_minus=[
            StructureRotation(brickhouse_middle, 0),
        ],
        z_plus=[
            StructureRotation(brickhouse_middle, 2),
            *all_rotations(brickhouse_center),
        ],
    ),
    brickhouse_center: StructureAdjacency(
        structure_name=brickhouse_center,
        x_plus=[
            *all_rotations(brickhouse_center),
            StructureRotation(brickhouse_middle, 1),
        ],
        x_minus=[
            *all_rotations(brickhouse_center),
            StructureRotation(brickhouse_middle, 3),
        ],
        z_plus=[
            *all_rotations(brickhouse_center),
            StructureRotation(brickhouse_middle, 2),
        ],
        z_minus=[
            *all_rotations(brickhouse_center),
            StructureRotation(brickhouse_middle, 0),
        ],
    ),
}
