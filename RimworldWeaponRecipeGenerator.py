import os
import xml
import argparse
import xml.etree.ElementTree as ET
import sys

__author__ = 'Malte Eckhoff'

class WeaponRecipes:
    """
    Data type for holding weapon recipes.
    """
    _weaponNames = []
    _weaponRecipes = str

    def __init__(self, weaponRecipes: "", weaponNames: []):
        self._weaponRecipes = weaponRecipes
        self._weaponNames = weaponNames

    @property
    def weaponNames(self):
        return self._weaponNames

    @property
    def weaponRecipes(self):
        return self._weaponRecipes

class WeaponRecipesParser:
    def GetWeaponRecipesFromFile(self, file: str) -> WeaponRecipes:
        """
        Gets an array of strings containing all weapon recipes from a specified XML file at position 0
        and an array of all weapon names at position 1.
        :param file: str The XML file that contains the weapon recipes
        """
        try:
            tree = ET.parse(file)
        except xml.etree.ElementTree.ParseError:
            print("Could not parse file '" + file + "': Invalid XML.")
            return WeaponRecipes("", [])

        root = tree.getroot()
        weaponRecipes = ""
        weaponNames = []

        # Read the template file that will be used to construct a single recipe
        receipe_templateFile = open('./Templates/recipeTemplate.xml', 'r')
        receipe_template = receipe_templateFile.read()

        for child in root:
            if ('ParentName' in child.attrib):
                parentClass = child.attrib['ParentName']

                # Weapon classes
                allowedClasses = ["BaseHumanGun", "BaseMeleeWeapon_Blunt", "BaseMeleeWeapon_Sharp"]

                # Check if the current thing is a weapon
                if (parentClass in allowedClasses):
                    if (child.find('defName') != None):
                        try:
                            # Get the name of the weapon
                            weaponName = "".join(child.find('defName').itertext())
                            weaponNames.append(weaponName)

                            # Get the marketvalue of the weapon
                            weaponCost = int("".join(next(child.iterfind('.//MarketValue')).itertext()))

                            # Replace the placeholder string in the template with the values from the current weapon
                            currentWeaponRecipe = receipe_template.replace('[WeaponName]', weaponName)

                            # Set the cost of the weapon according to its market value
                            currentWeaponRecipe = currentWeaponRecipe.replace('[WorkAmount]', str(weaponCost // 2))
                            currentWeaponRecipe = currentWeaponRecipe.replace('[SteelCost]', str(weaponCost // 10))
                            currentWeaponRecipe = currentWeaponRecipe.replace('[SilverCost]', str(weaponCost // 100))

                            weaponRecipes += currentWeaponRecipe + "\n"
                        except StopIteration:
                            pass
                        except:
                            # Could not parse file this file
                            print("Error while parsing file '" + file + "':\n" + str(sys.exc_info()[0]))
                            pass

        return WeaponRecipes(weaponRecipes, weaponNames)

    def GetWeaponRecipesFromFolder(self, folder: str) -> WeaponRecipes:
        """
        Gets an array of strings containing all weapon recipes from all XML files in a specified folder at position 0
        and an array of all weapon names at position 1.
        :param folder: str The folder that will be recursively searched for XML files.
        """

        weaponNames = []
        weaponRecipes = ""

        # Iterate over all files in the specified folder recursively
        for root, directories, filenames in os.walk(folder):
                for filename in filenames:
                    # Get the full path to the file
                    pathToFile = os.path.join(root,filename)

                    # Check if this is actually a file
                    if (not os.path.isfile(pathToFile)):
                        continue

                    # Check if this is an XML file
                    extension = os.path.splitext(pathToFile)[1]
                    if (extension.lower() != '.xml'):
                        continue

                    recipesFromFile = self.GetWeaponRecipesFromFile(pathToFile)
                    weaponNames.extend(recipesFromFile.weaponNames)
                    weaponRecipes += recipesFromFile.weaponRecipes

        return WeaponRecipes(weaponRecipes, weaponNames)

class WeaponRecipesWriter:
    def WriteRecipeFile(self, file, recipes: str):
        # Begin writing to file
        out_receipes = open(file, 'w')

        out_receipes.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        out_receipes.write('<RecipeDefs>\n')
        out_receipes.write(recipes)
        out_receipes.write('</RecipeDefs>')

    def WriteBuildingFile(self, file, weaponNames: []):
        # Read the template file
        building_templateFile = open('./Templates/workbenchTemplate.xml', 'r')
        building_template = building_templateFile.read()

        out_building = open(file, 'w')

        weaponReceipes = ""

        for weapon in weaponNames:
            weaponReceipes += "<li>Build" + weapon + "</li>\n\t\t\t"

        out_building.write(building_template.replace("[AdditionalReceipes]", weaponReceipes))

# ----------------------------------------------------------------------------------------------------------

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