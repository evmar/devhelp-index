#!/usr/bin/python

import bz2
import glob
import logging
import os
import xml.etree.ElementTree as ET
import re
import sys

CACHE_PATH = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
DB_PATH = os.path.join(CACHE_PATH, 'devhelp-index.bz2')

def devhelp_tag(name):
    return '{http://www.devhelp.net/book}' + name

def process(path):
    tree = ET.parse(path)

    book = tree.getroot()
    basedir = book.attrib.get('base', os.path.dirname(path))

    functions = tree.find(devhelp_tag('functions'))
    for keyword in functions.getiterator(devhelp_tag('keyword')):
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
            if attrs['link'] == '404':
                continue

            words = attrs['name'].split()

            # Drop e.g. operator[].
            if filter(lambda w: re.search(r'\boperator\b', w), words):
                continue

            strip = ('()', 'enum', 'struct', 'union')
            words = filter(lambda w: w not in strip, words)
            if len(words) != 1:
                logging.warning('unhandled name: ' + str(attrs))
                continue
            word = words[0]

            if word.endswith('()'):
                word = word[:-2]
            if word.startswith('std::'):
                word = word[5:]
            # XXX check word is only ascii
            yield word, os.path.normpath(os.path.join(basedir, attrs['link']))
        elif attrs['type'] in ('', 'property', 'signal'):
            pass
        else:
            raise NotImplementedError, attrs

def build_index(verbose=True):
    keyvals = []

    gtk_docs = glob.glob('/usr/share/gtk-doc/html/*/*.devhelp2')
    books = glob.glob('/usr/share/devhelp/books/*/*.devhelp2')
    for path in gtk_docs + books:
        if verbose:
            print >>sys.stderr, '*', path
        for kw, link in process(path):
            keyvals.append((kw, link))

    keyvals.sort()

    f = bz2.BZ2File(DB_PATH, 'w')
    for kw, link in keyvals:
        print >>f, '%s %s' % (kw, link)
    f.close()

def get_or_rebuild_index(verbose=True):
    if not os.path.exists(DB_PATH):
        build_index(verbose)
    return bz2.BZ2File(DB_PATH, 'r')

if __name__ == '__main__':
    build_index()
