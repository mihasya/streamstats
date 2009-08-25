#! /usr/bin/python

# License: MIT. Have at it.
#
# streamstats is a simple tool for performing basic stats on a stream of
# values. Pipe something into it and see what happens.
#
# Mikhail Panchenko <m@mihasya.com>

import sys, math as m
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-o", "--outliers", action="store_true", default=False,
    dest="outliers", help="Show only outliers")

parser.add_option("-t", "--time", action="store_true", default=False,
    dest="time", help="Use this command sequence to extract timestamps")

parser.add_option("-p", "--pattern", action="store", default=None, metavar='PTRN',
    dest="time", help="Use this command sequence to extract timestamps")

"""
parser.add_option("-s", "--start", action="store", default=None, metavar='TIME',
    dest="start", help="Starting timestamp")

parser.add_option("-e", "--end", action="store", default=None, metavar='TIME',
    dest="end", help="Ending timestamp")
"""
(options, args) = parser.parse_args()

distribution = {}
total = 0

print options

if (not options['time'] and not options['pattern']):
    pattern = None
else:
    if (options['pattern']):
        pattern = options['pattern']
    else:
        pattern = "\[(?P<time>.+)\]\s+(?P<value>.+)\n";

    import re
    regex = re.compile(pattern)

for line in sys.stdin.readlines():
    if (pattern):
        groups = regex.match(line).groupdict()
        value = groups['value']
        if (options['time']):
            time = groups['time']
    else:
        value = line.strip('\n')

    if value not in distribution:
        distribution[value] = 0
    distribution[value] += 1
    total += 1

s = {} # store our stats in a dict for easy printings later
s['count'] = len(distribution)
s['total'] = sum(distribution.values())
s['mean'] = float(total) / float(s['count'])
s['maximum'] = max(distribution.values())
s['minimum'] = min(distribution.values())
s['stdev'] = m.sqrt(float(sum([m.pow(distribution[x]-s['mean'], 2) for x in distribution]))/float(s['count']))
s['outliers'] = 0

token_len = max([len(x) for x in distribution.keys()]) + 1

for x in distribution:
    outlier = (distribution[x] < s['mean']-(s['stdev']*2) or s['mean']+(s['stdev']*2) < distribution[x])
    if not (not outlier and options.outliers):
        out = "%"+str(token_len)+"s %-40s %s %s\033[m"
        if outlier:
            print "\033[0;31m",
            s['outliers'] += 1
        else:
            print "\033[0m",
        print out % ( str(x),
            '|' * int(m.ceil(float(distribution[x])/s['total'] * 40)),
            distribution[x],
            ['', '*'][outlier] )

print "\nSome Statsy Things"

for x in s:
    print "%10s %s" % (x, s[x])