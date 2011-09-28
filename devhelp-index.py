#!/usr/bin/python

import anydbm
import glob
import logging
import os
import xml.etree.ElementTree as ET

CACHE_PATH = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
DB_PATH = os.path.join(CACHE_PATH, 'devhelp-index.db')

def devhelp_tag(name):
    return '{http://www.devhelp.net/book}' + name

def process(path):
    tree = ET.parse(path)
    functions = tree.find(devhelp_tag('functions'))
    for keyword in functions.iter(devhelp_tag('keyword')):
        KEEP = (
            'constant',
            'enum',
            'function',
            'macro',
            'struct',
            'typedef',
            'union',
            'variable',
            )
        attrs = keyword.attrib
        if attrs['type'] in KEEP:
            words = attrs['name'].split()
            strip = ('()', 'enum', 'struct', 'union')
            words = filter(lambda w: w not in strip, words)
            if len(words) == 1:
                yield words[0], attrs['link']
            else:
                logging.warning('unhandled: ' + str(attrs))
        elif attrs['type'] in ('', 'property', 'signal'):
            pass
        else:
            raise NotImplementedError, attrs

def build_index(verbose=True):
    db = anydbm.open(DB_PATH, 'n')
    for path in glob.glob('/usr/share/gtk-doc/html/*/*.devhelp2'):
        if verbose:
            print '*', path
        dir = os.path.dirname(path)
        for kw, link in process(path):
            db[kw] = os.path.join(dir, link)
    return db

def get_or_rebuild_index(verbose=True):
    if not os.path.exists(DB_PATH):
        return build_index(verbose)
    return anydbm.open(DB_PATH, 'r')

if __name__ == '__main__':
    build_index()
