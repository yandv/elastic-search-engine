from nltk.corpus import  stopwords
from whoosh.analysis import Filter, RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.fields import Schema, TEXT, ID

import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

analyzer = (
    RegexTokenizer() 
    | LowercaseFilter() 
    | StopFilter(stoplist=stopwords.words("english")) 
    | NLTKSynonymFilter()
)

whoosh_schema = Schema(
    id=ID(unique=True, stored=True),
    title=TEXT(analyzer=analyzer, stored=True, field_boost=1.1),
    content=TEXT(analyzer=analyzer, stored=True)
)
