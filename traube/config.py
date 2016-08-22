#!/usr/bin/env python

__author__ = "stefan"

import configparser
import os


def initParser(config_path):
    parser = configparser.ConfigParser()
    parser.read(config_path)
    return parser


def parseGlobal(parser, base):
    if 'GLOBAL' not in parser:
        raise KeyError('Invalid config ... No GLOBAL section.')
    glob = parser['GLOBAL']
    if 'remote' not in glob or 'index' not in glob or 'key' not in glob:
        raise KeyError('Invalid config... No remote/index/key.')
    idx = glob['index']
    if not idx.startswith('/'):
        idx = idx[1:] if idx.startswith('.') else idx
        idx = '/' + idx if not idx.startswith('/') else idx
        idx = base + idx

    return idx, glob['remote'], glob['key']


def parseKeys(parser):
    if 'KEYS' not in parser:
        raise KeyError('Invalid config ... No KEYS section.')
    return parser['KEYS']


def parseSources(parser):
    sections = parser.sections()
    sections.remove('GLOBAL')
    sections.remove('KEYS')
    sources = {}
    for section in sections:
        s = parser[section]
        if 'dir' not in s or 'keys' not in s:
            raise KeyError('Invalid config... No dir/keys for %s' % s['name'])
        name = s['name'].replace(' ', '_')
        source = {}
        source['dir'] = s['dir'][1:] if s['dir'].startswith('.') else s['dir']
        source['keys'] = s['keys'].split(',')
        sources[name] = source
    return sources


def loadConfig(config_path):
    parser = initParser(config_path)
    base = os.path.split(config_path)[0]

    idx, remote, key = parseGlobal(parser, base)
    keys = parseKeys(parser)
    sources = parseSources(parser)
    return base, idx, remote, key, keys, sources
