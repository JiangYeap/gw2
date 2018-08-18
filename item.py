class Item:
    def __init__(self, info):
        self._id = info[0]
        self._name = info[1]
    #enddef

    def __getitem__(self, key):
        dict = {
            'id': self._id,
            'name': self._name
        }
        return dict[key]
    #enddef

    def set_id(self, newId):
        self._id = newId
    #enddef

    def set_name(self, newName):
        self._name = newName
    #enddef
#endclass
