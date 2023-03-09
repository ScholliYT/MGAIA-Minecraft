import itertools
import unittest

from assignment.utils.structure_adjacency import StructureRotation, structure_adjecencies, all_rotations
from assignment.utils.structures import (
    brickhouse_balcony,
    brickhouse_big_window_flat_roof,
    brickhouse_center,
    brickhouse_corner,
    brickhouse_courtyard,
    brickhouse_entrance,
    brickhouse_middle,
    brickhouse_roofhouse_corner,
    brickhouse_roofhouse_courtyard,
    brickhouse_roofhouse_middle,
    brickhouse_small_window_flat_roof,
    empty_space_air,
)
from assignment.utils.wave_function_collapse import WaveFunctionCollapse

empty_space_air_structure = StructureRotation(empty_space_air, 0)
all_air_structures = set([StructureRotation(empty_space_air, r) for r in range(4)])

def print_state(wfc: WaveFunctionCollapse):
    for y in range(wfc.state_space_size[1]):
        print("Layer y="+str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            print(wfc.state_space[x][y])

def collapse_to_air_on_outer_rectangle(wfc: WaveFunctionCollapse):
        for x in range(wfc.state_space_size[0]):
            last = wfc.state_space_size[2]-1
            wfc.collapse_cell([x,0,0], StructureRotation(empty_space_air, 0))
            wfc.collapse_cell([x,0,last], StructureRotation(empty_space_air, 0))

        for z in range(wfc.state_space_size[2]):
            last = wfc.state_space_size[0]-1
            wfc.collapse_cell([0,0,z], StructureRotation(empty_space_air, 0))
            wfc.collapse_cell([last,0,z], StructureRotation(empty_space_air, 0))


class WaveFunctionCollaplse2x1x1_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((2,1,1), structure_adjecencies)
        return super().setUp()

    def test_collapses(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([0,0,0], empty_space_air_structure)

        print_state(self.wfc)
        self.assertIn(StructureRotation(brickhouse_entrance, 0), self.wfc.state_space[1][0][0])

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
        self.wfc.collapse_cell([1,0,1], StructureRotation(brickhouse_entrance, 0))


        print_state(self.wfc)
        # this i a valid state even though this house is not closed
        #   air         - entrance(0)
        #   entrance(2) - air
        bottom_left_subset = all_air_structures.union(set([StructureRotation(brickhouse_entrance, 2)]))
        self.assertTrue(bottom_left_subset.issubset(self.wfc.state_space[0][0][0]), msg=f"{bottom_left_subset} should be a subset of {self.wfc.state_space[0][0][0]}")

        self.assertEqual(all_air_structures, self.wfc.state_space[1][0][0])
        self.assertEqual(all_air_structures, self.wfc.state_space[0][0][1])
        self.assertEqual(set([StructureRotation(brickhouse_entrance, 0)]), self.wfc.state_space[1][0][1])



class WaveFunctionCollaplse3x1x3_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((3,1,3), structure_adjecencies)
        return super().setUp()
    
    def test_collapses_top_right(self):
        self.wfc.collapse_cell([2,0,1], StructureRotation(brickhouse_entrance, 0))


        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[2][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][1])
        self.assertIn(StructureRotation(brickhouse_entrance, 0), self.wfc.state_space[2][0][1])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

    def test_collapses_to_2x2_house(self):
        self.wfc.collapse_cell([0,0,0], StructureRotation(brickhouse_entrance, 0))
        self.wfc.collapse_cell([0,0,1], StructureRotation(brickhouse_entrance, 3))
        self.wfc.collapse_cell([1,0,0], StructureRotation(brickhouse_entrance, 1))
        self.wfc.collapse_cell([1,0,1], StructureRotation(brickhouse_entrance, 2))

        self.wfc.collapse_cell([2,0,2], empty_space_air_structure)

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 1)

    def test_collapses_middle_right(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([1,0,1], StructureRotation(brickhouse_entrance, 0))


        print_state(self.wfc)
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])
        self.assertIn(empty_space_air_structure, self.wfc.state_space[0][0][1])
        self.assertIn(StructureRotation(brickhouse_entrance, 0), self.wfc.state_space[1][0][1])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

    def test_collapses(self):
        print_state(self.wfc)
        self.wfc.collapse_cell([2,0,1], StructureRotation(brickhouse_entrance, 1))

        print_state(self.wfc)
        self.assertIn(empty_space_air_structure, self.wfc.state_space[1][0][0])

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)



class WaveFunctionCollaplse5x1x5_Surrounded_Air_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((5,1,5), structure_adjecencies)
        collapse_to_air_on_outer_rectangle(self.wfc)
        return super().setUp()
    
    def _assert_centered_3x3_building(self):
        for r in range(4):
            air = StructureRotation(empty_space_air, r)
            for x,y in itertools.product(range(1,4), range(1,4)):
                self.assertNotIn(air, self.wfc.state_space[x][0][y])

    
    def test_collapses_3x3_diagonal_corners(self):
        self.wfc.collapse_cell([1,0,1], StructureRotation(brickhouse_entrance, 0))
        self.wfc.collapse_cell([3,0,3], StructureRotation(brickhouse_entrance, 2))

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        self._assert_centered_3x3_building()

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

    def test_collapses_3x3_corner_and_middle_wall(self):
        self.wfc.collapse_cell([1,0,1], StructureRotation(brickhouse_entrance, 0))
        self.wfc.collapse_cell([2,0,3], StructureRotation(brickhouse_middle, 2))

        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        self._assert_centered_3x3_building()

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)
