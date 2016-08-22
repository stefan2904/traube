#!/usr/bin/env python

__author__ = "stefan"

import os.path
import json


class Index():
    def __init__(self, idx_path, crypto):
        self.idx_path = idx_path
        self.crypto = crypto
        self.__load()

    def __load(self):
        if os.path.isfile(self.idx_path):
            with open(self.idx_path) as idx_file:
                encrypted = idx_file.read().strip()
                if encrypted is None or len(encrypted) < 1:
                    self.__initializeNewIndex()
                else:
                    decrypted = self.crypto.decrypt(encrypted)
                    self.index = json.loads(decrypted)
        else:
            self.__initializeNewIndex()

    def save(self):
        decrypted = json.dumps(self.index)
        encrypted = self.crypto.encrypt(decrypted)
        with open(self.idx_path, 'w') as idx_file:
            idx_file.write(encrypted)
        print(' written index to %s!' % self.idx_path)
        print(decrypted)

    def __initializeNewIndex(self):
        self.index = {}
        self.index['generator'] = 'traube'
        self.index['data'] = {}

    def isUploaded(self, name, path_to_check):
        if name not in self.index['data']:
            self.index['data'][name] = {}
        else:
            node = self.index['data'][name]
            for alias, path in node.items():
                # print('%s: %s' % (alias, path))
                if path == path_to_check:
                    return True
        return False

    def add(self, name, alias, path):
        if name not in self.index['data']:
            self.index['data'][name] = {}
        node = self.index['data'][name]
        node[alias] = path
