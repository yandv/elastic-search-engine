import json
import nltk
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Tokenizing
    3. Removing stopwords and non-alphabetic tokens
    """
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    
    return tokens

def process_document(doc):
    try:
        if doc.get('type') == 'source-document':
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
            tokens = preprocess_text(content)
            return tokens
        return []
    except Exception as e:
        print(f"Erro ao processar documento: {doc.get('filename')}")
        return []

def analyze_word_distribution(json_file):
    """
    Analyze word distribution in the PAN-PC-11 dataset
    
    Args:
        json_file (str): Path to the papers.json file
    
    Returns:
        tuple: (total_words, vocabulary_size, word_frequencies)
    """
    # Initialize counters
    all_tokens = []
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    with ThreadPoolExecutor(max_workers=320) as executor:
        # Submeter as tarefas ao pool de threads
        futures = [executor.submit(process_document, doc) for doc in documents]
        
        # Aguarda as tarefas serem concluídas e agrega os resultados
        for future in as_completed(futures):
            try:
                tokens = future.result()  # Obtém o resultado da tarefa
                all_tokens.extend(tokens)
            except Exception as e:
                print(f"Erro ao processar documento: {e}")
    
    # Count word frequencies
    word_freq = Counter(all_tokens)
    
    # Sort frequencies in descending order
    sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return all_tokens, len(word_freq), sorted_freq

def plot_word_distribution(sorted_freq):
    """
    Create a log-log plot of word distribution
    
    Args:
        sorted_freq (list): List of (word, frequency) tuples sorted by frequency
    """
    frequencies = [freq for _, freq in sorted_freq]
    ranks = list(range(1, len(frequencies) + 1))
    
    plt.figure(figsize=(12, 6))
    plt.loglog(ranks, frequencies, marker='o')
    plt.title("Word Distribution in PAN-PC-11 Corpus (Zipf's Law)")
    plt.xlabel("Rank (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.tight_layout()
    plt.show()

def main(json_file='/../resources/papers.json'):
    # Analyze word distribution
    all_tokens, vocab_size, sorted_freq = analyze_word_distribution(os.path.dirname(__file__) + json_file)
    
    # Print basic statistics
    print(f"Total number of words: {len(all_tokens)}")
    print(f"Vocabulary size: {vocab_size}")
    
    # Print top 10 most frequent words
    print("\nTop 10 most frequent words:")
    for word, freq in sorted_freq[:10]:
        print(f"{word}: {freq}")
    
    # Print bottom 10 least frequent words
    print("\nBottom 10 least frequent words:")
    for word, freq in sorted_freq[-10:]:
        print(f"{word}: {freq}")
    
    # Plot word distribution
    plot_word_distribution(sorted_freq)

if __name__ == "__main__":
    main()