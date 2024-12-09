from nltk.corpus import  stopwords
from whoosh.analysis import Filter, RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.fields import Schema, TEXT, ID

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_helper import get_source_documents
from word_helper import get_synonyms

class NLTKSynonymFilter(Filter):
    def __call__(self, tokens):
        for token in tokens:
            yield token  # Retorna o token original
            synonyms = get_synonyms(token.text)         
            for synonym in synonyms:  # Obtém os sinônimos
                new_token = token.copy()
                new_token.text = synonym
                yield new_token  # Retorna cada sinônimo como novo token

class RemoveDuplicateFilter(Filter):
    def __call__(self, tokens):
        seen = set()
        for token in tokens:
            if token.text not in seen:
                seen.add(token.text)
                yield token

analyzer = (
    RegexTokenizer() 
    | LowercaseFilter() 
    | StopFilter(stoplist=stopwords.words("english")) 
    | NLTKSynonymFilter()
    | RemoveDuplicateFilter()
)

whoosh_schema = Schema(
    id=ID(unique=True, stored=True),
    title=TEXT(analyzer=analyzer, stored=True, field_boost=1.1),
    content=TEXT(analyzer=analyzer, stored=True)
)



if __name__ == '__main__':
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