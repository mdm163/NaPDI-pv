
select distinct tsn."name", tsn.substance_uuid, tsn.organism_family, tsn.organism_genus, tsn.organism_species, igc.code, regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_sanya.test_srs_np tsn on igc.owner_uuid = tsn.substance_uuid 
where igc.code_system = 'DSLD' 
union 
select distinct tsnp."name", tsnp.substance_uuid, tsnp.organism_family, tsnp.organism_genus, tsnp.organism_species, igc.code, regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_sanya.test_srs_np_parent tsnp on igc.owner_uuid = tsnp.substance_uuid 
where igc.code_system = 'DSLD'
union 
select distinct tsnp."name", tsnp.substance_uuid, tsnp.organism_family, tsnp.organism_genus, tsnp.organism_species, igc.code, regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_sanya.test_srs_np_part tsnp on igc.owner_uuid = tsnp.substance_uuid 
where igc.code_system = 'DSLD'

select * from ix_ginas_code igc
where igc.code_system  = 'DSLD'
limit 100

with subs_ref as (
select igs.uuid as ref_uuid_part, igs.refuuid as ref_uuid_parent from ix_ginas_substanceref igs 
where igs.refuuid in (select tsn2.substance_uuid from scratch_sanya.test_srs_np tsn2)
)
select tsn.substance_uuid, tsn3.organism_family, tsn3.organism_genus, tsn3.organism_species 
from scratch_sanya.test_srs_np_part tsn 
where tsn.parent_substance_uuid in (select ref_uuid_part from subs_ref)



select distinct tsn.substance_uuid, tsn2.organism_family, tsn2.organism_genus, tsn2.organism_species, igc.code, regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from scratch_sanya.test_srs_np_part tsn 
inner join ix_ginas_code igc on igc.owner_uuid = tsn.substance_uuid 
inner join 
where igc.code_system = 'DSLD' and tsn.parent_substance_uuid in (select ref_uuid from subs_ref)


select * from ix_ginas_substance igss
inner join ix_ginas_strucdiv ixs on ixs.uuid = igss.structurally_diverse_uuid 
inner join ix_ginas_name ign on ign.owner_uuid = igss.uuid 
where ixs.parent_substance_uuid in (select ref_uuid from subs_ref)

