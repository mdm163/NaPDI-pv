-- simple example
select distinct cp.*
from mitragynine_paths cp 
order by cp.path_start, cp.path_end, cp.path_count, cp.path_step 
;


--- qeutiapine - hypothermia 
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_8707'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0002045'
order by cp.path_count
;

--- mitragynine to quetiapine
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_8707'
order by cp.path_count
;


----------



--- qeutiapine - seizure
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_8707'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0001250'
order by cp.path_count
;

--- mitragynine to quetiapine
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_8707'
order by cp.path_count
;


-------

--- diphenhydramine - Pulmonary oedema

--- 
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_4636'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0100598'
order by cp.path_count
;

--- mitragynine to diphenhydramine 
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_4636'
order by cp.path_count
;



-------

--- valproate - seizure
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_60654'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0001250'
order by cp.path_count
;

--- mitragynine to valproate
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_60654'
order by cp.path_count
;


-------


--- valproate - hypothermia
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_60654'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0002045'
order by cp.path_count
;

--- mitragynine to valproate
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_60654'
order by cp.path_count
;

-------



--- mirtazapine - Pulmonary oedema
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6950'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0100598'
order by cp.path_count
;

--- mitragynine to mirtazapine
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_6950'
order by cp.path_count
;


-------


--- ethanol - Pulmonary oedema
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_16236'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0100598'
order by cp.path_count
;

--- mitragynine to ethanol
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_16236'
order by cp.path_count
;


---------


--- ethanol - Urinary retention
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_16236'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0000016'
order by cp.path_count
;

--- mitragynine to ethanol
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_16236'
order by cp.path_count
;


----------


--- diphenhydramine - Urinary retention
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_4636'
 and path_end = 'http://purl.obolibrary.org/obo/HP_0000016'
order by cp.path_count
;

--- mitragynine to diphenhydramine 
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_4636'
order by cp.path_count
;

-----------


--- diphenhydramine - Pulmonary congestion  (NO PATH)
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_4636'
 and path_end = 'http://purl.obolibrary.org/obo/MP_0010018'
order by cp.path_count
;


--- mitragynine to diphenhydramine 
select distinct cp.*
from mitragynine_paths cp
where path_start = 'http://purl.obolibrary.org/obo/CHEBI_6956'
 and path_end = 'http://purl.obolibrary.org/obo/CHEBI_4636'
order by cp.path_count
;



---------------
