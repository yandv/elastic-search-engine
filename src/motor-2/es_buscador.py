from elasticsearch import Elasticsearch

def search_documents(query_term, es_host="http://localhost:9200", index_name="motor-1"):
    es = Elasticsearch([es_host])
    
    search_query = {
        "from": 0,
        "size": 10,
        "sort": {
            "_score": "desc"
        },
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": query_term}},
                    {"match": {"content": query_term}},
                    {"match": {"entity": query_term}}
                ]
            }
        }
    }
    
    response = es.search(index=index_name, body=search_query)
    
    return response

if __name__ == "__main__":
    user_query = input("Digite um termo de busca: ")
    
    results = search_documents(user_query)
    
    print("Resultados da busca:")
    for hit in results["hits"]["hits"]:
        doc_id = hit["_id"]
        title = hit["_source"].get("title", "Sem título")
        content = hit["_source"].get("content", "")
        score = hit["_score"]
        print(f"ID: {doc_id}, Score: {score}")
        print(f"Título: {title}")
        print(f"Conteúdo: {content[:200]}...")
        print("-" * 50)