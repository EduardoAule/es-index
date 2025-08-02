from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from pytz import timezone

tz = timezone('America/Mexico_City')
# agentes
agents = ["ims-worker", "ims-rest"]
LAST_DAYS = 20

es = Elasticsearch("http://192.167.36.108:9200")

# obtener fecha actual y 14 dias atras
# ejemplo patron: ims-rest-2025.08.01
formatf = '%Y.%m.%d'
ds = datetime.now(tz)
# print("ds:", ds)
datestring = ds.strftime(formatf)

print("datestring:", datestring)
PRESERVE_INDEX = []
for x in range(LAST_DAYS):
  d = ds - timedelta(days=x)
  for agent in agents:
    index_name = agent + '-' + d.strftime(formatf)
    PRESERVE_INDEX.append(index_name)
    # print(index_name)
print(PRESERVE_INDEX)



# List indices matching pattern
indices = es.cat.indices( format="json")

# # Delete each index
for index in indices:
    index_name = index['index']
    if not index_name in PRESERVE_INDEX:
    # es.indices.delete(index=index_name)
        # print(f"index: {index_name} viejo")
        if not "heb" in index_name:
           print(f"index: {index_name} viejo")
    else:
        print(f"index: {index_name} vigente")
       

