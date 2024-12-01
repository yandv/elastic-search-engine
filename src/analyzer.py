import json
import nltk
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

import matplotlib
from matplotlib import pyplot as plt

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
        documents = [doc for doc in json.load(f) if doc.get('type') == 'source-document']
    
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(process_document, doc) for doc in documents]
        
        for future in as_completed(futures):
            try:
                result = future.result()  # Obtém o resultado da tarefa
                
                all_tokens.extend(result.get('tokens'))
                removed_stop_words.extend(result.get('removed_stop_words'))
                print(f"Processed {result.get('filename')}")
            except Exception as e:
                print(f"Erro ao processar documento: {e}")
                
    word_freq = Counter(all_tokens)
    stop_word_freq = Counter(removed_stop_words)
    
    sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_stop_freq = sorted(stop_word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return all_tokens, len(word_freq), sorted_freq, len(stop_word_freq), sorted_stop_freq

def plot_word_distribution(sorted_freq, max_words=50):
    """
    Create a log-log plot of word distribution
    
    Args:
        sorted_freq (list): List of (word, frequency) tuples sorted by frequency
    """
    
    words, frequencies = zip(*sorted_freq[:max_words])
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color="skyblue")
    
    plt.title("Distribuição de Frequência das Palavras", fontsize=16)
    plt.xlabel("Palavras", fontsize=14)
    plt.ylabel("Frequência", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)  # Rotaciona as palavras no eixo X para melhor legibilidade
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adiciona linhas de grade horizontais

    # Mostrar o gráfico
    plt.tight_layout()
    plt.show()

def main(json_file='/../resources/papers.json'):
    # Analyze word distribution
    all_tokens, vocab_size, sorted_freq, stop_word_vocab_size, sorted_stop_freq = analyze_word_distribution(os.path.dirname(__file__) + json_file)
    
    # Print basic statistics
    print(f"Total number of words: {len(all_tokens)}")
    print(f"Vocabulary size: {vocab_size}")
    print(f"Total number of stopwords: {stop_word_vocab_size}")
    
    # Print top 10 most frequent words
    print("\nTop 10 most frequent words:")
    for word, freq in sorted_freq[:10]:
        print(f"{word}: {freq}")
        
    print("\nTop 10 most frequent stopwords:")
    for word, freq in sorted_stop_freq[:10]:
        print(f"{word}: {freq}")
        
    # Print bottom 10 least frequent words
    print("\nBottom 10 least frequent words:")
    for word, freq in sorted_freq[-10:]:
        print(f"{word}: {freq}")
    
    
    print("\nBottom 10 least frequent stopwords:")
    for word, freq in sorted_stop_freq[-10:]:
        print(f"{word}: {freq}")
    
    # Plot word distribution
    plot_word_distribution(sorted_freq)
    plot_word_distribution(sorted_stop_freq)

if __name__ == "__main__":
    main()