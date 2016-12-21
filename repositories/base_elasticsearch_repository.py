class BaseElasticSearchRepository(object):
    def __init__(self, elastic_search):
        self._elastic_search = elastic_search
        self._index = None
        self._doc_type = None
        # Fields can be extended

    def get_all_query(self):
        return self._elastic_search.search(index=self._index)

    def clear_indexes(self):
        self._elastic_search.indices.delete(index=self._index, ignore=[400, 404])

    def create_index(self, body):
        self._elastic_search.index(index=self._index, doc_type=self._doc_type, body=body, pretty=True)

    def delete_by_id(self, id):
        self.es.delete(self.index, self.doc_type, id)

    def get_sources(self, elasticsearch_request):
        pass

    def _convert_search_with_higlight(self, search_result):
        res = []
        hits = search_result['hits']['hits']
        for hit in hits:
            item = {'id': hit['_id']}
            item.update(hit['_source'])
            if 'highlight' in hit:
                [item.update({k: v[0]}) for k, v in hit['highlight'].items()]  # OVERWRITING?
            # fields = hit['_source']
            # if 'highlight' in hit:
            #     item['highlight'] = hit['highlight']
            # for key in fields.keys():
            #     item[key] = fields[key]
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
