class BaseElasticSearchRepository(object):
    def __init__(self, elastic_search, index, doc_type, model_factory=None):
        """
        :type elastic_search: elasticsearch.client.Elasticsearch
        :type index: string
        :type doc_type: string
        :type model_factory: factories.base_model_factory.BaseModelFactory
        :return:
        """
        self._elastic_search = elastic_search
        self._index = index
        self._doc_type = doc_type
        self._model_factory = model_factory

    def get_model(self):
        """
        Instantiate model object to be filled in
        :rtype: model.base_model.BaseModel
        """
        return self._model_factory.get_model()

    def get_all_query(self):
        return self._elastic_search.search(index=self._index)

    def clear_indexes(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[400, 404])

    def create_index(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body, pretty=True)

    def delete_by_id(self, id):
        # TODO: fix errors
        self.es.delete(self.index, self.doc_type, id)

    def get_sources(self, elasticsearch_request):
        pass

    def _convert_search_with_higlight(self, search_result):
        res = []
        hits = search_result['hits']['hits']
        for hit in hits:
            item = self.get_model()
            item.init_from_search_result(hit)
            res.append(item)
        return res

    def search(self, query_string, fields=['content']):
        list_dict_fields = []
        for i in fields:
            list_dict_fields.append({i: {}})
        query = {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": fields,
                    "operator": "and"
                }
            },
            "highlight": {
                "fields": list_dict_fields,
                "require_field_match": 'false'
            }
        }
        return self._convert_search_with_higlight(self._elastic_search.search(self._index, body=query))
