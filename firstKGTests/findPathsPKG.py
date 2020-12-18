## find shortest paths for colliders
import os
import os.path
import networkx as nx
import json
import urllib
import traceback
import sys
import pickle
from itertools import islice
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, OWL

GRAPHPATH = "/home/rdb20/PheKnowLator/resources/knowledge_graphs/created-owl-nets-inverse-relations/PheKnowLator_full_InverseRelations_NotClosed_OWLNETS_Networkx_MultiDiGraph_REWEIGHT_NO_DISJOINT.gpickle"

NODE_LABEL_PATH = "/home/rdb20/PheKnowLator/resources/knowledge_graphs/created-owl-nets-inverse-relations/PheKnowLator_full_InverseRelations_NotClosed_NoOWLSemantics_NodeLabels.txt"

OUTFILE = 'PKG-paths-mitragynine-to-drug-to-AE.txt'

LABEL_CACHE_PATH = '/home/rdb20/PheKnowLator/resources/knowledge_graphs/created-owl-nets-inverse-relations/label_cache_napdi_test_run.pickle'

MAXNUMPATHS = 5 # NOTE: after running at 20 max paths for about 30 tuples, reduced to 5 to speed up processing

########
pheknowlator_service = "http://130.49.206.139:8890/sparql"
ontobee_service = "http://sparql.hegroup.org/sparql/"

## a subset of drug - outcome pairs from queries of kratom FAERS reports resulting in death
## SQL Query:
#  with  unnested_drugs_narrow as (
#  select caseid d_caseid, 
#         unnest(string_to_array(standard_drug_name,';')) drug_name, 
#         unnest(string_to_array(drug_concept_id,';')) drug_concept_id
#  from scratch_rich.kratom_reports kr 
#  where kr.standard_outcome_code like '%DE%'
# ), unnested_outcomes as (
#  select caseid o_caseid,
#         unnest(string_to_array(standard_outcome_name,';')) outcome_names, 
#         unnest(string_to_array(outcome_concept_id,';')) outcome_concept_id,
#         unnest(string_to_array(snomed_outcome_concept_id,';')) outcome_snomed
#  from scratch_rich.kratom_reports kr 
#  where kr.standard_outcome_code like '%DE%'
# ), drugs_and_outcomes as (
#   select * from unnested_drugs_narrow d inner join unnested_outcomes o on d.d_caseid = o.o_caseid
# )
# select drug_name, outcome_names, count(distinct d_caseid) cnt 
# from drugs_and_outcomes
# -- where outcome_names not in ('Death','Accidental death','Unresponsive to stimuli','Discharge','Toxicity to various agents','Drug interaction')
# group by drug_name, outcome_names
# order by cnt desc
# ;
####
## SQL Query results (partial)
# diphenhydramine	Toxicity to various agents	20
# oxycodone	Toxicity to various agents	18
# morphine	Toxicity to various agents	13
# alprazolam	Toxicity to various agents	13
# bupropion	Toxicity to various agents	13
# paroxetine	Toxicity to various agents	12
# quetiapine	Toxicity to various agents	12
# mirtazapine	Toxicity to various agents	11
# diphenhydramine	Pulmonary oedema	10
# quetiapine	Seizure	9
# venlafaxine	Toxicity to various agents	9
# valproate	Toxicity to various agents	9
# lorazepam	Toxicity to various agents	9
# quetiapine	Drug interaction	9
# valproate	Seizure	8
# quetiapine	Hyperthermia	8
# fluoxetine	Toxicity to various agents	8
# valproate	Drug interaction	8
# valproate	Hyperthermia	7
# zolpidem	Toxicity to various agents	7
# diphenhydramine	Unresponsive to stimuli	7
# oxycodone	Death	7
# etizolam	Death	6
# methadone	Toxicity to various agents	6
# citalopram	Toxicity to various agents	6
# oxycodone	Accidental death	6
# gabapentin	Toxicity to various agents	6
# tramadol	Toxicity to various agents	6
# oxycodone	Unresponsive to stimuli	6
# heroin	Toxicity to various agents	6
# ethanol	Toxicity to various agents	6
# morphine	Unresponsive to stimuli	6
# hydroxyzine	Toxicity to various agents	5
# mirtazapine	Pulmonary oedema	5
# ethanol	Pulmonary oedema	5
# ethanol	Urinary retention	5
# sertraline	Death	5
# clonazepam	Toxicity to various agents	5
# diphenhydramine	Urinary retention	5
# fentanyl	Toxicity to various agents	5
# venlafaxine	Urinary retention	5
# diphenhydramine	Pulmonary congestion	5
# fluoxetine	Pulmonary oedema	5

s_o_tpl_L = [
    ('http://purl.obolibrary.org/obo/CHEBI_8707','http://purl.obolibrary.org/obo/HP_0001250'), # qeutiapine - seizure
    ('http://purl.obolibrary.org/obo/CHEBI_4636','http://purl.obolibrary.org/obo/HP_0100598'), # diphenhydramine - Pulmonary oedema
    ('http://purl.obolibrary.org/obo/CHEBI_60654','http://purl.obolibrary.org/obo/HP_0001250'), # valproate - seizure
    ('http://purl.obolibrary.org/obo/CHEBI_60654','http://purl.obolibrary.org/obo/HP_0002045'), #  valproate - hypothermia
    ('http://purl.obolibrary.org/obo/CHEBI_8707','http://purl.obolibrary.org/obo/HP_0002045'), #  qeutiapine - hypothermia
    ('http://purl.obolibrary.org/obo/CHEBI_6950','http://purl.obolibrary.org/obo/HP_0100598'), # mirtazapine - Pulmonary oedema
    ('http://purl.obolibrary.org/obo/CHEBI_16236','http://purl.obolibrary.org/obo/HP_0100598'), # ethanol - Pulmonary oedema
    ('http://purl.obolibrary.org/obo/CHEBI_16236','http://purl.obolibrary.org/obo/HP_0000016'), # ethanol - Urinary retention
    ('http://purl.obolibrary.org/obo/CHEBI_4636','http://purl.obolibrary.org/obo/HP_0000016'), # diphenhydramine - Urinary retention
    ('http://purl.obolibrary.org/obo/CHEBI_4636','http://purl.obolibrary.org/obo/MP_0010018') # diphenhydramine - Pulmonary congestion    
]

## Leave as None unless you have to restart this cell before it has completely processed all tuples.
## Otherwise, replace this tuple with the first tuple to process completely by the program 
FIRST_TO_PROCESS =  None

kratom_obo = 'http://purl.obolibrary.org/obo/CHEBI_6956'

########

# Reloading this version of the graph -- NOTE: if running interactively, you need to re-import networkx and the RDFLib stuff first
nx_mdg = nx.read_gpickle(GRAPHPATH)

# Obtain the node labels (rdsf:label) that had been stripped from the graph
nodeLabD = {}

## Reloading any previously cached node labels returned from Ontobee queries
try:
    f = open(LABEL_CACHE_PATH,'rb')
    labelCacheD = pickle.load(f)
    f.close()
    for k,v in labelCacheD.items():
        nodeLabD[k] = v
except FileNotFoundError:
    print('WARNING: Unable to reload any previously cached node labels returned from Ontobee queries. A new file will be created at {}.'.format(LABEL_CACHE_PATH))
    pass

## Reloading from one of the PheKnowLator OWl NETS output files 
f = open(NODE_LABEL_PATH,'r')
buf = f.read()
f.close()
nodLabL = buf.split('\n')
for line in nodLabL:
    spL = line.split('\t')
    if len(spL) > 1:
        nodeLabD[spL[0]] = spL[1]

def query(q,epr,f='application/sparql-results+json'):
    """Function that uses urllib/urllib2 to issue a SPARQL query.
       By default it requests json as data format for the SPARQL resultset"""

    try:
        params = {'query': q}
        params = urllib.parse.urlencode(params)
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        request = urllib.request.Request(epr+'?'+params)
        request.add_header('Accept', f)
        request.get_method = lambda: 'GET'
        url = opener.open(request)
        return url.read()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e
        
def pathQuery(pth):
    """Given a single path (list of rdflib objects), run a sparql query to retrieve descriptive information 
       that will help construct a narrative explanation"""
    
    uriL = [x.toPython() for x in filter(lambda x: type(x) == URIRef, pth)]
    subjectStr = ''
    objectStr = ''
    for uri in uriL:
        subjectStr = subjectStr + '?s = <' + uri + '> || '
        objectStr = objectStr + '?o = <' + uri + '> || '
    subjectStr = subjectStr[:-3] # ?s = <..> || ?s = <...>... the URIs for the subject/object entities in the path
    objectStr = objectStr[:-3] # ?o = <..> || ?o = <...>... the URIs for the subject/object entities in the path
   
    q = '''
  prefix obo:<http://purl.obolibrary.org/obo/>
  prefix owl:<http://www.w3.org/2002/07/owl#>
 
  select distinct ?s ?p ?o ?p_lab ?s_lab_eg ?o_lab_eg
  from <http://pheknowlator.org>
  from <ro_with_imports_AD_mods>
  where {{
    ?s ?p ?o.FILTER(({}) && ({})) 
    OPTIONAL{{
     ?p rdfs:label ?p_lab.
   }}
   OPTIONAL{{
     ?egM_s <http://dikb.org/ad#obo_mapping> ?s.
     ?egM_s rdfs:label ?s_lab_eg.
   }}
   OPTIONAL{{
     ?egM_o <http://dikb.org/ad#obo_mapping> ?o.
     ?egM_o rdfs:label ?o_lab_eg.
   }}
  }}
'''.format(subjectStr,objectStr)
    
    return q

def missingLabelQuery(uri, endpoint):
    query_string = '''
SELECT distinct ?lab
WHERE {{ 
 <{}> rdfs:label ?lab. 
}}
'''.format(uri)
    json_string = query(query_string, endpoint)
    resultset = json.loads(json_string)
    rsltsD = {}
    for b in resultset["results"]["bindings"]:
        if not b.get('lab'):
            return None
        
        label = b['lab']['value']
        if label:
            return label
        else:
            return None

def constructPathNarData(pth, sparql_service):
    """ Iterate through the path to organize a narrative
        in: pth - a list of rdflib URIRef and BNode objects
        in: sparql_service - URL to the sparql endpoint
    """
    query_string = pathQuery(pth)
    json_string = query(query_string, pheknowlator_service)
    resultset = json.loads(json_string)
    print("[INFO] Number of results: " + str(len(resultset["results"]["bindings"])))
    
    # Re-organize the results set to be a dict keyed by the subject uri
    rsltsD = {}
    for b in resultset["results"]["bindings"]:
        s = b['s']['value']
        if rsltsD.get(s):
            rsltsD[s].append(b)
        else:
            rsltsD[s] = [b]
    
    narrative = ""    
    for i in range(0,len(pth)):
        if i == len(pth) - 1:
            break
        
        n1 = pth[i]
        n2 = pth[i+1]
    
        if not (type(n1) == URIRef and type(n2) == URIRef):
            narrative += "----- BLANK NODE STEP ----"
            continue
        else:
            # locate the results dict that relates n1 to n2 in a subject, predicate, object triple
            o_d = None
            for d in rsltsD.get(n1.toPython()):
                if d['o']['value'] == n2.toPython():
                    o_d = d
                    break
        
            if not o_d:
                print("ERROR: Unable to find a triple relating {} to {} in path {}".format(n1.toPython(),n2.toPython(),pth))
            else:
                o_lab = '<no label found>'
                o_node_id = o_d['o']['value'].split('/')[-1]
                if nodeLabD.get(o_node_id):
                    o_lab = nodeLabD[o_node_id]
                else:
                    if label_cache.get(o_d['o']['value']):
                        o_lab = label_cache[o_d['o']['value']]
                    else:
                        ql = missingLabelQuery(o_d['o']['value'],ontobee_service)
                        if ql:
                            label_cache[o_d['o']['value']] = ql
                            o_lab = ql
                    
                    if o_lab == '<no label found>' and o_d.get('o_lab_eg'):
                        o_lab = o_d['o_lab_eg']['value'] + ' (UMLS label)'

                s_lab = '<no label found>'
                s_node_id = o_d['s']['value'].split('/')[-1]
                if nodeLabD.get(s_node_id):
                    s_lab = nodeLabD[s_node_id]
                else:
                    if label_cache.get(o_d['s']['value']):
                        s_lab = label_cache[o_d['s']['value']]
                    else:
                        ql = missingLabelQuery(o_d['s']['value'],ontobee_service)
                        if ql:
                            label_cache[o_d['s']['value']] = ql
                            s_lab = ql  
                    
                    if s_lab == '<no label found>' and o_d.get('s_lab_eg'):
                        s_lab = o_d['s_lab_eg']['value'] + ' (UMLS label)'

                if o_d.get('p_lab'):                      
                    narrative += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                            s_lab,o_d['p_lab']['value'],o_lab,
                            o_d['s']['value'],o_d['p']['value'],o_d['o']['value']
                           )                          
                else:
                    narrative += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                            s_lab,o_d['p']['value'].replace('http://www.w3.org/2000/01/rdf-schema#',''),o_lab,
                            o_d['s']['value'],o_d['p']['value'],o_d['o']['value']
                           )                                          
    return narrative

def k_shortest_paths(G, source, target, k, weight='weight'):
    return list(islice(nx.all_shortest_paths(G, source, target, weight=weight), k))

###############

maxNumPaths = MAXNUMPATHS

f = open(OUTFILE, 'w')

# this is used because there is allot of repetition
processed_tpl_cache = []

# queried label cache
label_cache = {}

for tpl in s_o_tpl_L:
    #i += 1
    #if i == 3:
    #    break
    
    if FIRST_TO_PROCESS:
        if str(tpl) != str(FIRST_TO_PROCESS):
            f.write('INFO: skipping tuple because it is not FIRST_TO_PROCESS:' + str(tpl))
            continue
        else:
            FIRST_TO_PROCESS = None
    
    (s,o) = tpl    
    
    # kratom to drug involved in AE report
    startNd = URIRef(kratom_obo)
    endNd = URIRef(s) 
    f.write('INFO: Processing {} and {}:\n'.format(kratom_obo,s))
       
    pathL = []
    try:
        pthL = k_shortest_paths(nx_mdg,startNd,endNd,maxNumPaths)
    except nx.NetworkXNoPath:
        f.write('INFO: No results in the path search.\n')
        continue
    except nx.NodeNotFound:
        f.write('INFO: The source node does not exist in the Knowledge Graph.\n')
        continue

    narL = []
    c = -1
    for path in pthL:
        c += 1
        nar = constructPathNarData(path, pheknowlator_service)
        f.write('\n\nINFO: PATH {}:\n'.format(c))
        f.write(nar)
        f.write('\n\n')
    
    # drug involved in the kratom AE report  to adverse event       
    startNd = URIRef(s) 
    endNd = URIRef(o) 
        
    if tpl in processed_tpl_cache:
        f.write('INFO: skipping search because it is present in the processed_tpl_cache - please look earlier in the output file for the following statement: INFO: Processing {} and {}:\n'.format(s,o))
        continue
    else:
        processed_tpl_cache.append(tpl)
        
    f.write('INFO: Processing {} and {}:\n'.format(startNd,endNd))
                
    try:
        pthL = k_shortest_paths(nx_mdg,startNd,endNd,maxNumPaths)
    except nx.NetworkXNoPath:
        f.write('INFO: No results in the path search.\n')
        continue
    except nx.NodeNotFound:
        f.write('INFO: The source node does not exist in the Knowledge Graph.\n')
        continue

    narL = []
    c = -1
    for path in pthL:
        c += 1
        nar = constructPathNarData(path,pheknowlator_service)
        f.write('\n\nINFO: PATH {}:\n'.format(c))
        f.write(nar)
        f.write('\n\n')
f.close()

f = open(LABEL_CACHE_PATH,'wb')
pickle.dump(label_cache, f)
f.close()
