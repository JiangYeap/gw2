from __future__ import division
import time

class Quad(object):
    def __init__(self, totl_price, unit_price):
        assert type(totl_price) is QuadComp
        assert type(unit_price) is QuadComp
        self._totl_price = totl_price
        self._unit_price = unit_price

    def __sub__(self, other):
        assert type(other) is Quad
        totl_price = self.get_totl_price() - other.get_totl_price()
        unit_price = self.get_inst_price() - other.get_inst_price()
        return Quad(totl_price, unit_price)

    def __truediv__(self, num):
        assert isinstance(num, (int, long, float))
        totl_price = self.get_totl_price() / num
        unit_price = self.get_inst_price() / num
        return Quad(totl_price, unit_price)

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

class QuadComp(object):
    def __init__(self, ordr_price, inst_price):
        assert isinstance(ordr_price, (int, long, float))
        assert isinstance(inst_price, (int, long, float))
        self._ordr_price = ordr_price
        self._inst_price = inst_price

    def __sub__(self, other):
        assert type(other) is QuadComp
        ordr_price = self.get_ordr_price() - other.get_ordr_price()
        inst_price = self.get_inst_price() - other.get_inst_price()
        return QuadComp(ordr_price, inst_price)

    def __mul__(self, num):
        assert isinstance(num, (int, long, float))
        ordr_price = self.get_ordr_price() * num
        inst_price = self.get_inst_price() * num
        return QuadComp(ordr_price, inst_price)

    def __truediv__(self, other):
        if isinstance(other, (int, long, float)):
            ordr_price = self.get_ordr_price() / other
            inst_price = self.get_inst_price() / other
        elif type(other) is QuadComp:
            ordr_price = self.get_ordr_price() / other.get_ordr_price()
            inst_price = self.get_inst_price() / other.get_inst_price()
        return QuadComp(ordr_price, inst_price)

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
