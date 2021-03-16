import sys, time
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
# import urllib2
import urllib
import traceback
import csv
import difflib

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

## import Sparql-related
from SPARQLWrapper import SPARQLWrapper, JSON

## import RDF related
from rdflib import Graph, BNode, Literal, Namespace, URIRef, RDF, RDFS, XSD

OUT_GRAPH = "initial-chebi-srs.xml"
OUT_CSV = "processed-chebi-srs.tsv"


XREF = 'http://purl.obolibrary.org/obo/database_cross_reference'
#or
# xref = 'http://www.geneontology.org/formats/oboInOwl#hasDbXref'

CHEBI_RO = {"has_component: RO_0002180", "has_functional_parent: chebi#has_functional_parent", "has_role: RO_0000087", "part_of: BFO_0000050", "in_taxon: RO_0002162"}

## set up RDF graph
# identify namespaces for other ontologies to be used															  			 
RDF_NS = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
OBO_NS = Namespace('http://purl.obolibrary.org/obo/')
GO_NS = Namespace('http://purl.obolibrary.org/obo/go.owl/')
OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
RDFS_NS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
RO_NS = ....

def initialGraph(graph):
	graph.namespace_manager.reset()
	graph.namespace_manager.bind('obo', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
	graph.namespace_manager.bind('rdf', 'http://purl.obolibrary.org/obo/')
        graph.namespace_manager.bind('go','http://purl.obolibrary.org/obo/go.owl/')
        graph.namespace_manager.bind('owl','http://www.w3.org/2002/07/owl#')
        graph.namespace_manager.bind('rdfs','http://www.w3.org/2000/01/rdf-schema#')
# TODO: add qnames 
        
        #graph.namespace_manager.bind('','')
        
def addAssertion(graph, item)
	# graph.add((poc[currentAnnotationMaterial], RDF.type, mp["Material"])) 

if __name__ == "__main__":

	## default settings

	graph = Graph()
	initialGraph(graph)

        graph.add((OBO_NS.CHEBI_6956, RDF_NS.subClassOf, OBO_NS.CHEBI_24331))

        bn1 = BNode()
        graph.add((bn1, '<http://purl.obolibrary.org/obo/chebi#has_functional_parent>', OBO_NS.CHEBI_6956))

        graph.add((bn1, , ))

        graph.add(( , , ))

        graph.add(( , , ))
        # graph.add(( , , ))


        f = codecs.open(OUT_GRAPH,"w","utf8")
	s = graph.serialize(format="xml",encoding="utf8")
	f.write(unicode(s,errors='replace'))
	f.close

	graph.close()
