


import itertools
import random
from typing import Dict, List, Set, Tuple

from assignment.utils.structure_adjacency import StructureAdjacency, StructureRotation


class WaveFunctionCollapse:

    def __init__(self, state_space_size: Tuple[int,int,int], structure_adjecencies: Dict[str, StructureAdjacency]) -> None:
        if not state_space_size >= (1,1,1):
            raise ValueError("State space size should be at least (1,1,1)")

        self.state_space_size = state_space_size
        self.structure_adjecencies = structure_adjecencies

        self.superposition = set(
            StructureRotation(s_name, rotation) 
            for s_name, rotation in itertools.product(structure_adjecencies.keys(), range(4)))

        self._initialize_state_space()
    
    def _cell_coordinates(self):
        # return itertools.product(*self.state_space_size)
        for x in range(self.state_space_size[0]):
            for y in range(self.state_space_size[1]):
                for z in range(self.state_space_size[2]):
                    yield (x,y,z)

    def _initialize_state_space(self) -> None:
        self.state_space = [
            [[self.superposition.copy() # TODO: is a copy enough?
             for z in range(self.state_space_size[2])] 
             for y in range(self.state_space_size[1])] 
             for x in range(self.state_space_size[0])]

    def collapsed(self) -> bool:
        """Return true iff all states are collapes to exactly one elemnt

        Returns:
            bool: true iff all states are collapes to exactly one elemnt
        """
        return len(list(self.cells_with_entropy(1))) == (self.state_space_size[0] * self.state_space_size[1] * self.state_space_size[2])
    
    def min_entropy(self) -> int:
        """Minimal entropy of all states that is != 1

        Returns:
            int: Minimal entropy of all states
        """
        min_entropy = len(self.superposition)+1 # larger than maximum possible value
        for x,y,z in self._cell_coordinates():
                cell = self.state_space[x][y][z]
                if len(cell) < min_entropy and len(cell) != 1:
                    min_entropy = len(cell)
        return min_entropy

    def cells_with_entropy(self, entropy: int):
        """All cells with the specified entropy

        Args:
            entropy (int): the entropy to search for

        Yields:
            Tuple[int,int,int]: (x,y,z) coordinates of the cell
        """
        for x,y,z in self._cell_coordinates():
            cell = self.state_space[x][y][z]
            if len(cell) == entropy:
                yield (x,y,z)

    def collapse_cell(self, cell_xyz: Tuple[int,int,int], colappsed_structure: StructureRotation):
        return self.propagate(cell_xyz, set([colappsed_structure]))

    def propagate(self, cell_xyz: Tuple[int,int,int], remaining_states: Set[StructureRotation]):
        x,y,z = cell_xyz
        if not remaining_states.issubset(self.state_space[x][y][z]):
            raise Exception("Tried to colappse a state to values that are not available in current superposition")
        elif remaining_states == self.state_space[x][y][z]:
            # there is no change and nothing needs to be propagated further
            return

        # update the cell to the one collapsed state. The set only contains one element
        self.state_space[x][y][z] = remaining_states
        
        def neighbour_allowed_states(axis: str):
            """Compute all states that are allowed based on this cells current states

            Args:
                axis (str): direction to compute states for

            Returns:
                Set[StructureRotation]: allowed states
            """
            allowed_states: Set[StructureRotation] = set()
            for s in self.state_space[x][y][z]:
                allowed_states = allowed_states.union(set(self.structure_adjecencies[s.structure_name].adjecent_structrues(axis, s.rotation)))
            return allowed_states
        
        # propagate changes to neighboring cells
        if x > 0:
            neighbour_remaining_states = neighbour_allowed_states("x_minus").intersection(self.state_space[x-1][y][z])
            self.propagate((x-1,y,z), neighbour_remaining_states)
        if x < self.state_space_size[0]-1:
            neighbour_remaining_states = neighbour_allowed_states("x_plus").intersection(self.state_space[x+1][y][z])
            self.propagate((x+1,y,z), neighbour_remaining_states)

        if y > 0:
            neighbour_remaining_states = neighbour_allowed_states("y_minus").intersection(self.state_space[x][y-1][z])
            self.propagate((x,y-1,z), neighbour_remaining_states)
        if y < self.state_space_size[1]-1:
            neighbour_remaining_states = neighbour_allowed_states("y_plus").intersection(self.state_space[x][y+1][z])
            self.propagate((x,y+1,z), neighbour_remaining_states)

        if z > 0:
            neighbour_remaining_states = neighbour_allowed_states("z_minus").intersection(self.state_space[x][y][z-1])
            self.propagate((x,y,z-1), neighbour_remaining_states)
        if z < self.state_space_size[2]-1:
            neighbour_remaining_states = neighbour_allowed_states("z_plus").intersection(self.state_space[x][y][z+1])
            self.propagate((x,y,z+1), neighbour_remaining_states)
    
    def collapse(self) -> bool:
            
        while not self.collapsed():
            min_entropy = self.min_entropy()
            if min_entropy == 0:
                # the current state is unsolvable now
                return False

            next_cells_to_collapse = list(self.cells_with_entropy(min_entropy))
            assert len(next_cells_to_collapse) >= 1
            cell_xyz: Tuple[int, int, int] = random.choice(next_cells_to_collapse)
            x,y,z = cell_xyz

            state_superposition = list(self.state_space[x][y][z])
            assert len(state_superposition) >= 2
            collapsed_state: StructureRotation = random.choice(state_superposition)

            self.collapse_cell(cell_xyz, collapsed_state)
        
        return True
    
    def collapse_with_retry(self) -> int:
        retry_counter = 0

        while not self.collapse():
            self._initialize_state_space()
            retry_counter += 1
        return retry_counter

            

        

        



