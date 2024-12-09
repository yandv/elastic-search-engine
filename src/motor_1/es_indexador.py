from elasticsearch import Elasticsearch, helpers
from analyzer import analyzer, get_documents_to_index

import time

def preprocess_with_whoosh_analyzer(text):
    return " ".join([t.text for t in analyzer(text)])

# Exemplo de uso
documents_to_index = get_documents_to_index()

# Conectando ao Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

start_time = time.perf_counter()

actions = [
    {
        "_index": "motor-1",
        "_id": doc["id"],
        "_source": {
            "title": doc["title"],
            "content": preprocess_with_whoosh_analyzer(doc["content"])
        }
    }
    for doc in documents_to_index
]

response = helpers.bulk(es, actions)

print(f"Documentos indexados com sucesso!")
print(f"Tempo total de indexação: {time.perf_counter() - start_time:.4f} segundos")