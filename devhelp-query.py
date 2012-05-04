#!/usr/bin/python

import optparse
import sys

index = __import__('devhelp-index')

def main():
    parser = optparse.OptionParser(usage='%prog [options] keyword')
    opts, args = parser.parse_args()
    if len(args) != 1:
        print 'ERROR: expected keyword argument'
        print
        parser.print_help()
        return 1
    query = args[0]

    db = index.get_or_rebuild_index(verbose=False)

    result = None

    query += ' '
    for line in db:
        if line.startswith(query):
            result = line[len(query):].strip()
            break

    if result is None:
        return 1
    print result
    return 0

if __name__ == '__main__':
    sys.exit(main())
