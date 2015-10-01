# RimworldRecipeGenerator

A small and simple script that generates recipes for use with Brunayla's Security Co Weapon Crafting made by Brunayla.
https://ludeon.com/forums/index.php?topic=7179.0
Tested with Rimsenal by rooki1
https://ludeon.com/forums/index.php?topic=11160.0

## Usage

    python RimworldWeaponRecipeGenerator.py [defitiniton input file] [recipe output file] [weapon crafting output file]

* definition input file - Contains the thing defs for the weapons.
* recipe output file - The file that will contain the generated recipes.
* weapon crafting output file - The building definition for the weapons crafting workbench. This file references the newly
created recipes.

Example:

    python RimworldWeaponRecipeGenerator.py TestInput.xml TestRecipeOutput.xml TestWorkbenchOutput.xml