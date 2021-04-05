## import Sparql-related
from SPARQLWrapper import SPARQLWrapper, JSON

## import RDF related
import rdflib
from rdflib import Graph, BNode, Namespace, URIRef, Literal

#import urllib2
#import urllib
#import traceback
#import csv
#import difflib

#not needed in python3
#sys.setdefaultencoding('UTF8')
OUT_GRAPH = "initial-chebi-srs-kratom_20200405.xml"
OUT_CSV = "processed-chebi-srs-kratom_20200405.tsv"

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

def initialGraph(graph):
	graph.namespace_manager.reset()
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
        
	# Ontology
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), RDF_NS.type, OWL_NS.Ontology))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, rdflib.URIRef('http://purl.obolibrary.org/obo/iao/2017-03-24/iao.owl')))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, rdflib.URIRef('http://purl.obolibrary.org/obo/bfo/2014-05-03/classes-only.owl')))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), OWL_NS.imports, rdflib.URIRef('http://purl.obolibrary.org/obo/ro/core.owl')))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), DC_NS.creator, Literal('Sanya B. Taneja', lang='en')))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), DC_NS.contributor, Literal('Richard D. Boyce', lang='en')))
	graph.add((rdflib.URIRef('http://purl.obolibrary.org/obo/napdi-srs-imports'), RDFS_NS.label, Literal('NaPDI SRS imported entities', lang='en'))) # need to find how to specify XSD type lang=en

	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), RDF_NS.type, OWL_NS.Class))
	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), RDFS_NS.subClassOf, OBO_NS.CHEBI_24431))

	a = BNode()
	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), RDFS_NS.subClassOf, a))
	graph.add((a, RDF_NS.type, OWL_NS.Restriction))
	graph.add((a, OWL_NS.onProperty, OBO_NS.RO_0000087))
	graph.add((a, OWL_NS.someValuesFrom, OBO_NS.CHEBI_25212))

	b = BNode()
	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), RDFS_NS.subClassOf, b))
	graph.add((b, RDF_NS.type, OWL_NS.Restriction))
	graph.add((b, OWL_NS.onProperty, OBO_NS['chebi#has_functional_parent']))
	graph.add((b, OWL_NS.someValuesFrom, OBO_NS.CHEBI_6956))
	
	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), OBO_NS.database_cross_reference, SRS_NS['c50748a1-8231-42ad-a263-6abc6bc49005']))

	graph.add((rdflib.URIRef('urn:Ne4ee879d723f488db5de2634e498bc71'), RDFS_NS.label, Literal('7-hydroxy-mitragynine', lang='en')))

	f = open(OUT_GRAPH,"w")
	graph_str = graph.serialize(format='xml').decode('utf-8')
	f.write(graph_str)
	f.close()

	graph.close()
