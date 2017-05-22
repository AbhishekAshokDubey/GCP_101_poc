from google.cloud import datastore
datastore_client = datastore.Client()
kind = 'bor'
entity_key = datastore_client.key(kind)
entity_row = datastore.Entity(key=entity_key)

import csv
path = r"../data/Wline_bor_date_header.csv"
delimiter = "," 
with open(path, 'rb') as f:
	reader = csv.reader(f, delimiter = delimiter)
	header = f.readline().replace('\n','').replace('\r','').split(delimiter)
	for row in reader:
		#data = row.split(delimiter)
		entity_key = datastore_client.key(kind)
		entity_row = datastore.Entity(key=entity_key)
		for (h,x) in zip(header,row):
			entity_row[h] = x
		datastore_client.put(entity_row)
		print "..\n"
		
		
# https://googlecloudplatform.github.io/google-cloud-python/stable/datastore-queries.html