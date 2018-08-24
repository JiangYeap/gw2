class Item(object):
    def __init__(self, info):
        self._id = info[0]
        self._name = info[1]

    def __getitem__(self, key):
        dict = {
            'id': self._id,
            'name': self._name
        }
        return dict[key.lower()]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_id(self, new_id):
        self._id = new_id

    def set_name(self, new_name):
        self._name = new_name
    #enddef
