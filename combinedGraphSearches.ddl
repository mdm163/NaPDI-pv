
-- DDL and LOAD SQL that goes with the SPARQL output from extraction graph searches and
-- the output from processing the PheKnowLator searches

DROP SCHEMA IF EXISTS pheknowlator_paths CASCADE;
CREATE SCHEMA pheknowlator_paths;

set search_path to pheknowlator_paths;

DROP TABLE IF EXISTS cui_to_omop;
CREATE TABLE cui_to_omop (
	id serial,
	cui varchar NOT NULL,
	sab varchar NOT NULL,
	code varchar NOT NULL,
	concept_id bigint NOT NULL,
	vocabulary_id varchar NOT NULL,
	concept_code varchar NOT NULL
);

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into cui_to_omop from file '
\copy cui_to_omop (cui,sab,code,concept_id,vocabulary_id,concept_code) from 'cui-to-omop-map-partial.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;

DROP TABLE IF EXISTS cui_to_obo;
CREATE TABLE cui_to_obo (
	id serial,
	cui varchar NOT NULL,
	eg_uri varchar NOT NULL,
	obo varchar NOT NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into cui_to_obo from file '
\copy cui_to_obo (cui,eg_uri,obo) from 'CUI-to-OBO.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;


DROP TABLE IF EXISTS extraction_colliders;
CREATE TABLE extraction_colliders (
	id serial,
	expl varchar NOT NULL,
	s_lab varchar NOT NULL,
	s_obo varchar NOT NULL,
	s varchar NOT NULL,
	s_semType varchar NOT NULL,
	p1 varchar NOT NULL,
	p1_lab varchar NOT NULL,
	o_lab varchar NOT NULL,
	o_obo varchar NOT NULL,
	o varchar NOT NULL,
	o_semType varchar NOT NULL,
	p2 varchar NOT NULL,
	p2_lab varchar NOT NULL,
	g1 varchar NOT NULL,
	g2 varchar NOT NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into extraction_colliders'
\copy extraction_colliders (expl,s_lab,s_obo,s,s_semType,p1,p1_lab,o_lab,o_obo,o,o_semType,p2,p2_lab,g1,g2) from 'adColliderSearch/depression-ad-colliders-120220.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;



DROP TABLE IF EXISTS extraction_mediators;
CREATE TABLE extraction_mediators (
	id serial,
	expl varchar NOT NULL,
	s_lab varchar NOT NULL,
	s_obo varchar NOT NULL,
	s varchar NOT NULL,
	s_semType varchar NOT NULL,
	p1 varchar NOT NULL,
	p1_lab varchar NOT NULL,
	o_lab varchar NOT NULL,
	o_obo varchar NOT NULL,
	o varchar NOT NULL,
	o_semType varchar NOT NULL,
	p2 varchar NOT NULL,
	p2_lab varchar NOT NULL,
	g1 varchar NOT NULL,
	g2 varchar NOT NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into extraction_mediators'
\copy extraction_mediators (expl,s_lab,s_obo,s,s_semType,p1,p1_lab,o_lab,o_obo,o,o_semType,p2,p2_lab,g1,g2) from 'adMediatorSearch/depression-ad-mediators-120220.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;

DROP TABLE IF EXISTS extraction_confounders;
CREATE TABLE extraction_confounders (
	id serial,
	expl varchar NOT NULL,
	s_lab varchar NOT NULL,
	s_obo varchar NOT NULL,
	s varchar NOT NULL,
	s_semType varchar NOT NULL,
	p1 varchar NOT NULL,
	p1_lab varchar NOT NULL,
	o_lab varchar NOT NULL,
	o_obo varchar NOT NULL,
	o varchar NOT NULL,
	o_semType varchar NOT NULL,
	p2 varchar NOT NULL,
	p2_lab varchar NOT NULL,
	g1 varchar NOT NULL,
	g2 varchar NOT NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into extraction_confounders'
\copy extraction_confounders (expl,s_lab,s_obo,s,s_semType,p1,p1_lab,o_lab,o_obo,o,o_semType,p2,p2_lab,g1,g2) from 'adConfounderSearch/depression-ad-confounders-120220.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;


DROP TABLE IF EXISTS collider_paths;
CREATE TABLE collider_paths (
	id serial,
	path_type varchar NULL,
	path_start varchar NULL,
	path_end varchar NULL,
	path_count int4 NULL,
	path_step int4 NULL,
	subject_label varchar NULL,
	predicate_label varchar NULL,
	object_label varchar NULL,
	subject_uri varchar NULL,
	predicate_uri varchar NULL,
	object_uri varchar NULL,
	source_file varchar NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into collider_paths'
\copy collider_paths (path_type, path_start, path_end, path_count, path_step, subject_label, predicate_label, object_label, subject_uri, predicate_uri, object_uri, source_file) from 'adColliderSearch/aggregated-output/MR-and-lit-review-DEPRESSION-collider-set-relational.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;

DROP TABLE IF EXISTS mediator_paths;
CREATE TABLE mediator_paths (
	id serial,
	path_type varchar NULL,
	path_start varchar NULL,
	path_end varchar NULL,
	path_count int4 NULL,
	path_step int4 NULL,
	subject_label varchar NULL,
	predicate_label varchar NULL,
	object_label varchar NULL,
	subject_uri varchar NULL,
	predicate_uri varchar NULL,
	object_uri varchar NULL,
	source_file varchar NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into mediator_paths'
\copy mediator_paths (path_type, path_start, path_end, path_count, path_step, subject_label, predicate_label, object_label, subject_uri, predicate_uri, object_uri, source_file) from 'adMediatorSearch/aggregated-output/MR-and-lit-review-DEPRESSION-mediator-set-relational.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;


DROP TABLE IF EXISTS confounder_paths;
CREATE TABLE confounder_paths (
	id serial,
	path_type varchar NULL,
	path_start varchar NULL,
	path_end varchar NULL,
	path_count int4 NULL,
	path_step int4 NULL,
	subject_label varchar NULL,
	predicate_label varchar NULL,
	object_label varchar NULL,
	subject_uri varchar NULL,
	predicate_uri varchar NULL,
	object_uri varchar NULL,
	source_file varchar NULL
);
\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into confounder_paths'
\copy confounder_paths (path_type, path_start, path_end, path_count, path_step, subject_label, predicate_label, object_label, subject_uri, predicate_uri, object_uri, source_file) from 'adConfounderSearch/aggregated-output/MR-and-lit-review-DEPRESSION-confounder-set-relational.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;
