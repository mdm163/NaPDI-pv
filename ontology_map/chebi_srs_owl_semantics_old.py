## import Sparql-related
from SPARQLWrapper import SPARQLWrapper, JSON
import uuid
## import RDF related
from rdflib import Graph, BNode, Namespace, URIRef, Literal

#import urllib2
#import urllib
#import traceback
#import csv
#import difflib

#not needed in python3
#sys.setdefaultencoding('UTF8')
DIR_OUT = "graphs/"
OUT_GRAPH = DIR_OUT + "chebi-srs-kratom_20210413_sbt.xml"
OUT_CSV = DIR_OUT + "processed-chebi-srs-kratom_20210405.tsv"

urn_dict = {
	'Ne4ee879d723f488db5de2634e498bc71': '7-hydroxy-mitragynine',
	'N96829292877548cb887804ff54db08ab': 'Mitragyna speciosa',
	'Nb8704e8f75e24d05bcd48fb4e861fb04': 'Mitragyna speciosa whole'
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
DC_NS = Namespace('http://purl.org/dc/elements/1.1/')
RDF_NS = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
OBO_NS = Namespace('http://purl.obolibrary.org/obo/')
OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
RDFS_NS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
#RO, BFO, GO CHEBI, NCBITaxon, PRO use the OBO namespace
SRS_NS = Namespace('http://gsrs.ncats.nih.gov/ginas/app/substance/')
LOCAL_NS = Namespace('http://napdi.org/napdi_srs_imports:')

def initialGraph(graph):
	graph.namespace_manager.reset()
	graph.namespace_manager.bind('local_ns', LOCAL_NS)
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

	#Metabolite with cross-ref in SRS is subclass of 'Chemical Entity'
	#Generate UUID/URN for each blank node in diagram
	#Create blank nodes for each restriction placed on the UUID
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDF_NS.type, OWL_NS.Class))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OBO_NS.database_cross_reference, SRS_NS['c50748a1-8231-42ad-a263-6abc6bc49005']))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDFS_NS.label, Literal('7-hydroxy-mitragynine', lang='en')))

	#NP_metabolite has_role 'Metabolite'
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.onProperty, OBO_NS.RO_0000087))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.someValuesFrom, OBO_NS.CHEBI_25212))

	#NP_metabolite has_functional_parent NP_constituent
	

	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.onProperty, OBO_NS['chebi#has_functional_parent']))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.someValuesFrom, OBO_NS.CHEBI_6956))
	
	#NP with cross-ref in SRS
	b = BNode()
	graph.add((LOCAL_NS['mitragyna_speciosa'], RDFS_NS.type, OWL_NS.Class))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OBO_NS.database_cross_reference, SRS_NS['dac1ac7a-f1bb-42d7-ab9c-0bf06d0d9825']))
	graph.add((LOCAL_NS['mitragyna_speciosa'], RDFS_NS.label, Literal('Mitragyna speciosa', lang='en')))
	
	#c = BNode()
	graph.add((LOCAL_NS['mitragyna_speciosa'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.onProperty, OBO_NS.RO_0002162))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.someValuesFrom, OBO_NS.NCBITaxon_170351))

	#NP has_component NP_constituent (in CHEBI)
	#d = BNode()
	graph.add((LOCAL_NS['mitragyna_speciosa'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.someValuesFrom, OBO_NS.CHEBI_6956))
	#metabolism and inhibition entities added as individuals??
	graph.add((OBO_NS.CHEBI_6956, RDFS_NS.type, OWL_NS.Class))
	graph.add((OBO_NS.CHEBI_6956, RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))
	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_008152))
	graph.add((OBO_NS.GO_008152, RDFS_NS.type, OWL_NS.Class))
	graph.add((OBO_NS.GO_008152, OBO_NS.RO_0000057, OBO_NS.PR_P08684))
	
	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_0009892))
	graph.add((OBO_NS.GO_0009892, RDFS_NS.type, OWL_NS.Class))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P08684))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P10635))
	graph.add((OBO_NS.GO_0009892, OBO_NS.RO_0000057, OBO_NS.PR_P11712))

	graph.add((OBO_NS.CHEBI_6956, OBO_NS.RO_0000056, OBO_NS.GO_0032410))
	graph.add((OBO_NS.GO_0032410, RDFS_NS.type, OWL_NS.Class))
	graph.add((OBO_NS.GO_0032410, OBO_NS.RO_0000057, OBO_NS.PR_P000001891))
	
	#NP has_component NP_constituent (not in CHEBI, cross-ref in SRS) [role, subclass, cross-ref already defined above]
	#f = BNode()

	graph.add((LOCAL_NS['mitragyna_speciosa'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.onProperty, OBO_NS.RO_0002180))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.someValuesFrom, LOCAL_NS['7_hydroxy_mitragynine']))

	#g = BNode()

	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.onProperty, OBO_NS.RO_0000056))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.someValuesFrom, OBO_NS.GO_008152))

	#h = BNode()
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.onProperty, OBO_NS.RO_0000056))
	graph.add((LOCAL_NS['7_hydroxy_mitragynine'], OWL_NS.someValuesFrom, OBO_NS.GO_0032410))
	#NP part_of NP_parent
	#e = BNode()
	c = BNode()

	graph.add((LOCAL_NS['mitragyna_speciosa'], RDF_NS.type, OWL_NS.Restriction))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.onProperty, OBO_NS.BFO_0000050))
	graph.add((LOCAL_NS['mitragyna_speciosa'], OWL_NS.someValuesFrom, LOCAL_NS['mitragyna_speciosa_whole']))

	#NP_Parent with cross-ref in SRS 
	graph.add((LOCAL_NS['mitragyna_speciosa_whole'], RDFS_NS.type, OWL_NS.Class))
	graph.add((LOCAL_NS['mitragyna_speciosa_whole'], RDFS_NS.subClassOf, OWL_NS.Thing))
	graph.add((LOCAL_NS['mitragyna_speciosa_whole'], OBO_NS.database_cross_reference, SRS_NS['d469b67d-e9a6-459f-b209-c59451936336']))
	graph.add((LOCAL_NS['mitragyna_speciosa_whole'], RDFS_NS.label, Literal('Mitragyna speciosa whole', lang='en')))
	

	f = open(OUT_GRAPH,"w")
	graph_str = graph.serialize(format='xml').decode('utf-8')
	f.write(graph_str)
	f.close()

	graph.close()
