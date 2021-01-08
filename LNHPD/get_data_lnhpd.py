import requests
import json, os

#dir_out = '/home/sanya/npdi-workspace/LNHPD/LNHPD_output/'
#dir_out = "/Users/sanya/npdi-workspace/LNHPD/LNHPD_output"

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
	file_p = open(dir_out+'lnhpd_page.txt', 'a')

	#Total pages = 6292 (as of 2020-01-07)
	for page_no in range(page_start, page_end+1):
		#returns paginated response with 100 objects per page
		#Handle - duplicate data present in source files
		uri = "https://health-products.canada.ca/api/natural-licences/medicinalingredient/?page="+str(page_no)+"&lang=en&type=json"
		response = call_API(uri)
		result = response.json()
		lnhpd.extend(result['data'])
		count = len(lnhpd)
		#save every 100000 results and reinitialize the dictionary
		if count % 80 == 0:
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
	print('De-duplicating all objects')
	lnhpd_new_all = []
	lnhpd_ids_list = []
	files = os.listdir(dir_out)
	for file in files:
		if file[-5:] == '.json':
			file_i = open(dir_out+file)
			print('\nFilename: ', file)
			lnhpd = json.load(file_i)
			for item in lnhpd:
				if item['lnhpd_id'] not in lnhpd_ids_list:
					lnhpd_new_all.append(item)
					lnhpd_ids_list.append(item['lnhpd_id'])

	outfile = dir_out + 'lnhpd_all_unique.json'
	new_count = len(lnhpd_new_all)
	toJSON(outfile, lnhpd_new_all)
	return new_count

if __name__ == '__main__':
	total_count = extract_data_from_api(1, 10)
	print('Total objects saved: ', total_count)
	total_count_new = remove_duplicates_and_save(total_count)
	print('Total object after de-duplication: ', total_count_new)
	
	