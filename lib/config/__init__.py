from os import path

import json

def __get_filepath(filename):
    """ Get a filepath inside this directory. """
    return path.join(path.dirname(path.realpath(__file__)), filename)

def __get_echo_filepath(filename):
    """ Get a filepath inside echoes/. """
    return path.join(path.dirname(path.realpath(__file__)), "echoes", filename)

def __read_json(filename):
    """ Read JSON from a file inside this directory. """
    filepath = __get_filepath(filename)
    result = None
    with open(filepath, 'r') as infile:
        result = json.load(infile)
    return result

def __write_json(filename, data):
    """ Write JSON to a file inside this directory. """
    filepath = __get_filepath(filename)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def bot():
    """ Read bot info from JSON file """
    return __read_json('bot.json')

def token():
    """ Read bot token from JSON file """
    return (__read_json('creds.json'))['token']

def read_eligible_roles():
    """ Read eligible roles from JSON file """
    roles = __read_json('eligible_roles.json')
    return [role.lower() for role in roles]

def write_eligible_roles(roles):
    """ Write eligible roles to JSON file """
    __write_json('eligible_roles.json', [role.lower() for role in roles])

def read_eligible_channels():
    """ Read eligible channels from JSON file """
    return __read_json('eligible_channels.json')

def read_echo(filename):
    filepath = __get_echo_filepath(filename)
    result = []
    with open(filepath, 'r') as infile:
        result.extend(infile.readlines())
    return '\n'.join(result)
