#!/usr/bin/env python

__author__ = "stefan"

import random

import gnupg


class Crypto():
    def __init__(self, own_key, keys, base):
        self.gpg = gnupg.GPG(binary='/usr/bin/gpg2',
                             # homedir=base + '/traubekeys',
                             homedir='~/.gnupg',
                             # keyring='pubring.gpg',
                             # secring='secring.gpg'
                             )

        self.pubring = self.privring = self.gpg.list_keys()
        self.privring = self.gpg.list_keys(secret=True)

        if not self.__isInSecring(own_key):
            raise Exception('used main key (%s) not in secret keyring (%s).' % (own_key, self.gpg.secring))
        self.own_key = own_key

        self.__loadKeys(keys)

    def __isInKeyring(selfself, key, keyring):
        return any(map(lambda x: x.endswith(key), keyring.fingerprints))

    def __isInSecring(self, key):
        return self.__isInKeyring(key, self.privring)

    def __isInPubring(self, key):
        return self.__isInKeyring(key, self.pubring)

    def __loadKeys(self, keys):
        self.keys = {}
        for user in keys:
            fingerprint = keys[user]
            if not self.__isInPubring(fingerprint):
                raise Exception('Key of %s not in public keyring ...' % user)
            self.keys['user'] = fingerprint

    def decrypt(self, ciphertext):
        return str(self.gpg.decrypt(ciphertext))

    def encrypt(self, plaintext):
        ciphertext = self.gpg.encrypt(plaintext, self.own_key)
        # print(ciphertext.status)
        return str(ciphertext)

    def getRandomBits(self, num=128):
        # not a secure random,
        # should not be used for security purposes.
        return '%x' % random.getrandbits(num)
