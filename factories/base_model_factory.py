__author__ = 'Konstantin Gritsenko <gritsenko.konstantin@gmail.com>'


class BaseModelFactory:
    def __init__(self):
        pass

    def get_model(self):
        """
        :rtype: model.base_model.BaseModel
        """
        raise Exception("Implement this method")