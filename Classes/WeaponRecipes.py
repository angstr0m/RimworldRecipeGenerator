__author__ = 'Malte Eckhoff'


class WeaponRecipes:
    """
    Data type for holding weapon recipes.
    """
    _weaponData = []
    _weaponRecipes = str

    def __init__(self, weaponRecipes: "", weaponData: []):
        self._weaponRecipes = weaponRecipes
        self._weaponData = weaponData

    @property
    def weaponNames(self):
        return self._weaponData

    @property
    def weaponRecipes(self):
        return self._weaponRecipes
