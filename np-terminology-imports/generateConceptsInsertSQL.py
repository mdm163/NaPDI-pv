import sys, csv

reload(sys)  
sys.setdefaultencoding('utf8')

# create sql script for inserting custom concepts
# reserve (-9999999, -7000000) for concept names

VOCABULARY_SCHEMA = 'staging_vocabulary'
LIST_OF_CUSTOM_VOCABULARIES = []  # Use this to add vocabularies OTHER than NAPDI
INPUT_TSV = 'np-custom-terms.tsv'


## FOR NOW, edit the concept class insert function below to add the
## NaPDI NP names. Later, we will work out how to add ancestor
## relationship concepts to handle these


# UTILS ##############################################################################
# encode data as utf-8
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

        
# INSERT QUERY TEMPLATES #############################################################
def insert_concept_template(concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, concept_code):
    return "INSERT INTO %s.concept (concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason) VALUES (%s, '%s', '%s', '%s', '%s', '', '%s', '2000-01-01', '2099-02-22', '');" % (VOCABULARY_SCHEMA, concept_id, concept_name.replace("'", "''"), domain_id, vocabulary_id, concept_class_id, concept_code)

def insert_concept_class_template(concept_class_id, concept_class_name, concept_class_concept_id):
    return "INSERT INTO %s.concept_class (concept_class_id, concept_class_name, concept_class_concept_id) VALUES ('%s', '%s', %s);" % (VOCABULARY_SCHEMA, concept_class_id, concept_class_name, concept_class_concept_id)


def insert_vocabulary_template(vocabulary_id, vocabulary_name, vocabulary_reference, vocabulary_version, vocabulary_concept_id):
    return "INSERT INTO %s.vocabulary (vocabulary_id, vocabulary_name, vocabulary_reference, vocabulary_version, vocabulary_concept_id) VALUES ('%s', '%s', '%s', '%s', %s);" % (VOCABULARY_SCHEMA, vocabulary_id, vocabulary_name, vocabulary_reference, vocabulary_version, vocabulary_concept_id)


def insert_domain_template(domain_id, domain_name, domain_concept_id):
    return "INSERT INTO %s.domain (domain_id, domain_name, domain_concept_id) VALUES ('%s', '%s', %s);" % (VOCABULARY_SCHEMA, domain_id, domain_name, domain_concept_id)


# DELETE #############################################################################
def delete_concept_by_id():
    return "DELETE FROM %s.concept WHERE concept_id BETWEEN -9999999 AND -7000000;" % VOCABULARY_SCHEMA


def delete_concept_class_by_id():
    return "DELETE FROM %s.concept_class WHERE concept_class_concept_id BETWEEN -9999999 AND -7000000;" % VOCABULARY_SCHEMA


def delete_vocabulary_by_concept_id():
    return "DELETE FROM %s.vocabulary WHERE vocabulary_concept_id BETWEEN -9999999 AND -7000000;" % VOCABULARY_SCHEMA


def delete_domain_by_concept_id():
    return "DELETE FROM %s.domain WHERE domain_concept_id BETWEEN -9999999 AND -7000000;" % VOCABULARY_SCHEMA


# PRINT SQL ##########################################################################
# vocabulary table insert for custom and term URI namespaces
# return: the next available concept id 
def print_vocabulary_insert_sql(concept_id):

    # We have to have an entry for NaPDI
    print insert_concept_template(-9999000, 'Natural product-drug interaction project custom terms ', 'Metadata', 'Vocabulary', 'Vocabulary', 'OMOP generated')    
    print insert_vocabulary_template('NAPDI', 'Natural product-drug interaction project custom terms', 'NAPDI', 'Spring 2021', -9999000)

    # other custom vocabs are entered here 
    vocabL = LIST_OF_CUSTOM_VOCABULARIES
    for vocab in vocabL:
        print insert_concept_template(concept_id, vocab, 'Metadata', 'Vocabulary', 'Vocabulary', 'OMOP generated')
        print insert_vocabulary_template(vocab, vocab, '', 'Spring 2021', concept_id)
        concept_id += 1
    return concept_id + 1


# concept table insert for custom terms
# return: the next available concept id 
def print_concept_insert_sql(concept_id):
    
    (URI,TERM,DEFINITION,ALTERNATIVE) = (0,1,2,3)
    f = open(INPUT_TSV, 'r')
    buf = f.read()
    f.close()
    
    lines = buf.split('\n')
   
    domain_id = "NaPDI research";
    for rowS in lines[1:]:
        if rowS == "":
            break
       
        row = rowS.split('\t')
        if row[ALTERNATIVE] == '':
            row[ALTERNATIVE] = 'NEEDS COMMON NAME'
        uri = row[URI].replace('"','')
        concept_class_id = row[ALTERNATIVE].replace("'",'\'\'')
        vocabulary_id, concept_code = 'NAPDI', uri
        concept_name, synonyms = row[TERM].replace("'",'\'\'') + ' [' + row[DEFINITION] + ']', row[ALTERNATIVE].replace("'",'\'\'')

        print insert_concept_template(concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, concept_code)
        concept_id += 1
    return concept_id + 1


# domain table insert
# return: the next available concept id 
def print_domain_insert_sql():
    print insert_concept_template(-9900000, 'NaPDI custom terms', 'Metadata', 'Domain', 'Domain', 'OMOP generated')
    print insert_domain_template('NaPDI research', 'NaPDI research',  -9900000)


# concept class insert
def print_concept_class_insert_sql():
    print insert_concept_template(-9990000, 'NaPDI Natural Product', 'Metadata', 'Concept Class', 'Concept Class', 'OMOP generated')    
    print insert_concept_class_template('natural product', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('NEEDS COMMON NAME', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Aloe vera', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Barberry', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Beet root', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Black pepper', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Bladderwrack', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Bloodroot', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Blue Cohosh', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Broad Bean', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('California Poppy', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Candelilla', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Carrot', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Catnip', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Centaury', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Chamomile (not specified)', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Cinnamon', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('cola nut', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Coleus', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Coltsfoot', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Coptis', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Cramp Bark', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Cumin', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Dandelion', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Echinacea angustifolia', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Echinacea purpurea', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Elderberry', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('English Walnut', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Fenugreek', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Feverfew', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Flax seed', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Garcinia', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Gentian Root', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Ginkgo', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Goat\'\'s rue', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Goldenseal', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Green tea', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Hemp extract', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Horehound', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Horny goat weed', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Horse Chestnut', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Horsetail', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Ivy leaf', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Kale', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Kratom', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Leek', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Lesser Galangal', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Licorice', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Lungwort', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Magnolia', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Mimosa pudica', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('onion', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Parsley', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Peach', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Persimmon', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Quassia', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Queen\'\'s Delight', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Ragweed', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Robinia Pseudoacacia', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Rose Hip', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Sargassum', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Saw Palmetto', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Spearmint', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Spikenard', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('St. John\'\'s Wort', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Sweet Marjoram', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Tansy', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Turmeric', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Valerian', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Wild Yam', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Wormwood', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Yerba Mate', 'NaPDI Test Class', -9990000)
    print insert_concept_class_template('Yohimbe', 'NaPDI Test Class', -9990000)
    
    

# MAIN ###############################################################################
def print_insert_script():
    # templated inserting statements
    print_domain_insert_sql()
    print_concept_class_insert_sql()
    print_vocabulary_insert_sql(-8999999)
    print_concept_insert_sql(-7999999)
    
def print_delete_script():
    print delete_concept_by_id()
    print delete_vocabulary_by_concept_id()
    print delete_domain_by_concept_id()
    print delete_concept_class_by_id()

    
def main():
    print "START TRANSACTION;"
    print_insert_script()
    print "END;"

    ## Use this line to re print the delete statements
    #print_delete_script()

if __name__ == '__main__':
    main()


