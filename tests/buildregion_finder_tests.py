import unittest

import numpy as np

from assignment.utils.buildregion import score_all_possible_buildregions, terraform_distance

class TestTerraformDistance(unittest.TestCase):

    def test_distance_2x2(self):
        heightmap = np.array([[5,4],[6,5]])

        result = terraform_distance(heightmap, 5, (0,0), (2,2))

        self.assertEqual(result, 2)


class TestOptimizer(unittest.TestCase):


    def setUp(self) -> None:
        self.numpy_random_state = np.random.get_state()
        np.random.seed(42)
        return super().setUp()
    
    def tearDown(self) -> None:
        np.random.set_state(self.numpy_random_state)
        return super().tearDown()

    def test_optimize_2x2(self):
        heightmap = np.array([
            [5,4],
            [7,5]
        ])
        result = list(score_all_possible_buildregions(heightmap, square_sidelenght=1, max_adjecent_squares=2))

        # size 1x1
        self.assertIn(((0,0), (1,1), 5, 0), result)
        self.assertIn(((0,1), (1,1), 4, 0), result)
        self.assertIn(((1,0), (1,1), 7, 0), result)
        self.assertIn(((1,1), (1,1), 5, 0), result)

        # size 1x2
        self.assertIn(((0,0), (1,2), 5, 1), result)
        self.assertIn(((1,0), (1,2), 5, 2), result)

        # size 2x1
        self.assertIn(((0,0), (2,1), 5, 2), result)
        self.assertIn(((0,1), (2,1), 5, 1), result)

        # size 2x2
        self.assertIn(((0,0), (2,2), 5, 3), result)

        self.assertTrue(len(result) >= 9)



    def test_optimize_5x5(self):
        heightmap = np.array([
            [5,4,5,5,5],
            [6,5,5,4,5],
            [7,8,5,5,5],
            [4,4,4,4,4],
            [3,3,3,3,3]
        ])

        result = list(score_all_possible_buildregions(heightmap, square_sidelenght=1, max_adjecent_squares=3))

        self.assertIn(((0,2), (3,3), 5, 1), result)


    def test_optimize_100x100(self):
        heightmap = np.random.randint(low=10, high=20, size=(100,100))

        result = list(score_all_possible_buildregions(heightmap, square_sidelenght=11, min_adjecent_squares=2, max_adjecent_squares=4))

        self.assertIsNotNone(result)

        sorted_result = sorted(result, key=lambda r: r[3])
        self.assertLessEqual(sorted_result[0][3], 300)
        
