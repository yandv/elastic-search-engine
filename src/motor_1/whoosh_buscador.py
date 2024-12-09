from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from whoosh.index import open_dir

from whoosh.scoring import BM25F 
from whoosh.qparser import MultifieldParser

from analyzer import whoosh_index_address


import os
import time

if not os.path.exists(whoosh_index_address):
    print("Índice não encontrado, execute o indexador.py primeiro")
    exit(1)
    
stop_words = set(stopwords.words("english"))

print("Abrindo índice...")

ix = open_dir(whoosh_index_address)

# get oq deve ser buscado do input

search = input("Digite o termo que deseja buscar: ")

if (search == ""):
    print("Digite um termo para buscar")
    exit(1)

tokens = word_tokenize(search.lower())
tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
bigrams = list(bigrams(tokens))


## add synon
print(f"Procurando resultados para a consulta \"{search}\", inicializando index searcher...")

with ix.searcher(weighting=BM25F) as searcher:
    start_time = time.perf_counter()
    
    times = []
    
    for bigram in bigrams[:3]:
        start_time_search = time.perf_counter()
        # query = Or(And([Term("title", bigram[0]), Term("title", bigram[1])]), And([Term("content", bigram[0]), Term("content", bigram[1])]))
        query = MultifieldParser(["title", "content"], ix.schema).parse(f"{bigram[0]} {bigram[1]}")
        
        print(query)
        results = searcher.search(query)
        
        print(f"Foram encontrados {len(results)} resultados para sua consulta, tempo de busca {time.perf_counter() - start_time_search:.4f} segundos")
        times.append(time.perf_counter() - start_time_search)
        
        for hit in results:
            print("ID: ", hit["id"])
            # print("Título: ", hit["title"])
            # print("Conteúdo: ", hit["content"])
            print("Revelância: ", hit.score)
            print()
        
        print("--------------------------------------------------")
    
    print(f"Tempo total de busca: {time.time() - start_time:.4f} segundos")