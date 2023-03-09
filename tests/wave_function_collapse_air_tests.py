import unittest

from assignment.utils.structure_adjacency import StructureRotation, structure_adjecencies
from assignment.utils.wave_function_collapse import WaveFunctionCollapse

empty_space_air_structure = StructureRotation("empty-space-air", 0)
all_air_structures = set([StructureRotation("empty-space-air", r) for r in range(4)])

def print_state(wfc: WaveFunctionCollapse):
    for y in range(wfc.state_space_size[1]):
        print("Layer y="+str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            print(wfc.state_space[x][y])

class WaveFunctionCollaplse2x1x1_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((2,1,1), structure_adjecencies)
        return super().setUp()

    def test_collapses(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([0,0,0], empty_space_air_structure)

        print_state(self.wfc)
        self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[1][0][0])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)



class WaveFunctionCollaplse2x1x2_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((2,1,2), structure_adjecencies)
        return super().setUp()

    def test_collapses_to_all_air_from_bottom_left(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([0,0,0], empty_space_air_structure)

        print_state(self.wfc)
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][1])

    def test_collapses_with_entrance_top_right(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([1,0,1], StructureRotation("brickhouse-entrance", 0))


        print_state(self.wfc)
        # this i a valid state even though this house is not closed
        #   air         - entrance(0)
        #   entrance(2) - air
        bottom_left_subset = all_air_structures.union(set([StructureRotation("brickhouse-entrance", 2)]))
        self.assertTrue(bottom_left_subset.issubset(self.wfc.state_space[0][0][0]), msg=f"{bottom_left_subset} should be a subset of {self.wfc.state_space[0][0][0]}")

        self.assertEqual(all_air_structures, self.wfc.state_space[1][0][0])
        self.assertEqual(all_air_structures, self.wfc.state_space[0][0][1])
        self.assertEqual(set([StructureRotation("brickhouse-entrance", 0)]), self.wfc.state_space[1][0][1])



class WaveFunctionCollaplse3x1x3_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((3,1,2), structure_adjecencies)
        return super().setUp()
    
    def test_collapses_top_right(self):
        self.wfc.collapse_cell([2,0,1], StructureRotation("brickhouse-entrance", 0))


        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[2][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][1])
        self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[2][0][1])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

    def test_collapses_middle_right(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([1,0,1], StructureRotation("brickhouse-entrance", 0))


        print_state(self.wfc)
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][1])
        self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[1][0][1])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

    def test_collapses(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([2,0,1], StructureRotation("brickhouse-entrance", 1))

        print_state(self.wfc)
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        # self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        # self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][1])

        # self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][1])
        # self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[1][0][1])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

