""" Loads and updates CSV format game assets.
"""
from collections import namedtuple
import random
import requests


class Asset:
    TYPES = {'str': str, 'int': int, 'float': float, 'bool': bool}

    def __repr__(self):
        return self._list.__repr__()

    def __init__(self, file_path, delimiter=',', update=False):
        self.file_path = file_path

        if file_path.startswith('http'):
            r = requests.get(file_path)
            if r.ok:
                # Updating is redundant when loading from the web
                update = False
                raw_data = r.text
            else:
                raise FileNotFoundError(f'Failed to get file from {file_path}.')
        else:
            with open(file_path, 'r') as f:
                raw_data = f.read()

        # Aggregate header lines into dict
        self.headers = Asset.parse_headers(raw_data)

        if update:
            if (url := self.headers.get('url')):
                r = requests.get(url)
                if r.ok:
                    web_data = r.text
                    web_headers = Asset.parse_headers(web_data)
                    # Check if web version is newer than local
                    if int(web_headers.get('version', '0')) > \
                       int(self.headers.get('version', '0')):
                        # Replace local content with web content
                        raw_data = web_data
                        self.headers = web_headers

                        # Commit update to file
                        with open(file_path, 'w') as f:
                            f.write(web_data)

        # Parse column definitions in to list of (name, type)
        try:
            self.columns = [(col.split(':')[0].strip(), 
                            Asset.TYPES[col.split(':')[1].strip()])
                            for line in raw_data.splitlines()
                            if line.startswith('@')
                            for col in line.strip('@').lower().split(',') ]
        except IndexError:
            raise SyntaxError('Type hint not found for column.' + \
                              f'\nIn file: "{self.file_path}"')
        except KeyError as e:
            raise TypeError(f'Invalid type "{e.args[0]}" in column ' + \
                            f'declaration.\nIn file: "{self.file_path}"')

        # Ensure column declaration line was found
        if not self.columns:
            raise SyntaxError('Column declaration not found in file. ' + \
                              '(Did you forget the \'@\'?)' + \
                              f'\nIn file: "{self.file_path}"')

        # Create namedtuple with according to type header
        self.type = namedtuple(self.headers.get('type', 'Generic'), 
                               [name for name, _ in self.columns])

        self._list = list()
        for line in (line.strip() for line in raw_data.splitlines()
                     if not line.startswith('@') 
                     and not line.startswith('#')):
            self._list.append(
                self.type(*[self.columns[i][1](col.strip())
                            for i, col in enumerate(line.split(','))])
            )

    def __getitem__(self, *args, **kwargs):
        return self._list.__getitem__(*args, **kwargs)

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()

    @staticmethod
    def sanitize(text, lower=False):
        text = text.strip()
        if lower:
            text = text.lower()
        return text

    @staticmethod
    def parse_headers(text):
        return {line.split('=')[0][1:]: line.split('=')[1]
                for line in text.splitlines()
                if line.startswith('#')}


if __name__ == '__main__':
    weapons = Asset('https://pastebin.com/raw/DAGHFB7E')
    for weapon in weapons:
        print(weapon)
