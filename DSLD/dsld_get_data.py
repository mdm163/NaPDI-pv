import json, os

dirIn = '/home/sanya/npdi-workspace/DSLD/dsldjsonout/dsldjsonout/'
dirOut = '/home/sanya/npdi-workspace/DSLD/'

dsld_data = []
dsld_ingredients = {}
dsld_statements = []
dsld_contacts = []

#not unique, may have duplicates in statements and contacts
def extract_data(data_obj):
	statements = data_obj['statements']
	contacts = data_obj['contacts']

	dsld_statements.extend(statements)
	dsld_contacts.extend(contacts)

	data_obj['statements'] = ''
	data_obj['contacts'] = ''
	return data_obj

#extract unique ingredients from each product
def extract_ingredients(data_obj):
	ingredients = data_obj['ingredients']
	ingredient_IDs = []

	for item in ingredients:
		ingrID = item['Ingredient_ID']
		if ingrID not in dsld_ingredients:
			del item['DSLD_ID']
			item['Blends_Ancestry'] = item["Blends'_Ancestry"]
			del item["Blends'_Ancestry"]

			item['Suggested_Recommended_Usage_Directions'] = item['Suggested_Recommended_Usage_Directions:']
			del item['Suggested_Recommended_Usage_Directions:']
			dsld_ingredients[ingrID] = item

		ingredient_IDs.append(ingrID)

	data_obj['ingredients'] = ingredient_IDs
	return data_obj

def load_json():
	files = os.listdir(dirIn)
	#source data has one object per json file
	for file in files:
		#need to ignore error due to byte 0xae not being decoded by utf-8. Using errors='ignore' strips the character out and loads file
		file_i = open(dirIn+file, errors='ignore')
		try:
			data = json.load(file_i)
			data = extract_data(data)
			data = extract_ingredients(data)
			dsld_data.append(data)

		except Exception as e:
			print(file)
			continue
		

if __name__ == '__main__':
	
	load_json()

	dsld_ingredients_list = []
	#get ingredients in list
	for key in dsld_ingredients:
		dsld_ingredients_list.append(dsld_ingredients[key])

	print('Total products: ', len(dsld_data))
	print('Total ingredients: ', len(dsld_ingredients_list))
	print('Total statements: ', len(dsld_statements))
	print('Total contacts: ', len(dsld_contacts))
 

	with open(dirOut+'dsld_data.json', 'w') as file_d:
		json.dump(dsld_data, file_d)

	with open(dirOut+'dsld_ingredients.json', 'w') as file_ing:
		json.dump(dsld_ingredients_list, file_ing)

	with open(dirOut+'dsld_statements.json', 'w') as file_s:
		json.dump(dsld_statements, file_s)

	with open(dirOut+'dsld_contacts.json', 'w') as file_c:
		json.dump(dsld_contacts, file_c)





