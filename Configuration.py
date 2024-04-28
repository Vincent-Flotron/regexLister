import configparser

class Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.conf')

    def read_value(self, section_name, parameter_name, fallback_value):
        return self.config.get(section_name, parameter_name, fallback=fallback_value)