import json
import nltk
import os

from matplotlib import pyplot as plt

from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('words')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Tokenizing
    3. Removing stopwords and non-alphabetic tokens
    """
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    all_tokens = []
    removed_stop_words = []
    
    for token in tokens:
        if not token.isalpha():
            continue
        if token in stop_words:
            removed_stop_words.append(token)
            continue
        all_tokens.append(token)
    
    return all_tokens, removed_stop_words

def process_document(doc):
    try:
        filepath = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'resources', 
            doc.get('type'), 
            doc.get('filename')
        )
        
        print(f"Processing {filepath}")
        
        with open(filepath) as f:
            content = f.read()
        tokens, removed_stop_words = preprocess_text(content)
        return {
            'filename': doc.get('filename'),
            'tokens': tokens,
            'removed_stop_words': removed_stop_words
        }
    except Exception as e:
        print(f"Erro ao processar documento: {doc.get('filename')} {e}")
        raise e

def analyze_word_distribution(json_file):
    """
    Analyze word distribution in the PAN-PC-11 dataset
    
    Args:
        json_file (str): Path to the papers.json file
    
    Returns:
        tuple: (total_words, vocabulary_size, word_frequencies)
    """
    all_tokens = []
    removed_stop_words = []
    
    with open(json_file, 'r', encoding='utf-8') as f:
        documents = [doc for doc in json.load(f) if doc.get('type') == 'source-document'][:500]
    
    for doc in documents:
        result = process_document(doc)
        
        all_tokens.extend(result.get('tokens'))
        removed_stop_words.extend(result.get('removed_stop_words'))
        print(f"Processed {result.get('filename')}")
        
        del result
        del doc
                
    word_freq = FreqDist(all_tokens)
    stop_word_freq = FreqDist(removed_stop_words)
    
    return all_tokens, len(word_freq), word_freq, len(stop_word_freq), stop_word_freq

def plot_word_distribution(sorted_freq, max_words=50):
    """
    Create a log-log plot of word distribution
    
    Args:
        sorted_freq (list): List of (word, frequency) tuples sorted by frequency
    """
    
    p = sorted_freq.plot(max_words,show=False,title=f'Distribuição das {max_words} palavras mais frequentes no corpus')
    p.set_xlabel("Amostra")
    p.set_ylabel("Frequência")
    plt.show()
    
def plot_word_distribution_loglog(sorted_freq, max_words=10000):
    """
    Create a log-log plot of word distribution
    
    Args:
        sorted_freq (list): List of (word, frequency) tuples sorted by frequency
    """
    
    p = sorted_freq.plot(max_words, show=False, title=f'Distribuição das {max_words} palavras mais frequentes no corpus (log-log)')
    p.set_xscale('log')
    p.set_yscale('log')
    p.set_xlabel("Amostra")
    p.set_ylabel("Frequência")
    plt.show()

def main(json_file='/../resources/papers.json'):
    # Analyze word distribution
    all_tokens, vocab_size, sorted_freq, stop_word_vocab_size, sorted_stop_freq = analyze_word_distribution(os.path.dirname(__file__) + json_file)
    
    
    # Print basic statistics
    print(f"Total number of words: {len(all_tokens)}")
    print(f"Vocabulary size: {vocab_size}")
    print(f"Total number of stopwords: {stop_word_vocab_size}")
    
    print("\nTop 30 most frequent words:")
    for word, freq in sorted_freq.most_common(30):
        print(f"{word}: {freq}")
        
    print("\nTop 30 most frequent stopwords:")
    for word, freq in sorted_stop_freq.most_common(30):
        print(f"{word}: {freq}")
    
    sorted_desc_freq = sorted(sorted_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_desc_stop_freq = sorted(sorted_stop_freq.items(), key=lambda x: x[1], reverse=True)
    
    print("\nBottom 30 least frequent words:")
    for word, freq in sorted_desc_freq[-30:]:
        print(f"{word}: {freq}")
    
    print("\nBottom 30 least frequent stopwords:")
    for word, freq in sorted_desc_stop_freq[-30:]:
        print(f"{word}: {freq}")
    
    # Plot word distribution
    plot_word_distribution(sorted_freq)
    plot_word_distribution(sorted_stop_freq)
    
    plot_word_distribution_loglog(sorted_freq)
    plot_word_distribution_loglog(sorted_stop_freq)

if __name__ == "__main__":
    main()