class Item:
    def __init__(self, id, name, quantity=0):
        assert quantity >= 0
        self.__id = id
        self.__name = name
        self.__quantity = int(quantity)
    #enddef

    def __getitem__(self, key):
        if key == 'id': return self.__id
        elif key == 'name': return self.__name
        elif key == 'quantity': return self.__quantity
    #enddef

    def setId(self, newId):
        self.__id = newId
    #enddef

    def setName(self, newName):
        self.__name = newName
    #enddef

    def setQuantity(self, newQuantity):
        assert newQuantity >= 0
        self.__quantity = int(newQuantity)
    #enddef
#endclass
