from elasticsearch import Elasticsearch, helpers
from analyzer import analyzer

import time

def preprocess_with_whoosh_analyzer(text):
    return " ".join([t.text for t in analyzer(text)])

# Exemplo de uso
documents_to_index = [
        {"id": 1, "title": "Document title", "content": "Document content example for elasticsearch indexing test"},
        {"id": 2, "title": "Another document title", "content": "Another document content example for elasticsearch indexing test"},
        {"id": 3, "title": "Yet another document title", "content": "Yet another document content example for elasticsearch indexing test"}
    ]

actions = [
    {
        "_index": "motor-1",
        "_id": doc["id"],
        "_source": {
            "title": doc["title"],
            "content": doc["content"]
        }
    }
    for doc in documents_to_index
]

# Conectando ao Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

start_time = time.perf_counter()
response = helpers.bulk(es, actions)
print(f"Documentos indexados com sucesso!")
print(f"Tempo total de indexação: {time.perf_counter() - start_time:.4f} segundos")