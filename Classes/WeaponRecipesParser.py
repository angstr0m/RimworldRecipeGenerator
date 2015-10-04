import os
import sys
import xml
from xml.etree import ElementTree as ET

from Classes.Config import Config
from Classes.WeaponRecipes import WeaponRecipes

__author__ = 'Malte Eckhoff'

class ItemFromXML:
    pass

class WeaponRecipesParser:
    def GetItemsFromFile(self, file: str, allowedClasses: [], keysToRead: []) -> [ItemFromXML]:
        try:
            tree = ET.parse(file)
        except xml.etree.ElementTree.ParseError:
            print("Could not parse file '" + file + "': Invalid XML.")
            return WeaponRecipes("", [])

        itemData = []

        root = tree.getroot()

        for child in root:
            if ('ParentName' in child.attrib):
                # Get the class this thing def is derived from
                parentClass = child.attrib['ParentName']

                # Check if the current thing is a weapon
                if (parentClass in allowedClasses):
                    try:
                        currentItem = ItemFromXML()
                        tags = list(child.iter())
                        for xmlItem in tags:
                            if xmlItem.tag in keysToRead:
                                setattr(currentItem, xmlItem.tag, xmlItem.text)

                        objectValid = True;

                        # Only add objects to the return list that satisfy all specified keys.
                        for key in keysToRead:
                            if not hasattr(currentItem, key):
                                objectValid = False
                                break

                        if objectValid:
                            itemData.append(currentItem)
                    except:
                        # Could not parse file this file
                        print("Error while parsing file '" + file + "':\n" + str(sys.exc_info()[0]))
                        pass

        return itemData


    def GetWeaponRecipesFromFile(self, file: str) -> WeaponRecipes:
        """
        Gets an array of strings containing all weapon recipes from a specified XML file at position 0
        and an array of all weapon names at position 1.
        :param file: str The XML file that contains the weapon recipes
        """
        weaponRecipes = ""

        # Read the template file that will be used to construct a single recipe
        receipe_templateFile = open(Config.ReadValue("RecipeTemplate"), 'r')
        receipe_template = receipe_templateFile.read()

        # Get the weapons from the file
        allowedClasses = Config.ReadArray("WeaponBaseClasses")
        keysToRead = Config.ReadArray("WeaponReadKeys")
        weaponsFromFile = self.GetItemsFromFile(file, allowedClasses, keysToRead)

        for weapon in weaponsFromFile:
            # Get the name of the weapon
            weaponName = weapon.label

            # Get the description of the weapon
            weaponDesc = weapon.description

            # Get the definition name of the weapon
            weaponDefName = weapon.defName

            # Get the marketvalue of the weapon
            weaponCost = int(weapon.MarketValue)

            # Replace the placeholder strings in the template with the values from the current weapon
            currentWeaponRecipe = receipe_template.replace('[WeaponName]', weaponName)
            currentWeaponRecipe = currentWeaponRecipe.replace('[WeaponDefName]', weaponDefName)
            currentWeaponRecipe = currentWeaponRecipe.replace('[WeaponDesc]', weaponDesc)

            # Set the cost of the weapon according to its market value
            currentWeaponRecipe = currentWeaponRecipe.replace('[WorkAmount]', str(weaponCost // 2))
            currentWeaponRecipe = currentWeaponRecipe.replace('[SteelCost]', str(weaponCost // 10))
            currentWeaponRecipe = currentWeaponRecipe.replace('[SilverCost]', str(weaponCost // 100))

            weaponRecipes += currentWeaponRecipe + "\n"

        return WeaponRecipes(weaponRecipes, weaponsFromFile)

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
