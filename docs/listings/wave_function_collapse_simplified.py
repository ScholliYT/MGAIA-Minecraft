def wfc(self):
    self.self._initialize_state_space_superposition()

    while not self.collapsed():
        min_entropy = self.min_entropy()
        if min_entropy == 0:
            # the current state is unsolvable now. Restart.
            self.self._initialize_state_space_superposition()
            continue

        next_cells_to_collapse = list(self.cells_with_entropy(min_entropy))
        x,y,z = random.choice(next_cells_to_collapse)

        state_superposition = list(self.state_space[x][y][z])
        collapsed_state: StructureRotation = random.choice(state_superposition)

        self.collapse_cell(cell_xyz, collapsed_state)
