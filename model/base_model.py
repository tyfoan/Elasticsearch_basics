__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class BaseModel:
    def __init__(self, object_id=None):
        """
        :type object_id: string
        """
        self.id = object_id

    def init_from_search_result(self, search_result_item):
        """
        :type search_result_item: dict
        :rtype: model.base_model.BaseModel
        """
        self.id = search_result_item['_id']
        source = search_result_item['_source']
        highlight = search_result_item['highlight'] if 'highlight' in search_result_item else None
        for key in source.keys():
            if hasattr(self, key):
                source_value = source[key]
                highlight_value = highlight.get(key) if highlight else None
                value = highlight_value[0] if highlight_value else source_value
                setattr(self, key, value)
        return self
