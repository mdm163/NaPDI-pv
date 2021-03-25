--- This needs to be ran against the SRS database after running GSRS/gsrs_get_data_without_mixture.py

--- Example query to export the data needed by the vocab standardization tool
with dsld_cn as (
 select distinct tsn.related_latin_binomial, 
                regexp_replace(igc1.comments, '^.*\|','') t1
 from scratch_u54.test_srs_np_part tsn inner join scratch_u54.test_srs_np_part_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid 
 where     
     (igc1.code_system in ('DSLD')  and tsn.substance_uuid is not null)
 UNION
 select distinct tsn.related_latin_binomial,  
                regexp_replace(igc1.comments, '^.*\|','') t1
 from scratch_u54.test_srs_np tsn inner join scratch_u54.test_srs_np_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid   
 where 
     (igc1.code_system = 'DSLD' and tsn.substance_uuid is not null)    
)
select *
from (
select tsn.substance_uuid as uri, tsn.name, tsn.related_latin_binomial as definition, 
       case 
          when (tsn.related_common_name is not null and tsn.related_common_name != '') then tsn.related_common_name 
             else (select t1 from dsld_cn where dsld_cn.related_latin_binomial = tsn.related_latin_binomial limit 1) 
          end "alternative term"
from scratch_u54.test_srs_np tsn
union
select tsnp.substance_uuid as uri, tsnp.name, tsnp.related_latin_binomial as definition, 
       case 
          when (tsnp.related_common_name is not null and tsnp.related_common_name != '') then tsnp.related_common_name 
             else (select t1 from dsld_cn where dsld_cn.related_latin_binomial = tsnp.related_latin_binomial limit 1) 
          end "alternative term"
from scratch_u54.test_srs_np_parent tsnp
union
select tsnp2.substance_uuid as uri, tsnp2.name, tsnp2.related_latin_binomial as definition,
       case 
          when (tsnp2.related_common_name is not null and tsnp2.related_common_name != '') then tsnp2.related_common_name 
             else (select t1 from dsld_cn where dsld_cn.related_latin_binomial = tsnp2.related_latin_binomial limit 1) 
          end "alternative term"
from scratch_u54.test_srs_np_part tsnp2
) t
order by "alternative term"
;



--- scratch ---

/*

select *
from scratch_u54.test_srs_np tsn 
where tsn.organism_genus  = 'CANNABIS'
 and tsn.organism_species = 'SATIVA';

select *
from scratch_u54.test_srs_np_parent tsn 
where tsn.organism_genus  = 'CANNABIS'
 and tsn.organism_species = 'SATIVA'
 ;

select * from ix_ginas_code igc
where igc.owner_uuid = '4495dd37-943e-434d-bf30-ea9172d543c8' and igc.code_system = 'DSLD'

--- TODO: determine what the code column points to in the DSLD
select * 
from ix_ginas_code igc
where  igc.code_system = 'DSLD'
;

-- other potentially interesting terminologies

-- interesting but seems US centric
select * 
from ix_ginas_code igc
where  igc.code_system = 'USDA PLANTS'
;

-- probably interesting for its connetion into dbpedia
select * 
from ix_ginas_code igc
where  igc.code_system = 'WIKIPEDIA'
;

-- nothing interesting
select * 
from ix_ginas_code igc
where  igc.code_system in ('HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH') 
;

select distinct igc.code_system  
from ix_ginas_code igc
order by igc.code_system
;


-- Doesn't work well
select distinct tsn.substance_uuid, tsn.organism_family, tsn.organism_genus, tsn.organism_species, igc.* -- regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_u54.test_srs_np tsn on igc.owner_uuid = tsn.substance_uuid 
where igc.code_system in ('DSLD') 
union 
select distinct tsnp.substance_uuid, tsnp.organism_family, tsnp.organism_genus, tsnp.organism_species, igc.*-- regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_u54.test_srs_np_parent tsnp on igc.owner_uuid = tsnp.substance_uuid 
where igc.code_system in ('DSLD')
union 
select distinct tsnp2.substance_uuid, tsnp2.organism_family, tsnp2.organism_genus, tsnp2.organism_species, igc.* -- regexp_replace(igc.comments, '^.*\|','') t -- split_part(igc."comments",'|',3) 
from ix_ginas_code igc inner join scratch_u54.test_srs_np_part tsnp2 on igc.owner_uuid = tsnp2.substance_uuid 
where igc.code_system in ('DSLD')
;

-- 21
select *
from scratch_u54.test_srs_np tsn inner join scratch_u54.test_srs_np_part_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
;

-- 173
select distinct tsn.organism_genus, tsn.organism_species, tsn.substance_uuid, 
                tsnpr.related_substance_uuid, tsnpr.mediator_substance_uuid, tsnpr.originator_uuid,
                igc1.code_system, regexp_replace(igc1.comments, '^.*\|','') t1, 
                igc2.code_system, regexp_replace(igc2.comments, '^.*\|','') t2,
                igc3.code_system, regexp_replace(igc3.comments, '^.*\|','') t3, 
                igc4.code_system, regexp_replace(igc4.comments, '^.*\|','') t4,
                igc5.code_system, regexp_replace(igc5.comments, '^.*\|','') t5
from scratch_u54.test_srs_np_part tsn inner join scratch_u54.test_srs_np_part_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid 
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.related_substance_uuid
   left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.mediator_substance_uuid 
   left outer join ix_ginas_code igc4 on igc4.owner_uuid = tsnpr.originator_uuid 
   left outer join ix_ginas_code igc5 on igc5.owner_uuid = tsnpr.uuid
where 
     ((igc1.code_system in ('DSLD','HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH')  and tsn.substance_uuid is not null)
       or (igc2.code_system in ('DSLD','HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH') and tsnpr.related_substance_uuid is not null)
       or (igc3.code_system in ('DSLD','HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH') and tsnpr.mediator_substance_uuid is not null)
       or (igc4.code_system in ('DSLD','HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH') and tsnpr.originator_uuid is not null)
       or (igc5.code_system in ('DSLD','HEALTH-CANADA NHP INGREDIENT RECORD','HEALTH -CANADA NHP INGREDIENT MONOGRAPH') and tsnpr.uuid is not null)
       )
;


-- 0
select distinct tsn2.organism_genus, tsn2.organism_species, tsn2.substance_uuid, 
                tsnpr.related_substance_uuid, tsnpr.mediator_substance_uuid, tsnpr.originator_uuid, 
                regexp_replace(igc1.comments, '^.*\|','') t1, regexp_replace(igc2.comments, '^.*\|','') t2,
                regexp_replace(igc3.comments, '^.*\|','') t3, regexp_replace(igc4.comments, '^.*\|','') t4
from scratch_u54.test_srs_np_part tsn inner join scratch_u54.test_srs_np_part_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   inner join scratch_u54.test_srs_np tsn2 on tsnpr.owner_uuid = tsn2.substance_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid 
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.related_substance_uuid
   left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.mediator_substance_uuid 
   left outer join ix_ginas_code igc4 on igc4.owner_uuid = tsnpr.originator_uuid 
where 
     ((igc1.code_system = 'DSLD' and tsn.substance_uuid is not null)
       or (igc2.code_system = 'DSLD' and tsnpr.related_substance_uuid is not null)
       or (igc3.code_system = 'DSLD' and tsnpr.mediator_substance_uuid is not null)
       or (igc4.code_system = 'DSLD' and tsnpr.originator_uuid is not null)
       )
;

-- 190
select distinct tsn.organism_genus, tsn.organism_species, tsn.substance_uuid, 
                tsnpr.related_substance_uuid, tsnpr.mediator_substance_uuid, tsnpr.originator_uuid, 
                regexp_replace(igc1.comments, '^.*\|','') t1, regexp_replace(igc2.comments, '^.*\|','') t2,
                regexp_replace(igc3.comments, '^.*\|','') t3, regexp_replace(igc4.comments, '^.*\|','') t4
from scratch_u54.test_srs_np tsn inner join scratch_u54.test_srs_np_rel tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid 
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.related_substance_uuid
   left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.mediator_substance_uuid 
   left outer join ix_ginas_code igc4 on igc4.owner_uuid = tsnpr.originator_uuid 
where 
     ((igc1.code_system = 'DSLD' and tsn.substance_uuid is not null)
       or (igc2.code_system = 'DSLD' and tsnpr.related_substance_uuid is not null)
       or (igc3.code_system = 'DSLD' and tsnpr.mediator_substance_uuid is not null)
       or (igc4.code_system = 'DSLD' and tsnpr.originator_uuid is not null)
       )
;

-- 0
select distinct tsn.organism_genus, tsn.organism_species, tsn.substance_uuid, 
                tsnpr.owner_uuid, tsnpr.substance_uuid, tsnpr.parent_substance_uuid, 
                igc1."comments" c1, igc2."comments" c2, igc3."comments" c3
from scratch_u54.test_srs_np tsn inner join scratch_u54.test_srs_np_part tsnpr on tsn.substance_uuid = tsnpr.parent_substance_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsnpr.substance_uuid
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.parent_substance_uuid 
where 
     ((igc1.code_system = 'DSLD' and tsnpr.substance_uuid is not null)
       or (igc2.code_system = 'DSLD' and tsnpr.owner_uuid is not null)
       or (igc3.code_system = 'DSLD' and tsnpr.parent_substance_uuid is not null)
       )
;


-- 0
select distinct tsn.organism_genus, tsn.organism_species, tsn.substance_uuid, 
                tsnpr.owner_uuid, tsnpr.substance_uuid, tsnpr.parent_substance_uuid, 
                igc1."comments" c1, igc2."comments" c2, igc3."comments" c3
from scratch_u54.test_srs_np tsn inner join scratch_u54.test_srs_np_part tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.substance_uuid 
   left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.parent_substance_uuid 
where 
     ((igc1.code_system = 'DSLD' and tsn.substance_uuid is not null)
       or (igc2.code_system = 'DSLD' and tsnpr.substance_uuid is not null)
       or (igc3.code_system = 'DSLD' and tsnpr.parent_substance_uuid is not null)
       )
;

-- 0
select distinct tsn.organism_genus, tsn.organism_species, tsn.substance_uuid, 
                tsnpr.parent_substance_uuid,  
                igc1."comments" c1, igc2."comments" c2
from scratch_u54.test_srs_np_parent tsn inner join scratch_u54.test_srs_np_part tsnpr on tsn.substance_uuid = tsnpr.owner_uuid 
   left outer join ix_ginas_code igc1 on igc1.owner_uuid = tsn.substance_uuid 
   left outer join ix_ginas_code igc2 on igc2.owner_uuid = tsnpr.parent_substance_uuid 
 --  left outer join ix_ginas_code igc3 on igc3.owner_uuid = tsnpr.mediator_substance_uuid 
 --  left outer join ix_ginas_code igc4 on igc4.owner_uuid = tsnpr.originator_uuid 
where 
     ((igc1.code_system = 'DSLD' and tsn.substance_uuid is not null)
       or (igc2.code_system = 'DSLD' and tsnpr.parent_substance_uuid is not null)
     --  or (igc3.code_system = 'DSLD' and tsnpr.mediator_substance_uuid is not null)
     --  or (igc4.code_system = 'DSLD' and tsnpr.originator_uuid is not null)
       )
;


--- TODO : will need some help figuring out where the related substance uuid and other uuids point to in this result
select *
from scratch_u54.test_srs_np_rel tsn 
where tsn.owner_uuid  = '4495dd37-943e-434d-bf30-ea9172d543c8'
 ;
 
*/



