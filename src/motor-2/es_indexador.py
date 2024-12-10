from elasticsearch import Elasticsearch, helpers
from analyzer import analyzer, analyzer_named_entity, get_documents_to_index

import time

def preprocess_with_whoosh_analyzer(text):
    return " ".join([t.text for t in analyzer(text)])

def preprocess_with_whoosh_analyzer_entity(text):
    return " ".join([t.text for t in analyzer_named_entity(text)])

# Exemplo de uso
documents_to_index = get_documents_to_index()

print("Conectando ao servidor Elasticsearch...")

# Conectando ao Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

print("Conexão estabelecida, indexando documentos...")

start_time = time.perf_counter()

actions = [
    {
        "_index": "motor-1",
        "_id": doc["id"],
        "_source": {
            "title": doc["title"],
            "content": preprocess_with_whoosh_analyzer(doc["content"]),
            "entity": preprocess_with_whoosh_analyzer_entity(doc["content"]),
        }
    }
    for doc in documents_to_index
]

print("Fazendo a indexação....")

response = helpers.bulk(es, actions)

print(f"Documentos indexados com sucesso!")
print(f"Tempo total de indexação: {time.perf_counter() - start_time:.4f} segundos")