## import Sparql-related
from SPARQLWrapper import SPARQLWrapper, JSON
import uuid
## import RDF related
from rdflib import Graph, BNode, Namespace, URIRef, Literal
import json
#import urllib2
#import urllib
#import traceback
#import csv
#import difflib

#not needed in python3
#sys.setdefaultencoding('UTF8')
DIR_OUT = "graphs/"
OUT_GRAPH = DIR_OUT + "chebi-srs-20210413.xml"
OUT_CSV = DIR_OUT + "processed-chebi-srs-20210408.tsv"

urn_dict = {
	'7-hydroxy-mitragynine': 'http://napdi.org/napdi_srs_imports:7_hydroxy_mitragynine',  # could we use hyphens?
	'Mitragyna_speciosa': 'http://napdi.org/napdi_srs_imports:mitragyna_speciosa',
	'Mitragyna_speciosa_whole' :'http://napdi.org/napdi_srs_imports:mitragyna_speciosa_whole',
	'Goldenseal': 'http://napdi.org/napdi_srs_imports:goldenseal',
	'Hydrastis_canadensis_whole': 'http://napdi.org/napdi_srs_imports:hydrastis_canadensis_whole'
}

relations = {
"has_component" : "RO_0002180", 
"has_functional_parent": "chebi#has_functional_parent", 
"has_role": "RO_0000087", 
"part_of": "BFO_0000050", 
"in_taxon": "RO_0002162",
"has_participant": "RO_0000057",
"participates_in": "RO_0000056"}
XREF = URIRef('http://www.geneontology.org/formats/oboInOwl#DbXref')

## set up RDF graph
# identify namespaces for other ontologies to be used
LOCAL_NS = Namespace('http://napdi.org/napdi_srs_imports:')
DC_NS = Namespace('http://purl.org/dc/elements/1.1/')
RDF_NS = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
OBO_NS = Namespace('http://purl.obolibrary.org/obo/')
OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
RDFS_NS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
#RO, BFO, GO CHEBI, NCBITaxon, PRO use the OBO namespace
SRS_NS = Namespace('http://gsrs.ncats.nih.gov/ginas/app/substance/')

def create_urn(string_literal):
	uuid_new = uuid.uuid4().hex
	urn_dict[string_literal] = 'urn:'+uuid_new

def initialGraph(graph):
	graph.namespace_manager.reset()
	graph.namespace_manager.bind('napdi_srs', LOCAL_NS)
	graph.namespace_manager.bind('dc', DC_NS)
	graph.namespace_manager.bind('obo', OBO_NS)
	graph.namespace_manager.bind('rdf', RDF_NS)
	graph.namespace_manager.bind('owl', OWL_NS)
	graph.namespace_manager.bind('rdfs', RDFS_NS)
	graph.namespace_manager.bind('srs', SRS_NS)
# TODO: add qnames 
	
	#graph.namespace_manager.bind('','')
	
#def addAssertion(graph, item)
	# graph.add((poc[currentAnnotationMaterial], RDF.type, mp["Material"])) 

if __name__ == "__main__":

	## default settings

	graph = Graph()
	initialGraph(graph)
		
	# Ontology - about and imports
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), RDF_NS.type, OWL_NS.Ontology))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, URIRef('http://purl.obolibrary.org/obo/iao/2017-03-24/iao.owl')))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, URIRef('http://purl.obolibrary.org/obo/bfo/2014-05-03/classes-only.owl')))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, URIRef('http://purl.obolibrary.org/obo/ro/core.owl')))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), DC_NS.creator, Literal('Sanya B. Taneja', lang='en')))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), DC_NS.contributor, Literal('Richard D. Boyce', lang='en')))
	graph.add((URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), RDFS_NS.label, Literal('NaPDI SRS imported entities', lang='en'))) # need to find how to specify XSD type lang=en

	#NP with cross-ref in SRS
	# graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.subClassOf, OWL_NS.Class))
	##GOLDENSEAL
	graph.add((URIRef(urn_dict['Goldenseal']), OBO_NS.database_cross_reference, SRS_NS['acd31728-eac3-4005-a80f-aae4689f9eab']))
	graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.label, Literal('Goldenseal', lang='en')))

	#NP part_of NP_parent
	gs_a = BNode()
	graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.subClassOf, gs_a))
	graph.add((gs_a, RDF_NS.type, OWL_NS.Restriction))
	graph.add((gs_a, OWL_NS.onProperty, OBO_NS.BFO_0000050))
	graph.add((gs_a, OWL_NS.someValuesFrom, URIRef(urn_dict['Hydrastis_canadensis_whole'])))

	#NP_Parent with cross-ref in SRS 
	#graph.add((URIRef(urn_dict['Hydrastis_canadensis_whole']), RDFS_NS.subClassOf, OWL_NS.Class))
	#graph.add((URIRef(urn_dict['Hydrastis_canadensis_whole']), RDFS_NS.subClassOf, OWL_NS.Thing))
	graph.add((URIRef(urn_dict['Hydrastis_canadensis_whole']), OBO_NS.database_cross_reference, SRS_NS['66690655-f406-4d67-96e3-2066aafee8d5']))
	graph.add((URIRef(urn_dict['Hydrastis_canadensis_whole']), RDFS_NS.label, Literal('Hydrastis canadensis whole', lang='en')))

	#NP (extract) participate in inhibition
	gs_b = BNode()
	graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.subClassOf, gs_b))
	graph.add((gs_b, RDF_NS.type, OWL_NS.Restriction))
	graph.add((gs_b, OWL_NS.onProperty, OBO_NS.RO_0000056))
	graph.add((gs_b, OWL_NS.someValuesFrom, OBO_NS.GO_0009892))
	#graph.add((OBO_NS.GO_0009892, RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P10635))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P08684))

	##NP has_component NP_constituent (in CHEBI)
	gs_c = BNode()
	graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.subClassOf, gs_c))
	graph.add((gs_c, RDF_NS.type, OWL_NS.Restriction))
	graph.add((gs_c, OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((gs_c, OWL_NS.someValuesFrom, OBO_NS.CHEBI_16118))

	#metabolism and inhibition entities as classes
	#graph.add((OBO_NS.CHEBI_16118, RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((OBO_NS.CHEBI_16118, RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((OBO_NS.CHEBI_16118, OBO_NS.RO_0000056, OBO_NS.GO_0009892))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P11712))

	graph.add((OBO_NS.CHEBI_16118, OBO_NS.RO_0000056, OBO_NS.GO_0032410))
	#OCT2 (SLC22A2), BCRP (ABCG2), ABCB1
	#graph.add((OBO_NS.GO_0032410, OBO_NS.RO_0000057, OBO_NS.))

	gs_d = BNode()
	graph.add((URIRef(urn_dict['Goldenseal']), RDFS_NS.subClassOf, gs_d))
	graph.add((gs_d, RDF_NS.type, OWL_NS.Restriction))
	graph.add((gs_d, OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((gs_d, OWL_NS.someValuesFrom, OBO_NS.CHEBI_69919))

	#graph.add((OBO_NS.CHEBI_69919, RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((OBO_NS.CHEBI_69919, RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((OBO_NS.CHEBI_69919, OBO_NS.RO_0000056, OBO_NS.GO_0009892))

	#Metabolite with cross-ref in SRS is subclass of 'Chemical Entity'
	# graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), OBO_NS.database_cross_reference, SRS_NS['c50748a1-8231-42ad-a263-6abc6bc49005']))
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.label, Literal('7-hydroxy-mitragynine', lang='en')))

	#NP_metabolite has_role 'Metabolite'
	a = BNode()
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, a))
	graph.add((a, RDF_NS.type, OWL_NS.Restriction))
	graph.add((a, OWL_NS.onProperty, OBO_NS.RO_0000087))
	graph.add((a, OWL_NS.someValuesFrom, OBO_NS.CHEBI_25212))

	#NP_metabolite has_functional_parent NP_constituent
	b = BNode()
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, b))
	graph.add((b, RDF_NS.type, OWL_NS.Restriction))
	graph.add((b, OWL_NS.onProperty, OBO_NS['chebi#has_functional_parent']))
	graph.add((b, OWL_NS.someValuesFrom, OBO_NS.CHEBI_6956))
	
	#NP with cross-ref in SRS
	#graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.type, OWL_NS.Class))
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), OBO_NS.database_cross_reference, SRS_NS['dac1ac7a-f1bb-42d7-ab9c-0bf06d0d9825']))
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.label, Literal('Mitragyna speciosa', lang='en')))
	
	c = BNode()
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.subClassOf, c))
	graph.add((c, RDF_NS.type, OWL_NS.Restriction))
	graph.add((c, OWL_NS.onProperty, OBO_NS.RO_0002162))
	graph.add((c, OWL_NS.someValuesFrom, OBO_NS.NCBITaxon_170351))

	#NP has_component NP_constituent (in CHEBI)
	d = BNode()
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.subClassOf, d))
	graph.add((d, RDF_NS.type, OWL_NS.Restriction))
	graph.add((d, OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((d, OWL_NS.someValuesFrom, OBO_NS.CHEBI_6956))
	#metabolism and inhibition entities added as classes
	#graph.add((OBO_NS.CHEBI_6956, RDFS_NS.type, OWL_NS.Class))
	graph.add((OBO_NS.CHEBI_6956, RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_008152))
	#graph.add((OBO_NS.GO_008152, RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((OBO_NS.GO_008152, OBO_NS.RO_0000057, OBO_NS.PR_P08684))
	
	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_0009892))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P08684))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P10635))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P11712))

	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_0032410))
	#graph.add((OBO_NS.GO_0032410, RDFS_NS.subClassOf, OWL_NS.Class))
	graph.add((OBO_NS.GO_0032410, OBO_NS.RO_0000057, OBO_NS.PR_P000001891))
	
	#NP has_component NP_constituent (not in CHEBI, cross-ref in SRS) [role, subclass, cross-ref already defined above]
	f = BNode()
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.subClassOf, f))
	graph.add((f, RDF_NS.type, OWL_NS.Restriction))
	graph.add((f, OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((f, OWL_NS.someValuesFrom, URIRef(urn_dict['7-hydroxy-mitragynine'])))

	g = BNode()
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, g))
	graph.add((g, RDF_NS.type, OWL_NS.Restriction))
	graph.add((g, OWL_NS.onProperty, OBO_NS.RO_0000056))
	graph.add((g, OWL_NS.someValuesFrom, OBO_NS.GO_008152))

	h = BNode()
	graph.add((URIRef(urn_dict['7-hydroxy-mitragynine']), RDFS_NS.subClassOf, g))
	graph.add((h, RDF_NS.type, OWL_NS.Restriction))
	graph.add((h, OWL_NS.onProperty, OBO_NS.RO_0000056))
	graph.add((h, OWL_NS.someValuesFrom, OBO_NS.GO_0032410))

	#NP part_of NP_parent
	e = BNode()
	graph.add((URIRef(urn_dict['Mitragyna_speciosa']), RDFS_NS.subClassOf, e))
	graph.add((e, RDF_NS.type, OWL_NS.Restriction))
	graph.add((e, OWL_NS.onProperty, OBO_NS.BFO_0000050))
	graph.add((e, OWL_NS.someValuesFrom, URIRef(urn_dict['Mitragyna_speciosa_whole'])))

	#NP_Parent with cross-ref in SRS 
	#graph.add((URIRef(urn_dict['Mitragyna_speciosa_whole']), RDFS_NS.type, OWL_NS.Class))
	#graph.add((URIRef(urn_dict['Mitragyna_speciosa_whole']), RDFS_NS.subClassOf, OWL_NS.Thing))
	graph.add((URIRef(urn_dict['Mitragyna_speciosa_whole']), OBO_NS.database_cross_reference, SRS_NS['d469b67d-e9a6-459f-b209-c59451936336']))
	graph.add((URIRef(urn_dict['Mitragyna_speciosa_whole']), RDFS_NS.label, Literal('Mitragyna speciosa whole', lang='en')))
	

	f = open(OUT_GRAPH,"w")
	graph_str = graph.serialize(format='xml').decode('utf-8')
	f.write(graph_str)
	f.close()

	graph.close()
