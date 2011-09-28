#!/usr/bin/python

import bz2
import glob
import logging
import os
import xml.etree.ElementTree as ET
import sys

CACHE_PATH = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
DB_PATH = os.path.join(CACHE_PATH, 'devhelp-index.bz2')
GTK_DOC_PATH = '/usr/share/gtk-doc/html/'

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
            if len(words) != 1:
                logging.warning('unhandled: ' + str(attrs))
                continue
            word = words[0]

            if word.endswith('()'):
                word = word[:-2]
            # XXX check word is only ascii
            yield word, attrs['link']
        elif attrs['type'] in ('', 'property', 'signal'):
            pass
        else:
            raise NotImplementedError, attrs

def build_index(verbose=True):
    keyvals = []

    for path in glob.glob(GTK_DOC_PATH + '*/*.devhelp2'):
        if verbose:
            print >>sys.stderr, '*', path
        dir = os.path.dirname(path[len(GTK_DOC_PATH):])
        for kw, link in process(path):
            link = os.path.join(dir, link)
            keyvals.append((kw, link))

    keyvals.sort()

    with bz2.BZ2File(DB_PATH, 'w') as f:
        for kw, link in keyvals:
            print >>f, '%s %s' % (kw, link)

def get_or_rebuild_index(verbose=True):
    if not os.path.exists(DB_PATH):
        build_index(verbose)
    return bz2.BZ2File(DB_PATH, 'r')

if __name__ == '__main__':
    build_index()
