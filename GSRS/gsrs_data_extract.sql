--match to compound string name and then get all parents and synonyms for parent+compound
--cinnamon
with np_ign as (
select * from ix_ginas_name ign1 where ign1."name" = 'CINNAMON'
),
np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1 
inner join np_ign on np_ign.owner_uuid = igs1.uuid 
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)

--kratom
with np_ign as (
select * from ix_ginas_name ign1 where ign1."name" like '%KRATOM%'
),
np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1 
inner join np_ign on np_ign.owner_uuid = igs1.uuid 
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)

--goldenseal
with np_ign as (
select * from ix_ginas_name ign1 where ign1."name" like '%GOLDENSEAL%'
),
np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1 
inner join np_ign on np_ign.owner_uuid = igs1.uuid 
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)

--green tea
with np_ign as (
select * from ix_ginas_name ign1 where ign1."name" = 'GREEN TEA'
),
np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1 
inner join np_ign on np_ign.owner_uuid = igs1.uuid 
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)

--cannabis
with np_ign as (
select * from ix_ginas_name ign1 where ign1."name" like '%CANNABIS%'
),
np_substance as (
select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1 
inner join np_ign on np_ign.owner_uuid = igs1.uuid 
),
np_strucdiv as (
select * from ix_ginas_strucdiv igs2 
inner join np_substance on np_substance.structurally_diverse_uuid = igs2.uuid 
),
np_parent as (
select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
inner join np_strucdiv on np_strucdiv.parent_substance_uuid = igs3.uuid 
)
select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
ign."type", ign.preferred, ign.display_name, 
ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
ixs.part, ixs.parent_substance_uuid 
from ix_ginas_substance igs 
inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
where igs.uuid in 
(select substance_uuid from np_substance) or 
igs.uuid in
(select parent_uuid from np_parent)
