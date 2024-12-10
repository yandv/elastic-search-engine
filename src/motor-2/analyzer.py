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

import nltk
from nltk import ne_chunk, pos_tag, word_tokenize, tree

class NLTKNamedEntityFilter(Filter):
    def __call__(self, tokens):
        token_list = list(tokens)
        original_text = " ".join(t.text for t in token_list)
        
        nltk_tokens = word_tokenize(original_text)
        pos_tags = pos_tag(nltk_tokens)
        chunks = ne_chunk(pos_tags, binary=False)  
        
        ent_map = [None] * len(token_list)
        
        w_idx = 0
        
        def traverse_tree(chunks):
            nonlocal w_idx
            for chunk in chunks:
                if isinstance(chunk, tree.Tree):
                    ent_label = chunk.label()
                    for leaf in chunk.leaves():
                        if w_idx < len(ent_map):
                            ent_map[w_idx] = ent_label
                            w_idx += 1
                else:
                    if w_idx < len(ent_map):
                        w_idx += 1
        
        traverse_tree(chunks)
        
        for i, tok in enumerate(token_list):
            if ent_map[i] is not None:
                tok.ent_type = ent_map[i]
            yield tok


analyzer = (
    RegexTokenizer() 
    | LowercaseFilter() 
    | StopFilter(stoplist=stopwords.words("english")) 
    | NLTKSynonymFilter()
)

analyzer_named_entity = (
    RegexTokenizer() 
    | LowercaseFilter() 
    | StopFilter(stoplist=stopwords.words("english")) 
    | NLTKNamedEntityFilter()
)

whoosh_schema = Schema(
    id=ID(unique=True, stored=True),
    title=TEXT(analyzer=analyzer, stored=True, field_boost=1.1),
    content=TEXT(analyzer=analyzer, stored=True),
    entity=TEXT(analyzer=analyzer_named_entity, stored=True, field_boost=1.5)
)

whoosh_index_address = "whoosh-index"

def get_documents_to_index():
    return [{"id": doc['id'], "title": doc['title'], "content": doc['content']} for doc in get_source_documents()]

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
