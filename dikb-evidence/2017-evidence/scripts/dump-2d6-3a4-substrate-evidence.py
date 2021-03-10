# Description - Sam Rosko's File to Update the DIKB
# Last Update - 2016-03-29

import os,sys, string, cgi
from time import time, strftime, localtime

import sys
sys.path = sys.path + ['dikb-relational-to-object-mappings']

from mysql_tool import *
from DIKB_Load import load_ev_from_db

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from DIKB.ModelUtils import *
from DIKB.DIKB import *
from DIKB.DrugModel import *
from DIKB.EvidenceModel import *
from DIKB.ExportAssertions import *

timestamp = strftime("%m/%d/%Y %H:%M:%S\n", localtime(time()))

ident = "".join(["Current SQL DIKB evidence : ", timestamp])

### LOAD LATEST EV-BASE AND KB
ev = EvidenceBase("evidence","May2017")
ev.unpickleKB("Drive-Experiment/dikb-pickles/ev-test-two.pickle")

for k,v in ev.objects.iteritems():
    if v.slot == 'substrate_of' and v.value in ['cyp2d6','cyp3a4']:
        for e in v.evidence_for:
            print '\t'.join([v.object, v.slot, v.value, 'EVIDENCE FOR', e.doc_pointer, e.evidence_type.value, 'https://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/dikb-web/' + k + '.html'])
        for e in v.evidence_against:
            print '\t'.join([v.object, v.slot, v.value, 'EVIDENCE AGAINST', e.doc_pointer, e.evidence_type.value, 'https://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/dikb-web/' + k + '.html'])



# print "**************** CYP2D6 substrate evidence **************************"
# for k,v in ev.objects.iteritems():
#     if v.slot == 'substrate_of' and v.value == 'cyp2d6':
#         print 'EVIDENCE RELATED TO ' + v.object
#         for e in v.evidence_for:
#             print 'EVIDENCE FOR:' + '\n'.join([e.doc_pointer, e.evidence_type.value, e.quote])
#         for e in v.evidence_against:
#             print 'EVIDENCE AGAINST:' + '\n'.join([e.doc_pointer, e.evidence_type.value, e.quote])


# print "**************** CYP3A4 substrate evidence **************************"
# for k,v in ev.objects.iteritems():
#     if v.slot == 'substrate_of' and v.value == 'cyp2d6':
#         print 'EVIDENCE RELATED TO ' + v.object
#         for e in v.evidence_for:
#             print 'EVIDENCE FOR:' + '\n'.join([e.doc_pointer, e.evidence_type.value, e.quote])
#         for e in v.evidence_against:
#             print 'EVIDENCE AGAINST:' + '\n'.join([e.doc_pointer, e.evidence_type.value, e.quote])
