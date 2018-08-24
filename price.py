class Price(object):
    def __init__(self, totl_price, unit_price):
        assert type(totl_price) is PriceComp
        assert type(unit_price) is PriceComp
        self._totl_price = totl_price
        self._unit_price = unit_price

    def __getitem__(self, key):
        dict = {
            't': self._totl_price,
            'u': self._unit_price
        }
        return dict[key.lower()]

    def get_totl_price(self):
        return self._totl_price

    def get_unit_price(self):
        return self._unit_price

    def set_totl_price(self, new_price):
        self._totl_price = new_price

    def set_unit_price(self, new_price):
        self._unit_price = new_price
    #enddef

class PriceComp(object):
    def __init__(self, ordr_price, inst_price):
        assert int(ordr_price) > 0
        assert int(inst_price) > 0
        self._ordr_price = ordr_price
        self._inst_price = inst_price

    def __getitem__(self, key):
        dict = {
            'o': self._ordr_price,
            'i': self._inst_price
        }
        return dict[key.lower()]

    def get_ordr_price(self):
        return self._ordr_price

    def get_inst_price(self):
        return self._inst_price

    def set_ordr_price(self, new_price):
        self._ordr_price = new_price

    def set_inst_price(self, new_price):
        self._inst_price = new_price
    #enddef
