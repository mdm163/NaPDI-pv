import psycopg2, sys
import json
from psycopg2.extras import execute_values

dirPath = '/home/sanya/npdi-workspace/DSLD/'

def create_table(conn):
	
	"""create tables in postgresDB cem"""
	commands = ("""
		DROP TABLE IF EXISTS staging_dietary_suppl.dsld_product
		""",
		"""DROP TABLE IF EXISTS staging_dietary_suppl.dsld_ingredient""",
		"""DROP TABLE IF EXISTS staging_dietary_suppl.dsld_contact""",
		"""DROP TABLE IF EXISTS staging_dietary_suppl.dsld_statement""",
		"""
		CREATE TABLE staging_dietary_suppl.dsld_product (
	DSLD_ID VARCHAR(255),
	Outer_Packaging VARCHAR(255),
	Statement_of_Identity VARCHAR(1500),
	LanguaL_Dietary_Claim_or_Use VARCHAR(255),
	Product_Name VARCHAR(255),
	LanguaL_Product_Type VARCHAR(255),
	count INTEGER,
	Brand VARCHAR(255),
	Date_Entered_into_DSLD VARCHAR(255),
	Serving_Size VARCHAR(1500),
	NHANES_ID VARCHAR(255),
	success boolean,
	Suggested_Use VARCHAR(3000),
	Database VARCHAR(255),
	Net_Contents_Quantity VARCHAR(255),
	LanguaL_Supplement_Form VARCHAR(255),
	Product_Trademark_Copyright_Symbol VARCHAR(255),
	SKU VARCHAR(255),
	DB_Source VARCHAR(255),
	LanguaL_Intended_Target_Groups VARCHAR(255),
	Tracking_History VARCHAR(255),
	statements VARCHAR(255),
	contacts VARCHAR(255),
	ingredients VARCHAR(4000)
)
		""",
		"""
		CREATE TABLE staging_dietary_suppl.dsld_ingredient (
	Ingredient_ID VARCHAR(255),
	DSLD_Ingredient_Categories VARCHAR(255),
	Amount_Serving_Unit VARCHAR(255),
	Ingredient_Group_GRP_ID VARCHAR(255),
	Blends_Ancestry VARCHAR(500),
	Amount_Per_Serving VARCHAR(255),
	Dietary_Ingredient_Synonym_Source VARCHAR(3000),
	Blended_Ingredient_Types VARCHAR(255),
	Pct_Daily_Value_per_Serving VARCHAR(255),
	Serving_Size VARCHAR(255),
	Suggested_Recommended_Usage_Directions VARCHAR(3000),
	DB_Source VARCHAR(255),
	Ancestry__Number_of_Parents_Row_IDs VARCHAR(255)
)
		""",
		"""
		CREATE TABLE staging_dietary_suppl.dsld_contact (
	ZIP VARCHAR(255), 
	IS_MANUFACTURER VARCHAR(255), 
	Type VARCHAR(255), 
	IS_PACKAGER VARCHAR(255), 
	Address VARCHAR(255),
	State VARCHAR(255), 
	IS_DISTRIBUTOR VARCHAR(255),
	DSLD_ID VARCHAR(255), 
	City VARCHAR(255),
	IS_RESELLER VARCHAR(255),
	IS_OTHER VARCHAR(255),
	Name VARCHAR(255) 
)
		""",
		"""
		CREATE TABLE staging_dietary_suppl.dsld_statement (
	Statement VARCHAR(9000),
	Statement_Type VARCHAR(255),
	DSLD_ID VARCHAR(255)
)
		"""
		)

	flag = 0
	try:
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
		flag = 1
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	cur.close()
	return flag


def read_data():
	with open(dirPath+'dsld_data.json') as file_d:
		dsld_data = json.load(file_d)

	with open(dirPath+'dsld_ingredients.json') as file_ing:
		dsld_ingredients = json.load(file_ing)

	with open(dirPath+'dsld_statements.json') as file_s:
		dsld_statements = json.load(file_s)

	with open(dirPath+'dsld_contacts.json') as file_c:
		dsld_contacts = json.load(file_c)

	return dsld_data, dsld_ingredients, dsld_statements, dsld_contacts

def insert_data(conn, data_list, data_name):
	
	columns = data_list[0].keys()

	if data_name == "dsld_product":
		query = "INSERT INTO staging_dietary_suppl.dsld_product ({}) VALUES %s".format(','.join(columns))
	elif data_name == "dsld_ingredient":
		query = "INSERT INTO staging_dietary_suppl.dsld_ingredient ({}) VALUES %s".format(','.join(columns))
	elif data_name == "dsld_statement":
		query = "INSERT INTO staging_dietary_suppl.dsld_statement ({}) VALUES %s".format(','.join(columns))
	elif data_name == "dsld_contact":
		query = "INSERT INTO staging_dietary_suppl.dsld_contact ({}) VALUES %s".format(','.join(columns))

	try:
		cursor = conn.cursor()
		values = [[value for value in item.values()] for item in data_list]
		execute_values(cursor, query, values)
		
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		conn.rollback()
		cursor.close()
		sys.exit(1)
	print('Insert successful: ')
	print(str(cursor.rowcount))
	conn.commit()

if __name__ == '__main__':

	try:
		conn = psycopg2.connect("dbname='cem' user='rw_grp' host='localhost' password='rw_grp'")
	except Exception as error:
		print(error)
		print('Unable to connect to DB')
		conn = None
	if not conn:
		sys.exit(1)

	flag = create_table(conn)
	if flag == 0:
		print('Tables not created, exiting')
		sys.exit(1)
	print('Tables created successfully')
	print('Reading data from files: ')
	dsld_product, dsld_ingredient, dsld_statement, dsld_contact = read_data()

	###all data is list of dictionaries, insert into tables
	print('Inserting products:')
	insert_data(conn, dsld_product, "dsld_product")
	print('Inserting ingredients:')
	insert_data(conn, dsld_ingredient, "dsld_ingredient")
	print('Inserting statements:')
	insert_data(conn, dsld_statement, "dsld_statement")
	print('Inserting contacts')
	insert_data(conn, dsld_contact, "dsld_contact")

	conn.close()






