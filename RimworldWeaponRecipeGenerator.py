import os
import argparse

from Classes.WeaponRecipesParser import WeaponRecipesParser
from Classes.WeaponRecipesWriter import WeaponRecipesWriter

__author__ = 'Malte Eckhoff'

# Parse arguments
parser = argparse.ArgumentParser(description='Process Rimworld things def and create receipes for them.')
parser.add_argument('input', help='The file or folder from which the weapons will be read.')
parser.add_argument('outputFile_recipes', help='The file to which the receipes will be written to.')
parser.add_argument('outputFile_building', help='The file to which the building defs will be written to.')
args = parser.parse_args()

recipeParser = WeaponRecipesParser()
recipeWriter = WeaponRecipesWriter()

weaponrecipes = None

if (os.path.isfile(args.input)):
    weaponrecipes = recipeParser.GetWeaponRecipesFromFile(args.input)
elif (os.path.isdir(args.input)):
    weaponrecipes = recipeParser.GetWeaponRecipesFromFolder(args.input)
else:
    raise ValueError("Specified input '" + args.input + "' is neither a valid file nor folder.")

recipeWriter.WriteRecipeFile(args.outputFile_recipes, weaponrecipes.weaponRecipes)
recipeWriter.WriteBuildingFile(args.outputFile_building, weaponrecipes.weaponNames)
