__author__ = 'Malte Eckhoff'

import configparser


class Config:
    _defaultSection = "Constants"
    _configInitialized = False
    _config = configparser.ConfigParser();

    @classmethod
    def _getKey(cls, key):
        if (not cls._configInitialized):
            cls._readConfigFile()
            cls._configInitialized = True

        return cls._config[cls._defaultSection][key]

    @classmethod
    def _readConfigFile(cls):
        cls._config.read("config.ini")

    @classmethod
    def ReadValue(cls, key):
        return cls._getKey(key);

    @classmethod
    def ReadArray(cls, key):
        return str.split(cls._getKey(key).replace(" ", ""), ",")
