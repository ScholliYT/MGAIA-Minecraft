import unittest

from assignment.utils.structure_adjacency import StructureRotation, structure_adjecencies
from assignment.utils.wave_function_collapse import WaveFunctionCollapse


def print_state(wfc: WaveFunctionCollapse):
    for y in range(wfc.state_space_size[1]):
        print("Layer y="+str(y))
        for x in reversed(range(wfc.state_space_size[0])):
            print(wfc.state_space[x][y])

class WaveFunctionCollaplse1x1x1Test(unittest.TestCase):

    def test_contstructor(self):
        wfc = WaveFunctionCollapse((1,1,1), structure_adjecencies)
        self.assertEqual(len(wfc.state_space[0][0][0]), len(structure_adjecencies.keys())*4)


    def test_converges(self):
        wfc = WaveFunctionCollapse((1,1,1), structure_adjecencies)

        self.assertFalse(wfc.collapsed())
        some_structure_rotation = next(iter(wfc.state_space[0][0][0]))
        wfc.collapse_cell((0,0,0), some_structure_rotation)
        self.assertTrue(wfc.collapsed())


class WaveFunctionCollaplse2x1x2Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((2,1,2), structure_adjecencies)
        return super().setUp()

    def test_not_initially_collapsed(self):
        self.assertFalse(self.wfc.collapsed())

    def test_converges_on_first_collapse(self):
        self.wfc.collapse_cell((0,0,0), StructureRotation("brickhouse-entrance", 0))
        self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[0][0][0])
        self.assertIn(StructureRotation("brickhouse-entrance", 3), self.wfc.state_space[0][0][1])
        self.assertIn(StructureRotation("brickhouse-entrance", 1), self.wfc.state_space[1][0][0])
        self.assertIn(StructureRotation("brickhouse-entrance", 2), self.wfc.state_space[1][0][1])

    def test_converges_after_two_cell_collapses(self):
        self.wfc.collapse_cell((0,0,0), StructureRotation("brickhouse-entrance", 0))
        self.wfc.collapse_cell((1,0,1), StructureRotation("brickhouse-entrance", 2))
        self.assertIn(StructureRotation("brickhouse-entrance", 0), self.wfc.state_space[0][0][0])
        self.assertIn(StructureRotation("brickhouse-entrance", 3), self.wfc.state_space[0][0][1])
        self.assertIn(StructureRotation("brickhouse-entrance", 1), self.wfc.state_space[1][0][0])
        self.assertIn(StructureRotation("brickhouse-entrance", 2), self.wfc.state_space[1][0][1])
    
    
    def test_collapses(self):
        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 20)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)


class WaveFunctionCollaplse4x1x2Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((4,1,2), structure_adjecencies)
        return super().setUp()

    def test_collapses(self):
        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 20)

        print("WFC collapsed after", retries, "retries")
        for y in range(self.wfc.state_space_size[1]):
            print("Layer y="+str(y))
            for x in reversed(range(self.wfc.state_space_size[0])):
                print(self.wfc.state_space[x][y])


class WaveFunctionCollaplse2x2x2Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((2,2,2), structure_adjecencies)
        return super().setUp()

    def test_collapses(self):
        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 20)

        print("WFC collapsed after", retries, "retries")
        print_state(self.wfc)

class WaveFunctionCollaplse3x1x3Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((3,1,3), structure_adjecencies)
        return super().setUp()
    
    def test_uses_center_tile(self):
        
        self.wfc.collapse_cell([0,0,0], StructureRotation("brickhouse-entrance", 0))

        possible_picks = [(StructureRotation("brickhouse-center", r) in self.wfc.state_space[1][0][1]) for r in range(4)]

        self.assertTrue(all(possible_picks))


    def test_collapses(self):
        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 50)

        print("WFC collapsed after", retries, "retries")
        for y in range(self.wfc.state_space_size[1]):
            print("Layer y="+str(y))
            for x in reversed(range(self.wfc.state_space_size[0])):
                print(self.wfc.state_space[x][y])


class WaveFunctionCollaplse10x1x10Test(unittest.TestCase):

    def setUp(self) -> None:
        self.wfc = WaveFunctionCollapse((10,1,10), structure_adjecencies)
        return super().setUp()

    def test_collapses(self):
        retries = self.wfc.collapse_with_retry()
        self.assertLessEqual(retries, 100)

        print("WFC collapsed after", retries, "retries")
        for y in range(self.wfc.state_space_size[1]):
            print("Layer y="+str(y))
            for x in reversed(range(self.wfc.state_space_size[0])):
                print(self.wfc.state_space[x][y])

