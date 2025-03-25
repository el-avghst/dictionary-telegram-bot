import requests
import json


class WrongCommand(Exception):
    pass

class Word:

    def __init__(self, word):
        self.count = 1
        self.word = word


    def get_definition(self):
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + self.word
        res = requests.get(url).json()
        definitions = res[0]['meanings']
        string = ''
        for definition in definitions:
            string += str(self.count)
            string += ' – '
            string += str(definition['definitions'][0]['definition'])
            string += '\n'
            self.count += 1
        return string

    def get_phonetics(self):
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + self.word
        res = requests.get(url).json()
        return res[0]['phonetics'][1]['text']