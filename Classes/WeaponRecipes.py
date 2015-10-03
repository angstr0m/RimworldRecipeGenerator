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
