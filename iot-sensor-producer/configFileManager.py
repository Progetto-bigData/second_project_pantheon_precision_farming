import configparser


'''
    This module is responsible for reading and writing properties 
    specified in the properties.ini file.
'''

def read_config_file(section, property_name, file_name = "./properties.ini"):
    config = configparser.ConfigParser()
    config.read(file_name)
    return config.get(section, property_name)


def write_config_file(section, property_name, value, file_name = "./properties.ini"):
    config = configparser.ConfigParser()
    config[section] = {}
    config[section][property_name] = value
    with open(file_name, 'w') as configFile:
        config.write(configFile) 
