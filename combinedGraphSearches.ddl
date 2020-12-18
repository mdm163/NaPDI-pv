
-- DDL and LOAD SQL that goes with the SPARQL output from processing the PheKnowLator searches

DROP SCHEMA IF EXISTS napdi_paths CASCADE;
CREATE SCHEMA napdi_paths;

set search_path to napdi_paths;

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


DROP TABLE IF EXISTS mitragynine_paths;
CREATE TABLE mitragynine_paths (
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
\echo 'Loading data into mitragynine_paths'
\copy mitragynine_paths (path_type, path_start, path_end, path_count, path_step, subject_label, predicate_label, object_label, subject_uri, predicate_uri, object_uri, source_file) from 'firstKGTests/aggregated-output/PKG-paths-mitragynine-to-drug-to-AE-clean.tsv' DELIMITER E'\t' NULL '\\N' CSV HEADER;
COMMIT;
