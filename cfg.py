#!/usr/bin/python

import novacfg
c = novacfg.novaConfig()
c.info()
s = c.get('QPID', 'qpidhost');
print s
