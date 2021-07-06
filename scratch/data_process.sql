--Create tables for data -- DIKB, FDA and DrugCentral

create table staging_data.staging_dikb (
	id serial not null,
	chemical_name varchar(50),
	chemical_id varchar(20),
	protein_name varchar(50),
	protein_id varchar(20),
	relation_name varchar(50),
	relation_type varchar(20),
	relation_id varchar(20),
	evidence_type varchar(20),
	source_type varchar(50),
	source_link varchar(250),
	dikb_link varchar(250)
);

create table staging_data.staging_drugcentral2017 (
	id serial not null,
	chemical_name varchar(50),
	chemical_id varchar(20),
	protein_name varchar(50),
	protein_id varchar(20),
	protein_class varchar(20),
	relation_name varchar(50),
	relation_type varchar(20),
	relation_id varchar(20),
	activity_type varchar(20),
	activity_value integer,
	activity_source varchar(50),
	activity_source_link varchar(250),
	action_type varchar(50)
);

--Set relation names and types based on files (substrate, inhibit, interacts)
update staging_data.staging_drugcentral2017 
set relation_name = 'is_substrate_of', relation_id = 'DIDEO_00000041'
where relation_type = 'substrate_of'

update staging_data.staging_drugcentral2017 
set relation_name = 'inhibits', relation_id = 'RO_0002449'
where relation_type = 'inhibits'

update staging_data.staging_drugcentral2017 
set relation_name = 'molecularly interacts with', relation_id = 'RO_0002436'
where relation_type = 'interacts'

update staging_data.staging_dikb 
set relation_name = 'is_substrate_of', relation_id = 'DIDEO_00000041'
where relation_type = 'substrate_of'

update staging_data.staging_dikb 
set relation_name = 'inhibits', relation_id = 'RO_0002449'
where relation_type = 'inhibits'

--DIKB: Get chemical ID from drug central table where possible
drop table staging_data.mapping_table
create table staging_data.mapping_table (id varchar(20), name varchar(100), type varchar(20));
insert into staging_data.mapping_table
select distinct sd.chemical_id, sd.chemical_name from staging_data.staging_drugcentral2017 sd

select * from staging_data.mapping_table

update staging_data.staging_dikb 
set chemical_id = mp.id 
from staging_data.mapping_table mp
where mp."name" = chemical_name 

select * from staging_data.staging_dikb sd 

--protein strings to concepts in PRO, chemical names to concepts in CHEBI
select distinct sd.protein_name
from staging_data.staging_drugcentral2017 sd 

select distinct sd.protein_name
from staging_data.staging_dikb sd 

select distinct sd.chemical_name 
from staging_data.staging_dikb sd 
where chemical_id is null 
