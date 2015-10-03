from Classes.Config import Config

__author__ = 'Malte Eckhoff'


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
        building_templateFile = open(Config.ReadValue("BuildingTemplateFilePath"), 'r')
        building_template = building_templateFile.read()

        out_building = open(file, 'w')

        weaponReceipes = ""

        for weapon in weaponNames:
            weaponReceipes += "<li>Build" + weapon + "</li>\n\t\t\t"

        out_building.write(building_template.replace("[AdditionalReceipes]", weaponReceipes))
