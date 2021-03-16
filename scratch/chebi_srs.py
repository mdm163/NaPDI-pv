import sys, time
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
import urllib2
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

## to retrieve from PubMed
from Bio import Entrez

## parse pubmed metadata xml from EUtil
from lxml import etree
from io import StringIO
import urllib
import xml.etree.ElementTree as ElementTree

################################################################################
# Globals
################################################################################


PRE_POST_CHARS=50
mp_list = []

annotationSetCntr = 1
annotationItemCntr = 1
annotationDataCntr = 1
annotationClaimCntr = 1
annotationMaterialCntr = 1
annotationMethodCntr = 1
annotationStatementCntr = 1

xref = 'http://purl.obolibrary.org/obo/database_cross_reference'
#or
xref = 'http://www.geneontology.org/formats/oboInOwl#hasDbXref'

chebiR = {"has_component: RO_0002180", "has_functional_parent: chebi#has_functional_parent", "has_role: RO_0000087", "part_of: BFO_0000050", "in_taxon: RO_0002162"}

## set up RDF graph
# identify namespaces for other ontologies to be used																					 
srs = Namespace()
sio = Namespace('http://semanticscience.org/resource/')
oa = Namespace('http://www.w3.org/ns/oa#')

ncbit = Namespace('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')

rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
obo = Namespace('http://purl.obolibrary.org/obo/')

def initialGraph(graph):
	graph.namespace_manager.reset()
	graph.namespace_manager.bind('obo','http://purl.obolibrary.org/obo/')
	graph.namespace_manager.bind('ncbit','http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')

	#from DIKB ---
	graph.namespace_manager.bind("dcterms", "http://purl.org/dc/terms/")
	graph.namespace_manager.bind("pav", "http://purl.org/pav");
	graph.namespace_manager.bind("dctypes", "http://purl.org/dc/dcmitype/")
	graph.namespace_manager.bind('dailymed','http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/')
	graph.namespace_manager.bind('sio', 'http://semanticscience.org/resource/')
	graph.namespace_manager.bind('oa', 'http://www.w3.org/ns/oa#')
	graph.namespace_manager.bind('aoOld', 'http://purl.org/ao/core/') # needed for AnnotationSet and item until the equivalent is in Open Data Annotation
	graph.namespace_manager.bind('cnt', 'http://www.w3.org/2011/content#')
	graph.namespace_manager.bind('gcds','http://www.genomic-cds.org/ont/genomic-cds.owl#')

	graph.namespace_manager.bind('siocns','http://rdfs.org/sioc/ns#')
	graph.namespace_manager.bind('swande','http://purl.org/swan/1.2/discourse-elements#')
	graph.namespace_manager.bind('dikbD2R','http://dbmi-icode-01.dbmi.pitt.edu/dikb/vocab/resource/')
	graph.namespace_manager.bind('obo','http://purl.obolibrary.org/obo/')


	graph.namespace_manager.bind('linkedspls','file:///home/rdb20/Downloads/d2rq-0.8.1/linkedSPLs-dump.nt#structuredProductLabelMetadata/')
	graph.namespace_manager.bind('poc','http://purl.org/net/nlprepository/spl-ddi-annotation-poc#')
	graph.namespace_manager.bind('ncbit','http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
	graph.namespace_manager.bind('dikbEvidence','http://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/DIKB_evidence_ontology_v1.3.owl#')
	graph.namespace_manager.bind('mp','http://purl.org/mp/')
	graph.namespace_manager.bind('rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#')


	### open annotation ontology properties and classes
	graph.add((dctypes["Collection"], RDFS.label, Literal("Collection"))) # Used in lieau of the AnnotationSet https://code.google.com/p/annotation-ontology/wiki/AnnotationSet
	graph.add((dctypes["Collection"], dcterms["description"], Literal("A collection is described as a group; its parts may also be separately described. See http://dublincore.org/documents/dcmi-type-vocabulary/#H7")))

	graph.add((oa["Annotation"], RDFS.label, Literal("Annotation")))
	graph.add((oa["Annotation"], dcterms["description"], Literal("Typically an Annotation has a single Body (oa:hasBody), which is the comment or other descriptive resource, and a single Target (oa:hasTarget) that the Body is somehow 'about'. The Body provides the information which is annotating the Target. See  http://www.w3.org/ns/oa#Annotation")))

	graph.add((oa["annotatedBy"], RDFS.label, Literal("annotatedBy")))
	graph.add((oa["annotatedBy"], RDF.type, oa["objectproperties"]))

	graph.add((oa["annotatedAt"], RDFS.label, Literal("annotatedAt")))
	graph.add((oa["annotatedAt"], RDF.type, oa["dataproperties"]))

	graph.add((oa["TextQuoteSelector"], RDFS.label, Literal("TextQuoteSelector")))
	graph.add((oa["TextQuoteSelector"], dcterms["description"], Literal("A Selector that describes a textual segment by means of quoting it, plus passages before or after it. See http://www.w3.org/ns/oa#TextQuoteSelector")))

	graph.add((oa["hasSelector"], RDFS.label, Literal("hasSelector")))
	graph.add((oa["hasSelector"], dcterms["description"], Literal("The relationship between a oa:SpecificResource and a oa:Selector. See http://www.w3.org/ns/oa#hasSelector")))

	# these predicates are specific to SPL annotation
	graph.add((sio["SIO_000628"], RDFS.label, Literal("refers to")))
	graph.add((sio["SIO_000628"], dcterms["description"], Literal("refers to is a relation between one entity and the entity that it makes reference to.")))

	graph.add((sio["SIO_000563"], RDFS.label, Literal("describes")))
	graph.add((sio["SIO_000563"], dcterms["description"], Literal("describes is a relation between one entity and another entity that it provides a description (detailed account of)")))

	graph.add((sio["SIO_000338"], RDFS.label, Literal("specifies")))
	graph.add((sio["SIO_000338"], dcterms["description"], Literal("A relation between an information content entity and a product that it (directly/indirectly) specifies")))

def addAssertion(graph, item, currentAnnotationClaim):

	##### OA - EACH SPL HAS A SET OF ANNOTATIONS, EACH WITH A TARGET AND BODY #####
	oaItem = addOAItem(graph, item)

	# Claim : is a research statement label qualified by assertion URI

	if item['researchStatementLabel']:
		graph.add((poc[currentAnnotationClaim], RDFS.label, Literal(item["researchStatementLabel"])))

	# Method : used in data to supports statement
	global annotationMethodCntr
	currentAnnotationMethod = "ddi-spl-annotation-method-%s" % annotationMethodCntr
	annotationMethodCntr += 1	 
	graph.add((poc[currentAnnotationMethod], RDF.type, mp["Method"]))
	graph.add((poc[currentAnnotationMethod], RDF.type, URIRef(item["evidenceType"])))
	graph.add((URIRef(item["evidenceType"]), RDFS.subClassOf, mp["Method"]))

	# Data : supports statement
	global annotationDataCntr
	currentAnnotationData = "ddi-spl-annotation-data-%s" % annotationDataCntr
	annotationDataCntr += 1
	graph.add((poc[currentAnnotationData], RDF.type, mp["Data"]))
	graph.add((poc[currentAnnotationData], RDF.type, URIRef(item["evidenceType"]+"_Data")))
	graph.add((URIRef(item["evidenceType"]+"_Data"), RDFS.subClassOf, mp["Data"]))
		item["mp_evidence"] = currentAnnotationData

	# Material
	global annotationMaterialCntr
	currentAnnotationMaterial = "ddi-spl-annotation-material-%s" % annotationMaterialCntr
	annotationMaterialCntr += 1
	graph.add((poc[currentAnnotationMaterial], RDF.type, mp["Material"])) 
	graph.add((poc[currentAnnotationMaterial], RDF.type, URIRef(item["evidenceType"]+"_Material"))) 
	graph.add((URIRef(item["evidenceType"]+"_Material"), RDFS.subClassOf, mp["Material"])) 


	## increase AUC have PKDDI material info

	if "increases_auc" == item["assertType"].strip():
 
		graph.add((poc[currentAnnotationMaterial], RDFS.label, Literal("%s (object) - %s (precipitant)" % (item["object"], item["precip"]))))

		graph.add((poc[currentAnnotationMaterial], dikbD2R['ObjectDrugOfInteraction'], URIRef(item["objectURI"])))
		graph.add((poc[currentAnnotationMaterial], dikbD2R['PrecipitantDrugOfInteraction'], URIRef(item["preciptURI"])))
		graph.add((poc[currentAnnotationMaterial], dikbD2R['objectDose'], Literal(item["objectDose"])))
		graph.add((poc[currentAnnotationMaterial], dikbD2R['precipitantDose'], Literal(item["precipDose"])))
		graph.add((poc[currentAnnotationMaterial], dikbD2R['numOfSubjects'], Literal(item["numOfSubjects"])))

		# if item["numericVal"]:
		#	  graph.add((poc[currentAnnotationData], dikbD2R["increases_auc"], Literal(item["numericVal"])))
		# else:
		#	  graph.add((poc[currentAnnotationData], dikbD2R["increases_auc"], Literal("stubbed out")))

		if item["evidenceVal"]:
			graph.add((poc[currentAnnotationData], dikbD2R["increases_auc"], Literal(item["evidenceVal"])))
		else:
			graph.add((poc[currentAnnotationData], dikbD2R["increases_auc"], Literal("stubbed out")))


	# Relationships
	graph.add((poc[currentAnnotationMaterial], mp["usedIn"], poc[currentAnnotationMethod]))
	graph.add((poc[currentAnnotationMethod], mp["supports"], poc[currentAnnotationData]))


	if "support" in item["evidenceRole"]:
		graph.add((poc[currentAnnotationData], mp["supports"], poc[currentAnnotationClaim]))
	elif "refute" in item["evidenceRole"]:
		graph.add((poc[currentAnnotationData], mp["challenges"], poc[currentAnnotationClaim]))
	else:
		print "[WARN] evidence typed neither supports nor refutes"

	graph.add((poc[oaItem], oa["hasBody"], poc[currentAnnotationData]))

	graph.add((poc[oaItem], oa["hasBody"], poc[currentAnnotationMethod]))

## create MP graph

def createGraph(graph, dataset):

	assert_claimD = {}

	for item in dataset:   


				drugnameL = getDrugnameInLabel(item["researchStatementLabel"].strip())

				## add new field precipt URI
				item["preciptURI"] = ""

				## skip motabolites
				if "metabolite" in str(item["objectURI"] + item["valueURI"]).lower():
						continue

				## handle wrong URI pair from dikb v1.2
				#if item["objectURI"] == item["valueURI"]:
				#        item["objectURI"] = ""
				#        item["valueURI"] = ""


				## objectURI from old DIKB is preciptURI in DDI, valueURI is objectURI
				## label format: precipt - assertionType - object

				## precipt URI is available in dikb v1.2
				if item["objectURI"]:

						## URI in dikb v1.2 is drugbank URI
						if "www4.wiwiss" in item["objectURI"]:
								preciptDBId = item["objectURI"].replace("http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/","")
								if drugbankIdChEBID.has_key(preciptDBId):
										#print "[DEBUG] find URI %s for precipt %s" % (drugbankIdChEBID[preciptDBId],preciptDBId)
										item["preciptURI"] = drugbankIdChEBID[preciptDBId]
								else:
										print "[WARN] ChEBI for drugbank URI (%s) no found!" % (preciptDBId)
						else:
								item["objectURI"] = item["valueURI"]

				## find ChEBI in mappings of drugname and ChEBI or PRO in mappings of gene name and Pro        
				else:
		
						preciptStr = drugnameL[0].lower()
						if drugnameChEBID.has_key(preciptStr):
								#print "[DEBUG] find URI %s for %s" % (drugnameChEBID[preciptStr],preciptStr)
								item["preciptURI"] = drugnameChEBID[preciptStr]
						elif genenamePROD.has_key(preciptStr):
								#print "[DEBUG] find URI %s for %s" % (genenamePROD[preciptStr],preciptStr)
								item["preciptURI"] = genenamePROD[preciptStr]
						else:
								print "[WARN] asrt (%s) ChEBI for drug (%s) no found!" % (item["asrt"], preciptStr)

				## object URI is available in dikb v1.2
				if item["valueURI"]:

						if "www4.wiwiss" in item["valueURI"]:
								objectDBId = item["valueURI"].replace("http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/","")

								if drugbankIdChEBID.has_key(objectDBId):
										#print "[DEBUG] find URI %s for object %s" % (drugbankIdChEBID[objectDBId],objectDBId)
										item["objectURI"] = drugbankIdChEBID[objectDBId]
								else:
										print "[WARN] ChEBI for drugbank URI (%s) no found!" % (objectDBId)
						else:
								item["objectURI"] = item["valueURI"]

				else:                        
						objectStr = drugnameL[1].lower()
						if drugnameChEBID.has_key(objectStr):
								#print "[DEBUG] find URI %s for %s" % (drugnameChEBID[objectStr],objectStr)
								item["objectURI"] = drugnameChEBID[objectStr]
						elif genenamePROD.has_key(objectStr):
								#print "[DEBUG] find URI %s for %s" % (genenamePROD[objectStr],objectStr)
								item["objectURI"] = genenamePROD[objectStr]
						else:
								print "[WARN] asrt (%s) ChEBI for drug/gene (%s) no found!" % (item["asrt"], objectStr)

				## find wrong URI entities
				if item["preciptURI"] == item["objectURI"]:
						print "[ERROR] asrt (%s), URI wrong for d1 - d2 (%s - %s) (%s - %s)!" % (item["asrt"], drugnameL[0], drugnameL[1], item["preciptURI"], item["objectURI"])
						continue

		referenceId = ""

		if item["evidenceSource"]:
		
			if "pubmed" not in item["evidenceSource"]:
				
				if "resource/structuredProductLabelMetadata" in item["evidenceSource"]:
					referenceId = item["evidenceSource"].replace("http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/resource/structuredProductLabelMetadata/","")
					item["evidenceSource"] = u"http://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=%s" % unicode(referenceId)
				
				if "page/structuredProductLabelMetadata" in item["evidenceSource"]:
					referenceId = item["evidenceSource"].replace("http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/page/structuredProductLabelMetadata/","")
					item["evidenceSource"] = u"http://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=%s" % unicode(referenceId)

			else:
				referenceId = item["evidenceSource"].replace("http://www.ncbi.nlm.nih.gov/pubmed/","")


		###################################################################
		# MP - Claim (label, 3 qualifiedBy for subject, predicate, object)
		###################################################################

		global annotationClaimCntr 
		referenceD = {}

		# Claim : is a research statement label qualified by assertion URI
		if item['researchStatementLabel']:

			# one claim may supported by or refuted by multiple evidences (data/statement)
			if item['researchStatementLabel'] not in assert_claimD.keys():

				#print "[DEBUG] current Claim Cntr:" + str(annotationClaimCntr)

				currentMP = "ddi-spl-annotation-mp-%s" % (annotationClaimCntr)
				graph.add((poc[currentMP],RDF.type, mp["Micropublication"]))

				currentAnnotationClaim = "ddi-spl-annotation-claim-%s" % (annotationClaimCntr)
				annotationClaimCntr += 1

				# mp:Micropublication mp:argues mp:Claim
				graph.add((poc[currentMP], mp["argues"], poc[currentAnnotationClaim]))

				assert_claimD[item['researchStatementLabel']] = currentAnnotationClaim
			else:
				currentAnnotationClaim = assert_claimD[item['researchStatementLabel']]

			graph.add((poc[currentAnnotationClaim],RDF.type, mp["Claim"]))

			graph.add((poc[currentAnnotationClaim], RDFS.label, Literal(item["researchStatementLabel"])))

			# mp:Reference (evidence source URL) mp:supports mp:Claim
			if referenceId and item["evidenceRole"]:

				#if not referenceId:
				#	print "[DEUBG] referenceId: " + referenceId + " | source: " + item["evidenceSource"]

				referenceStr = ""

				if referenceId in referenceD.keys():
					referenceStr = referenceD[referenceId]
				else:
					if "pubmed" in item["evidenceSource"]:
						referenceStr = getPubmedMetaDataByPubmedId(referenceId)
					elif "dailymed" in item["evidenceSource"]:
						referenceStr = getDailymedSPLMetaDataByUrl("http://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=" + referenceId, lsplsparql)

				if referenceStr:
					
					referenceD[referenceId] = referenceStr


					if "support" in item["evidenceRole"]:
						graph.add((URIRef(item["evidenceSource"]), mp["supports"], poc[currentAnnotationClaim]))						
					elif "refute" in item["evidenceRole"]:
						graph.add((URIRef(item["evidenceSource"]), mp["challenges"], poc[currentAnnotationClaim]))

					graph.add((URIRef(item["evidenceSource"]), RDF.type, mp["Reference"]))
					graph.add((URIRef(item["evidenceSource"]), mp["qualifiedBy"], Literal(referenceStr)))

			graph.add((poc[currentAnnotationClaim], mp["qualifiedBy"], URIRef(item["preciptURI"])))
			graph.add((URIRef(item["preciptURI"]), RDF.type, mp["SemanticQualifier"]))

			graph.add((poc[currentAnnotationClaim], mp["qualifiedBy"], URIRef(item["objectURI"])))
			graph.add((URIRef(item["objectURI"]), RDF.type, mp["SemanticQualifier"]))

			## assert type : using dideo URI for inhibits, substrate_of, increase_auc
			if dideoD.has_key(item["assertType"].strip()):
				assertTypeDIDEO = dideoD[item["assertType"].strip()]
				graph.add((poc[currentAnnotationClaim], mp["qualifiedBy"], obo[assertTypeDIDEO]))
				graph.add((obo[assertTypeDIDEO], RDF.type, mp["SemanticQualifier"]))
			else:
				graph.add((poc[currentAnnotationClaim], mp["qualifiedBy"], URIRef(item["assertType"].strip())))
				graph.add((URIRef(item["assertType"]), RDF.type, mp["SemanticQualifier"]))
 
		###################################################################
		# MP - Evidence (Non traceable, Other evidences)
		###################################################################

		## if it's traceble statement
		## multiple bodies - mp:data, mp:Method, mp:Reference, mp:statement, mp:representation

		if item["evidence"]:

			if item["evidenceType"] != u'http://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/DIKB_evidence_ontology_v1.3.owl#Non_traceable_Drug_Label_Statement' and item["evidenceType"] != u'http://dbmi-icode-01.dbmi.pitt.edu/dikb-evidence/DIKB_evidence_ontology_v1.3.owl#Non_Tracable_Statement':
				addAssertion(graph, item, currentAnnotationClaim)

		## The bodies of non_traceable statement is different
		## statement typed as 'Non_traceable_Drug_Label_Statement' don't have evidence
			else:
				addNonTraceable(graph, item, currentAnnotationClaim)

		item["claim"] = currentAnnotationClaim
				item.pop("valueURI", None)
				
		mp_list.append(item)

	############################# QUYERY VALIDATION ###############################

	print "\n#####################TOTAL ITEMS#####################\n"
	print "Claim: %s | Data: %s | Method: %s | Material: %s \n" % (str(annotationClaimCntr - 1), str(annotationDataCntr - 1), str(annotationMethodCntr - 1), str(annotationMaterialCntr - 1))




if __name__ == "__main__":

	## default settings

	OUT_GRAPH = "initial-chebi-srs.xml"
	OUT_CSV = "processed-chebi-srs.tsv"

	if len(sys.argv) > 3:
		numFolds = str(sys.argv[1])
		OUT_GRAPH = str(sys.argv[2])
		OUT_CSV = str(sys.argv[3])
	else:
		print "Usage: dikbv1.2-to-MP-plus-OA.py <number of folds> <output graph> <output csv>"
		sys.exit(1)

	graph = Graph()
	initialGraph(graph)

	createGraphByFold(graph, int(numFolds), OUT_GRAPH, OUT_CSV)

	print "[INFO] create MP graph with %s triples" % str(len(graph))

	printGraphToCSVRDF(mp_list, OUT_GRAPH, OUT_CSV)
