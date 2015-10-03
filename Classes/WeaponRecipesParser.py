import os
import sys
import xml
from xml.etree import ElementTree as ET

from Classes.Config import Config
from Classes.WeaponRecipes import WeaponRecipes

__author__ = 'Malte Eckhoff'


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
        receipe_templateFile = open(Config.ReadValue("RecipeTemplate"), 'r')
        receipe_template = receipe_templateFile.read()

        for child in root:
            if ('ParentName' in child.attrib):
                parentClass = child.attrib['ParentName']

                # Weapon classes
                allowedClasses = Config.ReadArray("WeaponBaseClasses")

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
                pathToFile = os.path.join(root, filename)

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
