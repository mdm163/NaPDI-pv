# Description - dump-all-substrate-of-evidence.py
# 

import os,sys, string, cgi
from time import time, strftime, localtime

import sys

from DIKB.ModelUtils import *
from DIKB.DIKB import *
from DIKB.DrugModel import *
from DIKB.EvidenceModel import *
from DIKB.ExportAssertions import *

timestamp = strftime("%m/%d/%Y %H:%M:%S\n", localtime(time()))

ident = "".join(["SQL DIKB evidence as of May 2017: ", timestamp])

### LOAD EV-BASE
ev = EvidenceBase("evidence","May2017")
ev.unpickleKB("dikb-pickles/ev-test-two.pickle")

for k,v in ev.objects.iteritems():
    if v.slot == 'substrate_of':
        for e in v.evidence_for:
            print '\t'.join([v.object, v.slot, v.value, 'EVIDENCE FOR', e.doc_pointer, e.evidence_type.value, 'https://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/dikb-web/' + k + '.html'])
        for e in v.evidence_against:
            print '\t'.join([v.object, v.slot, v.value, 'EVIDENCE AGAINST', e.doc_pointer, e.evidence_type.value, 'https://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/dikb-web/' + k + '.html'])


