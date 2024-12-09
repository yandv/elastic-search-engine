from analyzer import analyzer
from file_helper import get_source_documents

import time

documents_to_index = [{"id": doc['id'], "title": doc['title'], "content": doc['content']} for doc in get_source_documents()]
times = []

for idx, doc in enumerate(documents_to_index):
    start_time = time.perf_counter()
    
    tokens = [token.text for token in analyzer(doc['content'])]
    
    end_time = time.perf_counter()
    times.append(end_time - start_time)
    
    print(f"Documento {doc['id']} pré-processado em {times[len(times) - 1]:.4f} segundos ({(idx + 1) / len(documents_to_index) * 100:.2f}%)")

print(f"Tempo total gasto: {sum(times):.4f} segundos")
print(f"Tempo médio gasto: {sum(times) / len(times):.4f} segundos")