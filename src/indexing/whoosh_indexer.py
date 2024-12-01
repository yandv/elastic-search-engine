import os
import json
import time
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer

class WhooshIndexer:
    def __init__(self, config):
        """
        Initialize Whoosh Indexer with configuration
        
        :param config: Dictionary containing indexing parameters
        """
        self.index_dir = 'whoosh_index'
        self.config = config
        
        # Choose analyzer based on configuration
        analyzer = StandardAnalyzer(minsize=config.get('min_word_length', 3))
        
        # Create schema 
        schema_fields = {
            'id': ID(stored=True, unique=True),
            'content': TEXT(
                stored=True, 
                analyzer=analyzer
            ),
            'filename': STORED,
            'type': STORED
        }
        
        self.schema = Schema(**schema_fields)
        
        # Ensure index directory exists
        os.makedirs(self.index_dir, exist_ok=True)
        
    def index(self, documents):
        """
        Index documents using Whoosh
        
        :param documents: List of documents to index
        """
        # Create index
        ix = create_in(self.index_dir, self.schema)
        writer = ix.writer()
        
        start_time = time.time()
        
        # Index documents
        for doc in documents:
            writer.add_document(
                id=doc.get('id', ''),
                content=doc.get('cleaned_content', ''),
                filename=doc.get('filename', ''),
                type=doc.get('type', '')
            )
        
        writer.commit()
        
        indexing_time = time.time() - start_time
        return {
            'total_documents': len(documents),
            'indexing_time': indexing_time
        }