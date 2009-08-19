#! /usr/bin/python

import sys, math as m
from collections import defaultdict

distribution = defaultdict(lambda: 0)
total = 0

for line in sys.stdin.readlines():
    value = line.strip('\n')
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
    out = "%"+str(token_len)+"s %-40s %s %s\033[m"
    outlier = (distribution[x] < s['mean']-s['stdev'] or s['mean']+s['stdev'] < distribution[x])
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