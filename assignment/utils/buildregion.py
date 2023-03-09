import itertools
from typing import Tuple
import numpy as np
from tqdm import tqdm


def terraform_distance(heights: np.ndarray, y: int, origin: Tuple[int,int], size: Tuple[int,int]) -> int:
    """Calculate how many blocks need to be placed and removed to make area falt on level y.

    Args:
        heights (np.ndarray): heightmap
        y (int): desired height of area (
        origin (Tuple[int,int,int,int]): the bottom left corner of the area to flatten in local coordinates x,z
        size (Tuple[int,int,int,int]): the size of the area to flatten in x,z
    """
    
    assert origin >= (0,0)
    assert origin[0]+size[0] <= heights.shape[0]
    assert origin[1]+size[1] <= heights.shape[1]

    heights_slice = heights[origin[0]:origin[0]+size[0], 
                            origin[1]:origin[1]+size[1]]

    edit_distance = np.sum(np.abs(heights_slice - y))

    assert edit_distance == int(edit_distance)
    return int(edit_distance)


def score_all_possible_buildregions(heights: np.ndarray, square_sidelenght=11, min_adjecent_squares=1, max_adjecent_squares=5, buffer=0):

    max_x, max_z = heights.shape

    sidelengths = range(square_sidelenght*min_adjecent_squares + 2*buffer, square_sidelenght*max_adjecent_squares+1 + 2*buffer, square_sidelenght)
    sizes = itertools.product(sidelengths, repeat=2)
    origins = itertools.product(range(max_x), range(max_z))
    for size, origin in tqdm(itertools.product(sizes, origins)):
            
        if origin[0]+size[0] <= heights.shape[0] and origin[1]+size[1] <= heights.shape[1]:
            heights_slice = heights[origin[0]:origin[0]+size[0], 
                                    origin[1]:origin[1]+size[1]]
            
            y_mean = int(np.mean(heights_slice))
            for y in range(y_mean-1, y_mean+2):
                if y == 63:
                    continue # water level
                distance = terraform_distance(heights, y, origin, size)
                yield  origin, size, y, distance
