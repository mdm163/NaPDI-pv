import json
import requests, os
import psycopg2, sys

#add np to list 
#np = ['KRATOM', 'GREEN TEA', 'GOLDENSEAL', 'CINNAMON', 'CANNABIS', 'LICORICE']

#or specify as argument
np = [str(sys.argv[1])]

np_result = {}

def get_initial_details(np_item):
	uri = "https://ginas.ncats.nih.gov/ginas/app/api/v1/substances/search?q="+np_item
	response = requests.get(uri)
	result = response.json()
	uuid = result["content"][0]["uuid"]
	substance_class = result["content"][0]["substanceClass"]
	np_result[np_item] = result
	return substance_class

def get_structurally_diverse_np(uuid, parent_uuid, conn):
	query_clean = ("""DROP TABLE IF EXISTS scratch_sanya.test_cinn
		""",
		"""DROP TABLE IF EXISTS scratch_sanya.test_cinn_parent
		""",
		"""DROP TABLE IF EXISTS scratch_sanya.test_cinn_rel
		""")

	query_main = """
		with np_substance as (
		select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1
		where igs1.uuid = '{}'
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
		into scratch_sanya.test_cinn
		from ix_ginas_substance igs 
		inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
		inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
		where igs.uuid in 
		(select substance_uuid from np_substance) or 
		igs.uuid in
		(select parent_uuid from np_parent)
		""".format(uuid)

	if parent_uuid == '':
		query_parent = None
		query_relations = """
			select * into scratch_sanya.test_cinn_rel from ix_ginas_relationship igr
			where igr.owner_uuid = '{}'
			""".format(uuid)
	else:
		#do we want all parent synonyms or just single? Should we include a flag for parent in the main query??
		query_parent = """
			with np_parent as (
			select refuuid as parent_id from ix_ginas_substanceref igs2
			where igs2.uuid = '{}'
			)
			select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
			igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
			ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
			ign."type", ign.preferred, ign.display_name, 
			ixs.uuid as structdiv_uuid, ixs.source_material_class, ixs.source_material_state, ixs.source_material_type,
			ixs.organism_family, ixs.organism_author, ixs.organism_genus, ixs.organism_species, ixs.part_location,
			ixs.part, ixs.parent_substance_uuid 
			into scratch_sanya.test_cinn_parent
			from ix_ginas_substance igs 
			inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
			inner join ix_ginas_strucdiv as ixs on ixs.uuid = igs.structurally_diverse_uuid 
			where igs.uuid in (select parent_id from np_parent)
			""".format(parent_uuid)

		query_relations = """
			with np_parent as (
			select refuuid as parent_id from ix_ginas_substanceref igs2
			where igs2.uuid = '{}'
			)
			select * into scratch_sanya.test_cinn_rel 
			from ix_ginas_relationship igr
			where igr.owner_uuid = '{}' or igr.owner_uuid in (select parent_id from np_parent)
			""".format(parent_uuid, uuid)

		'''query_constituents = """

		"""'''

	flag = 0
	try:
		cur = conn.cursor()
		for query in query_clean:
			cur.execute(query)
		cur.execute(query_main)
		if query_parent is not None:
			cur.execute(query_parent)
		cur.execute(query_relations)
		cur.close()
		conn.commit()
		flag = 1
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	cur.close()
	return flag
	

def get_mixture_np(uuid, parent_uuid, conn):
	query_main = """
		with np_substance as (
		select igs1.uuid as substance_uuid, igs1.* from ix_ginas_substance igs1
		where igs1.uuid = '{}'
		),
		np_mixture as (
		select * from ix_ginas_mixture igm1
		inner join np_substance on np_substance.mixture_uuid = igm1.uuid 
		),
		np_parent as (
		select igs3.refuuid as parent_uuid from ix_ginas_substanceref igs3 
		inner join np_mixture on np_mixture.parent_substance_uuid = igs3.uuid 
		)
		select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
		igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
		ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
		ign."type", ign.preferred, ign.display_name, 
		igm.uuid as mixture_uuid, igm.parent_substance_uuid 
		into scratch_sanya.test_lic
		from ix_ginas_substance igs 
		inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
		inner join ix_ginas_mixture as igm on igm.uuid = igs.mixture_uuid 
		where igs.uuid in 
		(select substance_uuid from np_substance) or 
		igs.uuid in
		(select parent_uuid from np_parent)
		""".format(uuid)
	if parent_uuid == '':
		query_parent = None
		query_relations = """
			select * into scratch_sanya.test_lic_rel
			from ix_ginas_relationship igr
			where igr.owner_uuid = '{}'
			""".format(uuid)
	else:
		query_parent = """
			with np_parent as (
			select refuuid as parent_id from ix_ginas_substanceref igs2
			where igs2.uuid = '{}')
			select igs.dtype, igs.uuid as substance_uuid, igs.created, igs.class, igs.status, igs.modifications_uuid,
			igs.approval_id, igs.structure_id, igs.structurally_diverse_uuid, 
			ign.uuid as name_uuid, ign.internal_references, ign.owner_uuid, ign."name",
			ign."type", ign.preferred, ign.display_name, 
			igm.uuid as mixture_uuid, igm.parent_substance_uuid 
			into scratch_sanya.test_lic_parent
			from ix_ginas_substance igs 
			inner join ix_ginas_name as ign on ign.owner_uuid = igs.uuid 
			inner join ix_ginas_mixture as igm on igm.uuid = igs.mixture_uuid 
			where igs.uuid in (select parent_id from np_parent)
			""".format(parent_uuid)
		query_relations = """
			with np_parent as (
			select refuuid as parent_id from ix_ginas_substanceref igs2
			where igs2.uuid = '{}')
			select * into scratch_sanya.test_lic_rel
			from ix_ginas_relationship igr
			where igr.owner_uuid = '{}' or igr.owner_uuid in (select parent_id from np_parent)
			""".format(parent_uuid, uuid)
	query_components = """
	with np_mixture as (
	select igm.uuid from ix_ginas_mixture igm
	inner join ix_ginas_substance as igs on igm.uuid = igs.mixture_uuid
	where igs.uuid = '{}'),
	np_comp_id as (
	select igsmc.ix_ginas_component_uuid as comp_uuid from ix_ginas_substance_mix_comp igsmc
	inner join np_mixture on np_mixture.uuid = igsmc.ix_ginas_mixture_uuid),
	np_component as (
	select * from ix_ginas_component igc
	inner join ix_ginas_substanceref as iss on igc.substance_uuid = iss.uuid
	where igc.uuid in (select comp_uuid from np_comp_id))
	select * from ix_ginas_substance igss
	into scratch_sanya.test_lic_comp
	inner join np_component on np_component.approval_id = igss.approval_id
	inner join ix_ginas_strucdiv ixs on ixs.uuid = igss.structurally_diverse_uuid
	inner join ix_ginas_name as ign on ign.owner_uuid = igss.uuid
	""".format(uuid)
		
	flag = 0
	try:
		cur = conn.cursor()
		cur.execute(query_main)
		if query_parent is not None:
			cur.execute(query_parent)
		cur.execute(query_relations)
		cur.close()
		conn.commit()
		flag = 1
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	cur.close()
	return flag

if __name__ == '__main__':
	
	try:
		conn = psycopg2.connect("dbname='g_substance_reg' user='rw_grp' host='localhost' password='rw_grp'")
	except Exception as error:
		print(error)
		print('Unable to connect to DB')
		conn = None
	if not conn:
		sys.exit(1)

	np_class = {}
	for item in np:
		np_class[item] = get_initial_details(item)
	print(np_result)

	for item in np:
		uuid = np_result[item]["content"][0]["uuid"]
		if 'structurallyDiverse' in np_result[item]["content"][0]:
			if 'parentSubstance' in np_result[item]["content"][0]['structurallyDiverse']:
				parent_uuid = np_result[item]["content"][0]["structurallyDiverse"]["parentSubstance"]["uuid"]
			else:
				parent_uuid = ''
		elif 'mixture' in np_result[item]['content'][0]:
			if 'parentSubstance' in np_result[item]['content'][0]['mixture']:
				parent_uuid = np_result[item]["content"][0]["mixture"]["parentSubstance"]["uuid"]
			else:
				parent_uuid = ''
		if np_class[item] == "structurallyDiverse":
			flag = get_structurally_diverse_np(uuid, parent_uuid, conn)
		elif np_class[item] == "mixture":
			flag = get_mixture_np(uuid, parent_uuid, conn)
	if flag:
		print('Success')

	conn.close()


