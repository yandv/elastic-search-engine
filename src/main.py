import json
import os
import nltk
import time
from preprocessing.text_cleaner import clean_text
from indexing.whoosh_indexer import WhooshIndexer
from indexing.elastic_indexer import ElasticsearchIndexer
from search.whoosh_searcher import WhooshSearcher
from search.elastic_searcher import ElasticsearchSearcher
from evaluation.metrics import calculate_precision_at_k, calculate_recall_at_k

def load_file_content(document):
    """
    Load content from file
    """
    with open(os.path.dirname(__file__) + '/../resources/' + document.get('type') + '/' + document.get('filename')) as f:
        content = f.read()
        
        return content, clean_text(content)

def load_documents(json_path):
    """
    Load documents from JSON file, separating source and suspicious documents
    """
    with open(json_path, 'r') as f:
        documents = json.load(f)[:250]
    
    print(f"Loaded {len(documents)} documents")
    
    for doc in documents:
        doc['id'] = doc.get('filename').split('.')[0]
        content, cleaned_content = load_file_content(doc)
        doc['content'] = content
        doc['cleaned_content'] = cleaned_content
    
    source_docs = [doc for doc in documents if doc.get('type') == 'source-document']
    suspicious_docs = [doc for doc in documents if doc.get('type') == 'suspicious-document']
    
    return source_docs, suspicious_docs

# Example usage in main script
def main():
    
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    
    print('Loading source and suspicious documents...')
    
    start_time = time.time()
    
    # Separate source and suspicious documents
    source_docs, suspicious_docs = load_documents(os.path.dirname(__file__) + '/../resources/papers.json')
    
    print(f"Loaded {len(source_docs)} source documents and {len(suspicious_docs)} suspicious documents in {time.time() - start_time:.2f} seconds\n")
    
    config = {
        'name': 'advanced_config',
        'min_word_length': 3,
        'analyzer': 'snowball'
    }
    
    print(f"Starting routine with configuration: {config['name']}\n")
    # Whoosh
    whoosh_indexer = WhooshIndexer(config)
    whoosh_index_stats = whoosh_indexer.index(source_docs)
    
    whoosh_searcher = WhooshSearcher(whoosh_indexer)
    whoosh_search_results = whoosh_searcher.search(suspicious_docs)
    
    # Elasticsearch
    # elasticsearch_indexer = ElasticsearchIndexer(config)
    # elasticsearch_index_stats = elasticsearch_indexer.index(source_docs)
    
    # elasticsearch_searcher = ElasticsearchSearcher(elasticsearch_indexer)
    # elasticsearch_search_results = elasticsearch_searcher.search(suspicious_docs)
    
    # Print results
    # print("Whoosh Indexing Stats:", whoosh_index_stats)
    # print("Whoosh Search Results:", whoosh_search_results)
    # print("Elasticsearch Indexing Stats:", elasticsearch_index_stats)
    # print("Elasticsearch Search Results:", elasticsearch_search_results.get('id'), elasticsearch_search_results.get('search_time'))
    print("")
    print("")

if __name__ == "__main__":
    main()