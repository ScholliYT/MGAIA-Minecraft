import unittest

from assignment.utils.structure_adjacency import structure_adjecencies, check_symmetry


class TestSymmetryChecker(unittest.TestCase):


    def test_current_structure_adjecencies_symmetry(self):
        check_symmetry(structure_adjecencies)
