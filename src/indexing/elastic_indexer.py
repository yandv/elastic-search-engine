import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ElasticsearchIndexer:
    def __init__(self, config):
        """
        Initialize Elasticsearch Indexer
        
        :param config: Dictionary containing indexing parameters
        """
        self.es = Elasticsearch(['http://localhost:9200'])
        self.index_name = 'plagiarism_documents'
        self.config = config
        
        # Create index with custom settings
        index_settings = {
            'settings': {
                'analysis': {
                    'analyzer': {
                        'custom_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'standard',
                            'filter': ['lowercase', 'stop']
                        }
                    }
                }
            },
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'content': {
                        'type': 'text', 
                        'analyzer': 'custom_analyzer',
                    },
                    'filename': {'type': 'keyword'},
                    'type': {'type': 'keyword'}
                }
            }
        }
        
        # Delete existing index if it exists
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
        
        # Create new index
        self.es.indices.create(index=self.index_name, body=index_settings)
    
    def index(self, documents):
        """
        Index documents in Elasticsearch
        
        :param documents: List of documents to index
        """
        def document_generator():
            for doc in documents:
                yield {
                    '_index': self.index_name,
                    '_id': doc.get('id', ''),
                    '_source': {
                        'id': doc.get('id', ''),
                        'content': doc.get('cleaned_content', ''),
                        'filename': doc.get('filename', ''),
                        'type': doc.get('type', '')
                    }
                }
        
        start_time = time.time()
        
        # Bulk indexing
        success, failed = bulk(self.es, document_generator())
        
        # Refresh index to make documents searchable immediately
        self.es.indices.refresh(index=self.index_name)
        
        indexing_time = time.time() - start_time
        return {
            'total_documents': len(documents),
            'indexing_time': indexing_time,
            'success': success,
            'failed': len(failed)
        }