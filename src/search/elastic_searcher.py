import time

class ElasticsearchSearcher:
    def __init__(self, indexer):
        """
        Initialize Elasticsearch Searcher
        
        :param indexer: ElasticsearchIndexer instance
        """
        self.es = indexer.es
        self.index_name = indexer.index_name
    
    def search(self, queries, top_k=10):
        """
        Search documents using Elasticsearch
        
        :param queries: List of query documents
        :param top_k: Number of top results to return
        :return: Search results
        """
        results = []
        
        for query_doc in queries:
            query_text = query_doc.get('cleaned_content', '')
            
            # Prepare Elasticsearch query
            es_query = {
                'query': {
                    'match': {
                        'content': {
                            'query': query_text,
                            'operator': 'or'
                        }
                    }
                },
                'size': top_k
            }
            
            # Measure search time
            start_time = time.time()
            search_response = self.es.search(
                index=self.index_name, 
                body=es_query
            )
            search_time = time.time() - start_time
            
            # Convert results
            doc_results = [
                {
                    'id': hit['_source']['id'],
                    'filename': hit['_source']['filename'],
                    'score': hit['_score']
                } 
                for hit in search_response['hits']['hits']
            ]
            
            results.append({
                'query_id': query_doc.get('id', ''),
                'results': doc_results,
                'search_time': search_time
            })
        
        return results