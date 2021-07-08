from elasticsearch import Elasticsearch


class elasticSearch():

    def __init__(self, index_type: str, index_name: str):
        self.es = Elasticsearch("http://es01:9200/", http_auth=('elastic', 'changeme'))
        self.index_type = index_type
        self.index_name = index_name

    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    def insert_one(self, doc: dict):
        self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)

    def insert_array(self, docs: list):
        for doc in docs:
            self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)

    def search(self, query, count: int = 30):
        dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "text"]
                }
            },
            "highlight": {
                "fields": {
                    "text": {}
                }
            }
        }
        match_data = self.es.search(index=self.index_name, body=dsl, size=count)
        return match_data