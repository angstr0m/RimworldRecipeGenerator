import xml
import argparse
import xml.etree.ElementTree as ET

__author__ = 'Malte Eckhoff'

# Parse arguments
parser = argparse.ArgumentParser(description='Process Rimworld things def and create receipes for them.')
parser.add_argument('inputFile', help='The file from which the weapons will be read.')
parser.add_argument('outputFile_recipes', help='The file to which the receipes will be written to.')
parser.add_argument('outputFile_workbench', help='The file to which the workbench defs will be written to.')
args = parser.parse_args()

# Parse the input file
tree = ET.parse(args.inputFile)
root = tree.getroot()

# Open the output file
out_receipes = open(args.outputFile_recipes, 'w')
out_building = open(args.outputFile_workbench, 'w')

# Read the template files
receipe_templateFile = open('./Templates/recipeTemplate.xml', 'r')
receipe_template = receipe_templateFile.read()
building_templateFile = open('./Templates/workbenchTemplate.xml', 'r')
building_template = building_templateFile.read()

weaponNames = []

# Begin writing to file
out_receipes.write('<?xml version="1.0" encoding="utf-8" ?>\n')
out_receipes.write('<RecipeDefs>\n')

# Iterate over the XML tree and find all contained weapon names
for child in root:
    if ('ParentName' in child.attrib):
        parentClass = child.attrib['ParentName']

        # Weapon classes
        allowedClasses = ["BaseHumanGun", "BaseMeleeWeapon_Blunt", "BaseMeleeWeapon_Sharp"]

        # Check if the current thing is a weapon
        if (parentClass in allowedClasses):
            if (child.find('defName') != None):
                # Get the name of the weapon
                weaponName = "".join(child.find('defName').itertext())
                weaponNames.append(weaponName)
                # Get the marketvalue of the weapon
                weaponCost = int("".join(next(child.iterfind('.//MarketValue')).itertext()))

                weaponReceipe = receipe_template.replace('[WeaponName]', weaponName)
                weaponReceipe = weaponReceipe.replace('[WorkAmount]', str(weaponCost // 2))
                weaponReceipe = weaponReceipe.replace('[SteelCost]', str(weaponCost // 10))
                weaponReceipe = weaponReceipe.replace('[SilverCost]', str(weaponCost // 100))

                out_receipes.write(weaponReceipe + "\n")

weaponReceipes = ""
for weapon in weaponNames:
    weaponReceipes += "<li>Build" + weapon + "</li>\n\t\t\t"

out_building.write(building_template.replace("[AdditionalReceipes]", weaponReceipes))

# finish writing to the receipes file
out_receipes.write('</RecipeDefs>')