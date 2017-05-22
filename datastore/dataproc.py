from google.cloud import datastore
datastore_client = datastore.Client()
kind = 'bor'

# in case it is a new entity, comment below two lines
id = 5649391675244544 
entity_key = datastore_client.key(kind, id)

# in case it is a new entity, uncomment below line
# entity_key = datastore_client.key(kind)

entity_row = datastore.Entity(key=entity_key)

entity_row['bhp_range'] = 'bhp_range'
entity_row['area'] = 'area'
entity_row['country'] = 'india'

datastore_client.put(entity_row)
#print('Saved {}: {}'.format(entity_row.key.id, entity_row['area']))


query = client.query(kind='bor')
query.add_filter('area', '=', 'area')
query.add_filter('bhp_range', '=', 'bhp_range')
query.add_filter('country', '=', 'india')

results = query.fetch()

#print (list(results))
#for result in results:
#	print result

for result in results:
#	print result['country']
	a = result
	a['country'] = 'UK'
	datastore_client.put(result)