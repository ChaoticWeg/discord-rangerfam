from os import path

import json

def __get_filepath(filename):
    return path.join(path.dirname(path.realpath(__file__)), filename)

def __read_json(filename):
    filepath = __get_filepath(filename)
    result = None
    with open(filepath, 'r') as infile:
        result = json.load(infile)
    return result

def __write_json(filename, data):
    filepath = __get_filepath(filename)
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def bot():
    return __read_json('bot.json')

def token():
    return (__read_json('creds.json'))['token']

def read_eligible_roles():
    roles = __read_json('eligible_roles.json')
    return [role.lower() for role in roles]

def write_eligible_roles(roles):
    __write_json('eligible_roles.json', [role.lower() for role in roles])
