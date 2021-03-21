## import Sparql-related
from SPARQLWrapper import SPARQLWrapper, JSON

## import RDF related
from rdflib import Graph, BNode, Namespace, URIRef

# import urllib2
#import urllib
#import traceback
#import csv
#import difflib

#not needed in python3
#sys.setdefaultencoding('UTF8')
OUT_GRAPH = "initial-chebi-srs.xml"
OUT_CSV = "processed-chebi-srs.tsv"

relations = {
"has_component" : "RO_0002180", 
"has_functional_parent": "chebi#has_functional_parent", 
"has_role": "RO_0000087", 
"part_of": "BFO_0000050", 
"in_taxon": "RO_0002162"}
XREF = URIRef('http://www.geneontology.org/formats/oboInOwl#DbXref')
## set up RDF graph
# identify namespaces for other ontologies to be used															  			 
RDF_NS = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
OBO_NS = Namespace('http://purl.obolibrary.org/obo/')
GO_NS = Namespace('http://purl.obolibrary.org/obo/go.owl/')
OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
RDFS_NS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
#RO, BFO, CHEBI, NCBITaxon use the OBO namespace
SRS_NS = Namespace('http://gsrs.ncats.nih.gov/ginas/app/substance/')

def initialGraph(graph):
	graph.namespace_manager.reset()
	graph.namespace_manager.bind('obo', OBO_NS)
	graph.namespace_manager.bind('rdf', RDF_NS)
	graph.namespace_manager.bind('go', GO_NS)
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

	graph.add((OBO_NS.CHEBI_6956, RDF_NS.subClassOf, OBO_NS.CHEBI_24331))
	#green blank node in figure
	bn1 = BNode()
	graph.add((bn1, URIRef('http://purl.obolibrary.org/obo/chebi#has_functional_parent'), OBO_NS.CHEBI_6956))
	graph.add((bn1, OBO_NS.RO_0000087, OBO_NS.CHEBI_25212))
	graph.add((bn1, RDF_NS.subClassOf, OBO_NS.CHEBI_24331))
	graph.add((bn1, OBO_NS.database_cross_reference, SRS_NS['c50748a1-8231-42ad-a263-6abc6bc49005']))
	
	#orange blank nodes
	bn2 = BNode()
	bn3 = BNode()
	graph.add((bn2, OBO_NS.RO_0002180, OBO_NS.CHEBI_6956))
	graph.add((bn2, OBO_NS.BFO_0000050, bn3))
	graph.add((bn2, XREF, SRS_NS['dac1ac7a-f1bb-42d7-ab9c-0bf06d0d9825']))
	graph.add((bn2, OBO_NS.RO_0002162, OBO_NS.NCBITaxon_170351))
	graph.add((bn3, XREF, SRS_NS['d469b67d-e9a6-459f-b209-c59451936336']))
	
	# graph.add(( , , ))

	f = open(OUT_GRAPH,"w")
	graph_str = graph.serialize(format='xml').decode('utf-8')
	f.write(graph_str)
	f.close()

	graph.close()
