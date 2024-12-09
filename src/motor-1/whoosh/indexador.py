from whoosh import index
from analyzer import whoosh_schema as schema

from file_helper import get_source_documents

import os
import time

# Criando o índice
if not os.path.exists("/media/allanmxr/01DB1BE20861AF20/Users/Allan/woosh/motor-1.1"):
    os.mkdir("/media/allanmxr/01DB1BE20861AF20/Users/Allan/woosh/motor-1.1")

ix = index.create_in("/media/allanmxr/01DB1BE20861AF20/Users/Allan/woosh/motor-1.1", schema)

#extract id, title and content
documents_to_index = [{"id": doc['id'], "title": doc['title'], "content": doc['content']} for doc in get_source_documents()]

start_time = time.time()
times = []
print(f"Indexando {len(documents_to_index)} documentos, aguarde...")

writer = ix.writer()

for idx, doc in enumerate(documents_to_index):
    start_time = time.perf_counter()
    writer.add_document(**doc)    
    end_time = time.perf_counter()
    times.append(end_time - start_time)
    print(f"Indexado documento {doc['id']} em {times[len(times) - 1]:.4f} segundos ({(idx + 1) / len(documents_to_index) * 100:.2f}%)")

writer.commit(optimize=True)

print(f"Documentos indexados com sucesso!")
print(f"Tempo total de indexação: {time.time() - start_time:.4f} segundos")
print(f"Tempo médio de indexação: {sum(times) / len(times):.4f} segundos")

