from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from pytz import timezone, UTC

tz = timezone('America/Mexico_City')
# agentes
agents = ["ims-worker", "ims-rest"]
OLDERS_WITH_DAYS = 20

es = Elasticsearch("http://192.167.36.108:9200")

# obtener fecha actual y 14 dias atras
# ejemplo patron: ims-rest-2025.08.01
# formatf = '%Y.%m.%d'
ds = datetime.now(tz)
# print("ds:", ds)
# datestring = ds.strftime(formatf)
dt_last_days = ds - timedelta(days=OLDERS_WITH_DAYS)

print("datestring:", dt_last_days, ds)

# Index with pattern: agents[]
agents_indices = []
# List all index
indices = es.cat.indices( format="json")
# print(indices[7])

# Filtrar por nombre de agente
for index in indices:
    index_name = index['index']
    for a in agents:
        # indice contiene el nombre de un agente valido
        if index_name.__contains__(a):
            print(f"Yes! {index_name} is containing.")
            # obtener index y agregarlo a una array
            resp = es.indices.get(index=index_name)
            agents_indices.append(resp.body[index_name])
            # print(resp.body)

# print(agents_indices)
# Recorrer los indices con el patron
# Obtener su fecha de creacion y eliminar
for aindex in agents_indices:
    # print(aindex['settings']['index']['provided_name'])
    index_name = aindex['settings']['index']['provided_name']
    my_datetime = datetime.fromtimestamp(int(aindex['settings']['index']['creation_date']) / 1000)
    index_datetime = my_datetime.replace(tzinfo=UTC)
    if index_datetime > dt_last_days:
        print(index_name, my_datetime, "vigente")
    else:
        print(index_name, my_datetime, "old")
