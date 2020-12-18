#!/usr/bin/python3

## pathOutputToRDB.py -- convert the output of find path searches over
## PheKnowLator to a table that can be loaded into an relational DB
##
## Checked for counts by comparing:
##  grep "INFO: Processing " <INFILE> | wc -l:
## to the sum of:
##  egrep "     0       1       " <OUTFILE>  | wc -l
##  grep "No results" <INFILE> | wc -l
##  grep "INFO: skipping" <INFILE> | wc -l
##

### DDL and LOAD SQL that goes with this script

# -- DROP SCHEMA pheknowlator_paths;
# CREATE SCHEMA pheknowlator_paths 

# -- pheknowlator_paths.collider_paths definition

# -- Drop table

# -- DROP TABLE pheknowlator_paths.collider_paths;
# CREATE TABLE pheknowlator_paths.collider_paths (
# 	id int4 NULL,
# 	path_type varchar NULL,
# 	path_start varchar NULL,
# 	path_end varchar NULL,
# 	path_count int4 NULL,
# 	path_step int4 NULL,
# 	subject_label varchar NULL,
# 	predicate_label varchar NULL,
# 	object_label varchar NULL,
# 	subject_uri varchar NULL,
# 	predicate_uri varchar NULL,
# 	object_uri varchar NULL,
# 	source_file varchar NULL
# );

# -- DROP TABLE pheknowlator_paths.confounder_paths;
# CREATE TABLE pheknowlator_paths.confounder_paths (
# 	id int4 NULL,
# 	path_type varchar NULL,
# 	path_start varchar NULL,
# 	path_end varchar NULL,
# 	path_count int4 NULL,
# 	path_step int4 NULL,
# 	subject_label varchar NULL,
# 	predicate_label varchar NULL,
# 	object_label varchar NULL,
# 	subject_uri varchar NULL,
# 	predicate_uri varchar NULL,
# 	object_uri varchar NULL,
# 	source_file varchar NULL
# );

# -- DROP TABLE pheknowlator_paths.mediator_paths;
# CREATE TABLE pheknowlator_paths.mediator_paths (
# 	id int4 NULL,
# 	path_type varchar NULL,
# 	path_start varchar NULL,
# 	path_end varchar NULL,
# 	path_count int4 NULL,
# 	path_step int4 NULL,
# 	subject_label varchar NULL,
# 	predicate_label varchar NULL,
# 	object_label varchar NULL,
# 	subject_uri varchar NULL,
# 	predicate_uri varchar NULL,
# 	object_uri varchar NULL,
# 	source_file varchar NULL
# );

import sys, getopt
from subprocess import check_output


##
def main(argv):
    help_str = ''''pathOutputToRDB.py -t path type (some label so you can distinguish the type of path); -f input file of paths found in PheKnowLator (see below for expected format); -o output file path for relational data formatted paths; -m output file path for the list of paths not found in PheKnowLator

        Input file formatting example - note that this script uses the comment formatting to identify the start and end of paths. Also, each path step is tab delimitted:

INFO: Processing http://purl.obolibrary.org/obo/CHEBI_15843 and http://purl.obolibrary.org/obo/HP_0000716:


INFO: PATH 0:
arachidonic acid	participates in	Developmental Biology	http://purl.obolibrary.org/obo/CHEBI_15843	http://purl.obolibrary.org/obo/RO_0000056	https://reactome.org/content/detail/R-HSA-1266738
Developmental Biology	has participant	DUSP6	https://reactome.org/content/detail/R-HSA-1266738	http://purl.obolibrary.org/obo/RO_0000057	https://www.ncbi.nlm.nih.gov/gene/1848
DUSP6	causes or contributes to condition	Depressivity	https://www.ncbi.nlm.nih.gov/gene/1848	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0000716




INFO: PATH 1:
arachidonic acid	participates in	Signaling by GPCR	http://purl.obolibrary.org/obo/CHEBI_15843	http://purl.obolibrary.org/obo/RO_0000056	https://reactome.org/content/detail/R-HSA-372790
Signaling by GPCR	has participant	DUSP6	https://reactome.org/content/detail/R-HSA-372790	http://purl.obolibrary.org/obo/RO_0000057	https://www.ncbi.nlm.nih.gov/gene/1848
DUSP6	causes or contributes to condition	Depressivity	https://www.ncbi.nlm.nih.gov/gene/1848	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0000716

....


INFO: Processing http://purl.obolibrary.org/obo/CHEBI_15843 and http://purl.obolibrary.org/obo/HP_0002511:


INFO: PATH 0:
arachidonic acid	participates in	Developmental Biology	http://purl.obolibrary.org/obo/CHEBI_15843	http://purl.obolibrary.org/obo/RO_0000056	https://reactome.org/content/detail/R-HSA-1266738
Developmental Biology	has participant	PRNP	https://reactome.org/content/detail/R-HSA-1266738	http://purl.obolibrary.org/obo/RO_0000057	https://www.ncbi.nlm.nih.gov/gene/5621
PRNP	causes or contributes to condition	Alzheimer disease	https://www.ncbi.nlm.nih.gov/gene/5621	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0002511




INFO: PATH 1:
arachidonic acid	participates in	Developmental Biology	http://purl.obolibrary.org/obo/CHEBI_15843	http://purl.obolibrary.org/obo/RO_0000056	https://reactome.org/content/detail/R-HSA-1266738
Developmental Biology	has participant	DPYSL2	https://reactome.org/content/detail/R-HSA-1266738	http://purl.obolibrary.org/obo/RO_0000057	https://www.ncbi.nlm.nih.gov/gene/1808
DPYSL2	causes or contributes to condition	Alzheimer disease	https://www.ncbi.nlm.nih.gov/gene/1808	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0002511

....

INFO: skipping common cause to  AD path search because it is present in the processed_tpl_cache - please look earlier in the output file for the following statement: INFO: Processing http://purl.obolibrary.org/obo/HP_0000716 and http://purl.obolibrary.org/obo/DOID_10652:
INFO: Processing http://purl.obolibrary.org/obo/CHEBI_16113 and http://purl.obolibrary.org/obo/HP_0000716:


INFO: PATH 0:
cholesterol	participates in	Immune System	http://purl.obolibrary.org/obo/CHEBI_16113	http://purl.obolibrary.org/obo/RO_0000056	https://reactome.org/content/detail/R-HSA-168256
Immune System	has participant	POMC	https://reactome.org/content/detail/R-HSA-168256	http://purl.obolibrary.org/obo/RO_0000057	https://www.ncbi.nlm.nih.gov/gene/5443
POMC	causes or contributes to condition	Depressivity	https://www.ncbi.nlm.nih.gov/gene/5443	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0000716

....

INFO: Processing http://purl.obolibrary.org/obo/PR_O42145 and http://purl.obolibrary.org/obo/HP_0000716:
INFO: The source node does not exist in the Knowledge Graph.

INFO: Processing http://www.ebi.ac.uk/efo/EFO_0001073 and http://purl.obolibrary.org/obo/HP_0000716:
INFO: No results in the path search.


INFO: Processing http://purl.obolibrary.org/obo/VO_0000811 and http://purl.obolibrary.org/obo/HP_0002511:


INFO: PATH 0:
epitope	subClassOf	antigen	http://purl.obolibrary.org/obo/VO_0000811	http://www.w3.org/2000/01/rdf-schema#subClassOf	http://purl.obolibrary.org/obo/OBI_1110034
antigen	has role	antigen role	http://purl.obolibrary.org/obo/OBI_1110034	http://purl.obolibrary.org/obo/RO_0000087	http://purl.obolibrary.org/obo/OBI_0000237
antigen role	realized in	immune response	http://purl.obolibrary.org/obo/OBI_0000237	http://purl.obolibrary.org/obo/BFO_0000054	http://purl.obolibrary.org/obo/GO_0006955
immune response	molecularly interacts with	bortezomib	http://purl.obolibrary.org/obo/GO_0006955	http://purl.obolibrary.org/obo/RO_0002436	http://purl.obolibrary.org/obo/CHEBI_52717
bortezomib	interacts with	SOD2	http://purl.obolibrary.org/obo/CHEBI_52717	http://purl.obolibrary.org/obo/RO_0002434	https://www.ncbi.nlm.nih.gov/gene/6648
SOD2	causes or contributes to condition	Alzheimer disease	https://www.ncbi.nlm.nih.gov/gene/6648	http://purl.obolibrary.org/obo/RO_0003302	http://purl.obolibrary.org/obo/HP_0002511


...

'''
    
    try:
        opts, args = getopt.getopt(argv, 'ht:f:o:m:', ['pathtype=','inputfile=', 'outputfile=','missingfile='])
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
   
    for opt, arg in opts:
      if opt == '-h':
         print(help_str)
         sys.exit()

      elif opt in ("-t", "--inputfile"):
         PATH_TYPE = arg
         
      elif opt in ("-f", "--inputfile"):
         INFILE = arg

      elif opt in ("-o", "--outputfile"):
         OUTFILE = arg

      elif opt in ("-m", "--missingfile"):
         NOT_PATH_OUTFILE = arg

    print('Path Type:{}\nInfile:{}\nOutfile:{}\nMissingfile:{}\n\n'.format(PATH_TYPE, INFILE, OUTFILE, NOT_PATH_OUTFILE))
    
    f = open(INFILE,'r')
    lines = f.readlines()
    f.close()

    not_path_l = []
    header_l = ['PATH_TYPE','PATH_START','PATH_END','PATH_COUNT','PATH_STEP','SUBJECT_LABEL','PREDICATE_LABEL','OBJECT_LABEL','SUBJECT_URI','PREDICATE_URI','OBJECT_URI','SOURCE_FILE']
    records_l = []

    path_batch_start = ""
    path_start = ""
    path_l = []
    path_end = ""

    for l in lines:    
    # print"line: " + l)
    # print"path_batch_start: {}, path_start: {}, length path_l: {}, path_end: {}".format(path_batch_start, path_start, len(path_l), path_end))
    
        if l == "\n" or l.find("INFO: skipping") >= 0:
            # print("skip")
            continue
        else:
            l = l.strip('\n')

        if (not path_batch_start) and l.find("INFO: Processing") >= 0:
            # print("starting path batch")
            path_batch_start = l        
            continue

        if path_batch_start and l == "INFO: No results in the path search.":
            # print("appending no path result")
            not_path_l.append(path_batch_start)
            path_batch_start = ""
            path_start = ""
            path_l = []
            path_end = ""
            continue   

        if path_batch_start and (not path_start) and l.find("INFO: PATH ") >= 0:
            # print("found path: " + l)
            path_start = l
            continue

        if path_batch_start and path_start and len(path_l) >= 0 and (not ((l.find("INFO: skipping") >= 0) or (l.find("INFO: PATH ") >= 0 or l.find("INFO: Processing") >= 0))):
            # print("adding step")
            path_l.append(l)

        elif path_batch_start and path_start and len(path_l) > 0 and ((l.find("INFO: skipping") >= 0) or l.find("INFO: PATH ") >= 0 or l.find("INFO: Processing") >= 0):
            # print("found end of path, saving and starting new. path_l: {}".format(path_l))
            for step in range(0,len(path_l)):
                # print("append")
                (start_uri,end_uri) = path_batch_start.strip(":").strip(":\n").replace("INFO: Processing ","").split(" and ")
                path_cnt = int(path_start.strip(":\n").replace("INFO: PATH ",""))
                records_l.append([PATH_TYPE, start_uri, end_uri, path_cnt, step+1] + path_l[step].split('\t') + [INFILE])
             
            if l.find("INFO: PATH ") >= 0:
                # print("path start found: " + l)
                path_start = l
                path_l = []
                path_end = ""
            
            elif l.find("INFO: Processing") >= 0:
                # print("New path batch start: " + l)
                path_batch_start = l
                path_start = ""
                path_l = []
                path_end = ""

            elif l.find("INFO: skipping") >= 0:
                # print("Skipped record: " + l)
                path_batch_start = l
                path_start = ""
                path_l = []
                path_end = ""

    # print'Writing output')
    outf = open(OUTFILE,'w')
    outf.write("\t".join(header_l) + "\n")
    for r in records_l:
        outf.write("\t".join([str(x) for x in r]) + "\n")
    outf.close()

    outf = open(NOT_PATH_OUTFILE,'w')
    outf.write("\n".join(not_path_l))
    outf.close()

    return(INFILE,OUTFILE)


if __name__ == "__main__":
    (INFILE, OUTFILE) = main(sys.argv[1:])

    print(INFILE)

    pairs_total = -1
    pairs_processed = -1
    no_results = -1
    skipped = -1
    no_source_node = -1
    
    output=check_output("grep 'INFO: Processing ' {}  | wc -l".format(INFILE), shell=True)
    if output:
        pairs_total = int(str(output).replace('\\n','').replace('b','').replace("'",''))
       
    output=check_output("egrep '\t0\t1\t' {}  | wc -l".format(OUTFILE), shell=True)
    if output:
        pairs_processed  = int(str(output).replace('\\n','').replace('b','').replace("'",''))

    output=check_output("grep 'No results' {}  | wc -l".format(INFILE), shell=True)
    if output:
        no_results  = int(str(output).replace('\\n','').replace('b','').replace("'",''))
       
    output=check_output("grep 'INFO: skipping ' {}  | wc -l".format(INFILE), shell=True)
    if output:
        skipped  = int(str(output).replace('\\n','').replace('b','').replace("'",''))

    output=check_output("grep 'INFO: The source node does not exist in the Knowledge Graph.' {}  | wc -l".format(INFILE), shell=True)
    if output:
        no_source_node  = int(str(output).replace('\\n','').replace('b','').replace("'",''))


    if pairs_total == -1 or pairs_processed == -1 or no_results == -1 or skipped == -1 or no_source_node == -1:
        print("ERROR: Unable to do quality checks - something is wrong with the script or the file paths passed to the script.")
    else:
        print("INFO: Test if the process accounted for all paths. Does the number of lines to process in the input file ({}) equal the sum of those lines processed ({}), no results ({}), skipped ({}), and no source node in KB ({}) [{} = {}]? {} ".format(pairs_total, pairs_processed, no_results, skipped,  no_source_node, pairs_total, pairs_processed + no_results + skipped + no_source_node, pairs_total == pairs_processed + no_results + skipped + no_source_node ))

    

   