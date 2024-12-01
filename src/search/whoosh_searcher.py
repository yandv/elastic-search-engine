import time
from whoosh.index import open_dir  # Adicione open_dir aqui
from whoosh.qparser import QueryParser

max_terms = 250
class WhooshSearcher:
    def __init__(self, indexer):
        """
        Initialize Whoosh Searcher
        
        :param indexer: WhooshIndexer instance
        """
        self.indexer = indexer
        self.ix = open_dir(indexer.index_dir)
        
    def search(self, queries, top_k=10):
        """
        Search documents using Whoosh
        
        :param queries: List of query documents
        :param top_k: Number of top results to return
        :return: Search results
        """
        
        results = []
        
        with self.ix.searcher() as searcher:
            for query_doc in queries:
                query_text = query_doc.get('cleaned_content', '').strip()
                
                if not query_text:
                    continue
                
                    
                terms = query_text.split()
                batched_queries = [terms[i:i + max_terms] for i in range(0, len(terms), max_terms)]
                
                all_results = []
                search_time = time.time()
                
                for batch in batched_queries:
                    query = QueryParser('content', self.ix.schema).parse(' '.join(batch))
                    
                    search_results = searcher.search(query, limit=top_k)
                    all_results.extend(search_results)
                
                unique_results = list({r.docnum: r for r in all_results}.values())
                
                # Convert results
                doc_results = map(lambda r: {
                    'id': r['id'],
                    'filename': r['filename'],
                    'score': r.score
                }, unique_results)
                
                results.append({
                    'query_id': query_doc.get('id', ''),
                    'results': doc_results,
                    'search_time': search_time
                })
        
        return results