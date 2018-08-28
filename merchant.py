from __future__ import division
from quad import Quad, QuadComp
import requests, json

class Merchant(object):
    LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

    def trade(self, trade_type, item, quantity):
        item_link = self.LIST_API.format(item['id'])
        item_json = json.loads(requests.get(item_link).content)
        modifier = None
        if trade_type.lower() == 'b':
            item_ordr = item_json['buys'][0]['unit_price']
            item_inst = item_json['sells']
            modifier = 1
        elif trade_type.lower() == 's':
            item_ordr = item_json['sells'][0]['unit_price']
            item_inst = item_json['buys']
            modifier = 0.85
        ordr_totl = item_ordr * quantity
        inst_totl = self._complete_instant(item_inst, quantity)
        ordr_unit = self._round_whole((ordr_totl / quantity))
        inst_unit = self._round_whole((inst_totl / quantity))
        totl_price = QuadComp(ordr_totl * modifier, inst_totl * modifier)
        unit_price = QuadComp(ordr_unit, inst_unit)
        return Quad(totl_price, unit_price)

    def fixed_trade(self, trade_type, item, quantity, price):
        assert int(price) >= 0
        modifier = None
        if trade_type.lower() == 'b':
            modifier = 1
        elif trade_type.lower() == 's':
            modifier = 0.85
        ordr_totl = price * quantity
        inst_totl = price * quantity
        ordr_unit = self._round_whole(price)
        ordr_unit = self._round_whole(price)
        totl_price = QuadComp(ordr_totl * modifier, inst_totl * modifier)
        unit_price = QuadComp(ordr_unit, inst_unit)
        return Quad(totl_price, unit_price)

    def currency_conv(self, amount):
        abs_value = abs(amount)
        rounded = self._round_whole(abs_value)
        copper = rounded % 100
        silver = int((rounded % 10000) / 100)
        gold = int(rounded / 10000)
        sign = '+' if amount >= 0 else '-'
        return '{} {}g {}s {}c'.format(sign, gold, silver, copper)

    def _complete_instant(self, listing, remainder):
        value = 0
        for i in range(len(listing)):
            curr_item = listing[i]
            if curr_item['quantity'] >= remainder:
                value += remainder * curr_item['unit_price']
                remainder = 0
                break
            elif i == len(listing):
                value += remainder * curr_item['unit_price']
                remainder = 0
                break
            else:
                value += curr_item['quantity'] * curr_item['unit_price']
                remainder -= curr_item['quantity']
            #endelse
        return value

    def _round_whole(self, num):
        return int(round(num))
    #enddef
