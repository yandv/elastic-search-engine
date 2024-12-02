import json
import nltk
import os
from functools import reduce

import matplotlib
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

def load_documents(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return [doc for doc in json.load(f) if doc.get('type') == 'source-document']

def analyze_word_distribution(json_file):
    """
    Analyze word distribution in the PAN-PC-11 dataset
    
    Args:
        json_file (str): Path to the papers.json file
    
    Returns:
        tuple: (total_words, vocabulary_size, word_frequencies)
    """
    
    tokens = FreqDist()
    stop_words = FreqDist()
    
    for idx, doc in enumerate(load_documents(json_file)):
        file_name = doc.get('filename')
            
        print(f"Processing {file_name}")
        
        filepath = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'resources', 
            doc.get('type'), 
            file_name
        )
        
        
        with open(filepath) as f:
            content = f.read()
                
        text_tokens, removed_stop_words = preprocess_text(content)
        
        for token in text_tokens:
            tokens[token] += 1
        
        for stop_word in removed_stop_words:
            stop_words[stop_word] += 1
        
        del content
        del text_tokens
        del removed_stop_words
        
        print(f"Finished processing {file_name} ({(idx + 1)/len(load_documents(json_file)):.2%})")
                
    
    return tokens, stop_words

def plot_word_distribution(sorted_freq, max_words=100):
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
    words_freq, stop_word_freq = analyze_word_distribution(os.path.dirname(__file__) + json_file)
    
    
    # Print basic statistics
    print(f"Total number of words: {reduce(lambda x, y: x + y, words_freq.values()) + reduce(lambda x, y: x + y, stop_word_freq.values())}")
    print(f"Vocabulary size: {len(words_freq.items()) + len(stop_word_freq.items())}")
    print(f"Total number of stopwords: {len(stop_word_freq.items())}")
    
    print("\nTop 30 most frequent words:")
    for word, freq in words_freq.most_common(30):
        print(f"{word}: {freq}")
        
    print("\nTop 30 most frequent stopwords:")
    for word, freq in stop_word_freq.most_common(30):
        print(f"{word}: {freq}")
    
    sorted_desc_freq = sorted(words_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_desc_stop_freq = sorted(stop_word_freq.items(), key=lambda x: x[1], reverse=True)
    
    print("\nBottom 30 least frequent words:")
    for word, freq in sorted_desc_freq[-30:]:
        print(f"{word}: {freq}")
    
    print("\nBottom 30 least frequent stopwords:")
    for word, freq in sorted_desc_stop_freq[-30:]:
        print(f"{word}: {freq}")
    
    # Plot word distribution
    plot_word_distribution(words_freq)
    plot_word_distribution(stop_word_freq)
    
    plot_word_distribution_loglog(words_freq)
    plot_word_distribution_loglog(stop_word_freq)

if __name__ == "__main__":
    main()