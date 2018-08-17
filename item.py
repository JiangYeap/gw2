class Item:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name
    #enddef

    def __getitem__(self, key):
        dict = {
            'id': self.__id,
            'name': self.__name
        }
        return dict[key]
    #enddef

    def setId(self, newId):
        self.__id = newId
    #enddef

    def setName(self, newName):
        self.__name = newName
    #enddef
#endclass
