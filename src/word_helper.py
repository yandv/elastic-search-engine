from nltk.corpus import wordnet, stopwords
import nltk

nltk.download("wordnet")
nltk.download("omw-1.4")

stop_words = set(stopwords.words("english"))

synonyms_cache = {}

def get_synonyms(word):
    if word in synonyms_cache:
        return synonyms_cache[word]
    
    synonyms = set()  # Usamos um set para evitar duplicatas
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())  # Adiciona o nome do sinônimo
    synonyms.discard(word)  # Remove a própria palavra da lista
    synonyms_cache[word] = synonyms
    return synonyms