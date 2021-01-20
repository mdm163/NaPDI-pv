#1. (python script) please make the URI a parameter to the script since it will likely change

#5. In the pentaho workflow, I would set the path to the python script and to any data files to be relative to the job to make it more portable. 
#Also, you need some kind of error checking so that if the python script fails the job stops. I can't see this in Pentaho right now so am not sure if you have that. 

import requests
import json, os, sys

dir_out = sys.argv[1]

def call_API(link):
	response = requests.get(link)
	return response

# Writes complete objects to a JSON file.
def toJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def extract_data_from_api(page_start, page_end):
	lnhpd = []
	count = 0
	total_count = 0
	file_p = open(dir_out+'lnhpd_page_completed.txt', 'w')

	#Total pages = 6292 (as of 2020-01-07)
	for page_no in range(page_start, page_end+1):
		#returns paginated response with 100 objects per page
		uri = "https://health-products.canada.ca/api/natural-licences/medicinalingredient/?page="+str(page_no)+"&lang=en&type=json"
		response = call_API(uri)
		result = response.json()
		lnhpd.extend(result['data'])
		count = len(lnhpd)
		#save every 100000 results and reinitialize the dictionary
		if count % 100000 == 0:
			total_count += count
			outfile = dir_out + 'lnhpd_' + str(total_count) + '.json'
			toJSON(outfile, lnhpd)
			print('\nsaving: ', total_count)
			lnhpd = []
		#logging page numbers
		page = result["metadata"]["pagination"]["page"]
		file_p.write('\n'+str(page))
		last_page = result["metadata"]["pagination"]["next"]
	
		if last_page is None or page_no == page_end:
			#save remaining objects
			
			total_count += count
			outfile_last = dir_out + 'lnhpd_' + str(total_count) + '.json'
			toJSON(outfile_last, lnhpd)
			break		
	return total_count

def remove_duplicates_and_save(total_count):
	print("De-duplicating all objects")
	lnhpd_new_all = {}
	files = os.listdir(dir_out)
	for file in files:
		if file[-5:] == '.json':
			file_i = open(dir_out+file)
			print('\nFilename: ', file)
			lnhpd = json.load(file_i)
			for item in lnhpd:
				lnhpd_id = item['lnhpd_id']
				if lnhpd_id not in lnhpd_new_all:
					lnhpd_new_all[lnhpd_id] = item
	lnhpd_all_unique = []
	for key in lnhpd_new_all:
		lnhpd_all_unique.append(lnhpd_new_all[key])
	outfile = dir_out + 'lnhpd_all_unique.json'
	new_count = len(lnhpd_all_unique)
	toJSON(outfile, lnhpd_all_unique)
	return new_count

if __name__ == '__main__':
	total_count = extract_data_from_api(1, 100000)
	print('Total objects saved: ', total_count)
	total_count_new = remove_duplicates_and_save(total_count)
	print('Total object after de-duplication: ', total_count_new)
	
	