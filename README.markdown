# streamstats

**streamstats** is a very simple tool that takes a stream via stdin and does some very basic statistics on it.

The primary usecase is to pipe output from grep/awk which results in one token per line (for example, an IP address out of an apache logfile) and see if any of the values of the token show up more often than others. A real life example of this is seeing if a particular IP is showing up in logs more often than reasonable (something I see our Ops team trying to figure out quite frequently)

## Sample Output:

Assuming you have a logfile where the IP address is the first token (and for some reason, you only had 42 log lines in it, all of which were from local IPs...):

    # cat access.log | awk '{print $1}' | streamstats.py

       192.168.10.100 |                                        1 
       192.168.10.101 |                                        1 
       192.168.10.102 ||||                                     4 
       192.168.10.103 ||||                                     4 
       192.168.10.104 |                                        1 
       192.168.10.105 |                                        1 
       192.168.10.106 |||||                                    5 
       192.168.10.107 ||||                                     4 
       192.168.10.108 |||||||||||                              11 *
       192.168.10.109 ||||||                                   6 
       192.168.10.110 |||                                      3 
       192.168.10.111 |                                        1 

    Some Statsy Things
         count 12
      outliers 1
       maximum 11
       minimum 1
         stdev 2.84312035154
         total 42
          mean 3.5

It'll draw a (somewhat accurate) histogram and highlight any outliers.

Enjoy.