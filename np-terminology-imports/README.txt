The input file for NapDI project concepts is np-custom-terms.csv

This process assumes that you have reserved (-9999999, -7000000) for
custome concept ids. The script will create the concept ids as it
generates the insert statements. The assumption is that you will
delete all custom concepts and re-run the entire process every time
you add or modify the custome concepts. This is important because, if
you don't completely replace the concepts every time, you will get
identifier issues.

START: IF you are rerunning this, use these queries to delete the
       existing custom concepts. If you ever need to change the range of concepts
       edit the range in the python script and uncomment the line in the main method
       to generate the delete queries.

--- RUN AS SUPER USER ON THE DATABASE OF INTEREST
alter table staging_vocabulary.concept disable trigger all;
alter table staging_vocabulary.vocabulary disable trigger all;
alter table staging_vocabulary.domain  disable trigger all;
alter table staging_vocabulary.concept_class disable trigger all;

DELETE FROM staging_vocabulary.concept cascade WHERE concept_id BETWEEN -9999999 AND -7000000 ;
DELETE FROM staging_vocabulary.vocabulary cascade WHERE vocabulary_concept_id BETWEEN -9999999 AND -7000000 ;
DELETE FROM staging_vocabulary.domain cascade WHERE domain_concept_id BETWEEN -9999999 AND -7000000 ;
DELETE FROM staging_vocabulary.concept_class cascade WHERE concept_class_concept_id BETWEEN -9999999 AND -7000000 ;

alter table staging_vocabulary.concept enable trigger all;
alter table staging_vocabulary.vocabulary enable trigger all;
alter table staging_vocabulary.domain  enable trigger all;
alter table staging_vocabulary.concept_class enable trigger all;

--

1) Add/Edit concepts in the input file - the input file needs to be a tab separated file with unix line feeds. The first column of the rows needs to be a URL with the concept code following the name of the vocabulary (e.g., http://blah.org/VOCAB_0001). The script will split on the term at the end of the URL and then split on the '_' to get the vocabulary id and the concept code for the concept (e.g., VOCAB and 0001).

2) Edit the global variables in generateConceptsInsertSQL.py

3) python2.7 generateConceptsInsertSQL.py

4) Use the output SQL to insert the new custom concepts


--

Use this to create the mapping from common name to latin binomial to SRS:

cut -f1,3,4 np-custom-terms.tsv | sort | uniq > common-name-to-LB-to-SRS-map.tsv
