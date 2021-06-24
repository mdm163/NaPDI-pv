---- Useful to see the kind of things we can query --

-- Of interest: Bacteria, Enzyme, Transporter
select distinct target_class
FROM act_table_full atf
order by target_class 
;

-- of interest for enzyme inhibition: app Ki, Ki, IC50
-- of interest for transport inhibition: EC50, EC90
-- of interest for enzyme metabolism: :  app Km, Km
select distinct act_type 
FROM act_table_full atf
order by act_type
;

----------

--- drug-bacteria interactions from drug central
with struct_ids as (
  SELECT DISTINCT struct_id
  FROM identifier i 
  WHERE id_type = 'DRUGBANK_ID' 
)
select distinct atf.struct_id, atc.chemical_substance, identifier.identifier chebi_id, target_name, target_class, act_type activity_type, act_value, act_unit, act_source, act_source_url, action_type
-- select * 
FROM act_table_full atf 
   inner join struct2atc s2atc on atf.struct_id = s2atc.struct_id 
   inner join atc on s2atc.atc_code = atc.code
   inner join identifier on atf.struct_id = identifier.struct_id
WHERE atf.struct_id in (select struct_id from struct_ids)
  and target_class = 'Bacteria'
  and identifier.parent_match is null
  and identifier.id_type  = 'CHEBI'
ORDER BY target_name
;



-- in vitro drug enzyme inhibition data from drug central
with struct_ids as (
  SELECT DISTINCT struct_id
  FROM identifier i 
  WHERE id_type = 'DRUGBANK_ID' 
)
select distinct atf.struct_id, atc.chemical_substance, identifier.identifier chebi_id, target_name, target_class, act_type activity_type, act_value, act_unit, act_source, act_source_url, action_type
-- select * 
FROM act_table_full atf 
   inner join struct2atc s2atc on atf.struct_id = s2atc.struct_id 
   inner join atc on s2atc.atc_code = atc.code
   inner join identifier on atf.struct_id = identifier.struct_id
WHERE atf.struct_id in (select struct_id from struct_ids)
  and target_class = 'Enzyme' and (target_name LIKE 'Cytochrome P450%' or target_name ILIKE '%Glucuronosyl%')
  and act_type in ('app Ki', 'Ki', 'IC50')
  and identifier.parent_match is null
  and identifier.id_type  = 'CHEBI'
ORDER BY target_name
;


-- in vitro drug transporter inhibition data from drug central
with struct_ids as (
  SELECT DISTINCT struct_id
  FROM identifier i 
  WHERE id_type = 'DRUGBANK_ID' 
)
select distinct atf.struct_id, atc.chemical_substance, identifier.identifier chebi_id, target_name, target_class, act_type activity_type, act_value, act_unit, act_source, act_source_url, action_type
-- select * 
FROM act_table_full atf 
   inner join struct2atc s2atc on atf.struct_id = s2atc.struct_id 
   inner join atc on s2atc.atc_code = atc.code
   inner join identifier on atf.struct_id = identifier.struct_id
WHERE atf.struct_id in (select struct_id from struct_ids)
  and target_class = 'Transporter'  
  and act_type in ('EC50', 'EC90')
  and identifier.parent_match is null
  and identifier.id_type  = 'CHEBI'
ORDER BY target_name
;


----------
-- in vitro drug substrate data from drug central
with struct_ids as (
  SELECT DISTINCT struct_id
  FROM identifier i 
  WHERE id_type = 'DRUGBANK_ID' 
)
SELECT atf.struct_id, atc.chemical_substance, identifier.identifier chebi_id, target_name, target_class,  act_type activity_type, act_value, act_unit, act_source, act_source_url, action_type
FROM act_table_full atf 
   inner join struct2atc s2atc on atf.struct_id = s2atc.struct_id 
   inner join atc on s2atc.atc_code = atc.code
   inner join identifier on atf.struct_id = identifier.struct_id
WHERE atf.struct_id in (select struct_id from struct_ids)
  and target_class = 'Enzyme' and (target_name LIKE 'Cytochrome P450%' or target_name ILIKE '%Glucuronosyl%') 
  and act_type in ('app Km','Km')
  and identifier.parent_match is null
  and identifier.id_type  = 'CHEBI'
ORDER BY target_name
;

--- 
