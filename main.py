from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from pytz import timezone

tz = timezone('America/Mexico_City')
# agentes
agents = ["ims-worker-2025.08"] # , "ims-rest-2025.08"
LAST_DAYS = 20

es = Elasticsearch("http://192.167.36.108:9200")

# obtener fecha actual y 14 dias atras
# ejemplo patron: ims-rest-2025.08.01
formatf = '%Y.%m.%d'
ds = datetime.now(tz)
# print("ds:", ds)
datestring = ds.strftime(formatf)

print("datestring:", datestring)
HIDDEN_INDEX = ["service", "heb"]
# 'service', '.tasks', '.geoip_databases', '.async-search', '.apm-agent-configuration','.kibana', '.apm-custom-link', '.apm-custom-link', 'heb'
# List of index de agentes que no se borraran
PRESERVE_INDEX = []
for x in range(LAST_DAYS):
  d = ds - timedelta(days=x)
  for agent in agents:
    index_name = agent + '-' + d.strftime(formatf)
    PRESERVE_INDEX.append(index_name)
    # print(index_name)
print(PRESERVE_INDEX)

resp = es.indices.get(index="ims-worker-2025.08.01", )
print("--->resp:", resp.body)


# List all indices
agents_indices = []
indices = es.cat.indices( format="json")
print(indices[7])

# Filtra por nombre de agente
for index in indices:
    index_name = index['index']
    for a in agents:
       if index_name.__contains__(a):
          print(f"Yes! {index_name} is containing.")
          resp = es.indices.get(index=index_name)
          print(resp)
          agents_indices.append(resp.body)

print(agents_indices)
# for aindex in agents_indices:
#     index_name = aindex['index']
#     my_datetime = datetime.fromtimestamp(aindex['index']['settings']['index']['creation_date'] / 1000)
#     print(index_name, my_datetime)

# formatf = '%Y-%m-%d_%H-%M-%S'
# my_datetime = datetime.datetime.fromtimestamp(aindex['index']['settings']['index']['creation_date'] / 1000)
# my_datetime.strftime(formatf)
'''
# Delete each index
for index in indices:
    index_name = index['index']
    if not index_name in PRESERVE_INDEX:
    # es.indices.delete(index=index_name)
      # print(f"index: {index_name} viejo")
        # if not "service" in index_name:
        #   print(f"index: {index_name} viejo")
        # print(f"index: {index_name} viejo")
        for hide in HIDDEN_INDEX:
          if not hide in index_name:
            print(f"index: {index_name} viejo")
    else:
        print(f"index: {index_name} vigente")
       
'''