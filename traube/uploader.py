#!/usr/bin/env python

__author__ = "stefan"

import os

import click

from config import loadConfig
from index import Index
from crypto import Crypto


class Uploader():
    def __init__(self, remote, idx, crypto):
        self.remote = remote
        self.idx = idx
        self.crypto = crypto
        print('# TODO: create temporary dir $tmp')
        self.tmp = '/tmp/traube'

    def upload(self, name, dir, keys):
        print('   %s: uploading %s ...' % (name, dir))
        for file in os.listdir(dir):
            path = dir + '/' + file
            print('    uploading %s' % path)
            if self.idx.isUploaded(name, file):
                print('      already in index. skipping ...')
            else:
                alias = self.crypto.getRandomBits()
                self.__doUpload(alias, path, keys)
                self.idx.add(name, alias, file)

    def __doUpload(self, alias, path, keys):
        target = self.tmp + '/' + alias
        print('     encrypt file %s to %s for %d keys' % (path, target, len(keys)))
        self.crypto.encryptFile(path, target, keys)

        print('     # TODO: upload %s to %s' % (target, self.remote))


@click.command()
@click.option('--config', help='Location of your traube.cfg', required=True)
def main(config):
    print(' loading config from %s' % config)
    base_path, idx_path, remote, key, keys, sources = loadConfig(config)

    print(' initializing crypto')
    crypto = Crypto(key, keys, base_path)

    print(' loading index from %s' % idx_path)
    idx = Index(idx_path, crypto)

    upl = Uploader(remote, idx, crypto)

    for name, data in sources.items():
        dir = base_path + data['dir']
        keys = data['keys']
        upl.upload(name, dir, keys)

    print('')
    idx.save()


if __name__ == '__main__':
    print('Welcome to traube!')
    main()
