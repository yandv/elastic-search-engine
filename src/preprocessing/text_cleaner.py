import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem import WordNetLemmatizer

synonyms_limit = 4

lemmatizer = WordNetLemmatizer()

def expands_query(tokens):
    """
    Expands query by adding synonyms
    """
    expanded = []
    
    for token in tokens:
        synsets = nltk.corpus.wordnet.synsets(token)
        # Adiciona sinônimos
        synonyms = set([lemma.name() for syn in synsets for lemma in syn.lemmas()])
        expanded.extend([token] + list(synonyms)[:synonyms_limit])  # Limita a 2 sinônimos
    
    return list(set(expanded))

def clean_text(text):
    """
    Clean and preprocess text for indexing
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    tokens = expands_query(tokens)
    
    return ' '.join(tokens)
