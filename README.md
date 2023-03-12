# MGAIA-Minecraft
This project was realized for the first assignment of the course Modern Game AI Algorithms at Leiden University on procedural content generation in Minecraft.

This project uses the wave function collapse algorithm to generate randomized realistic buildings in Minecraft.

![Close up of some building structures](docs/images/structures/building-structures-close-up.png)
![Large city of buildings](docs/images/buildings/large-city.png)



# Getting Started
## Installation

The project uses Python [Poetry](https://python-poetry.org/) (version 1.3.2) to manage dependencies. However, installing the dependencies from `pyproject.toml` manually using pip should also work.


## Running

Below are short descriptions on how to use the most important scripts.
The whole end to end script `e2e_brickhouse.py` contains building placement, building generation and interior decoration.


### Building Placement
See `buildregion_finder.py`

### Structure Scanning and Building

1. Set the build area in Minecraft using `/setbuildarea ~1 ~ ~ ~11 ~6 ~10` (or similar)
2. Update the name for the structure in `structure_scanner.py`
3. Run `structure_scanner.py`

The structures are saved in `./structures`. There are some premade ones in this repository.

You can now replicate a single structure using `structure_builder.py` or go to the next steps.

### Building Generation

The main building generation happens in `brickhouse.py`. 
You can also run this file directly to generate a building (a brickhouse in this case).

1. Update the coordinates where to place the house in `brickhouse.py`
2. Update the maximum size of the house including air padding in `brickhouse.py`
    - `WaveFunctionCollapse((7,2,7), structure_adjecencies)` for a house of
    5x2x5 structure building blocks because of  
    "structure" air padding around it
3. Optionally, specify some fixed structures in `reinit()` that guide the algorithm
    - For example `wfc.collapse_cell([8,0,8], StructureRotation(brickhouse_courtyard, 0))` will ensure that a courtyard is placed at position (8,0,8) with rotation 0
    - The algorithm will use this information and build a house around it
    - This is very useful as the algorithm tends to not use certain cool structures ☹️
4. Run `brickhouse.py`. This might take a while. You can see the progress in the terminal.

You can also try to generate on a larger area like ``WaveFunctionCollapse((17,2,17), ...)`
which will likely generate multiple unconnected houses (which still follows the rules!). 
Way larger areas unfortunately don't work because of recursion depth limitations. 

