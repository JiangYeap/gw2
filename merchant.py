from __future__ import division
import requests, json

class Merchant(object):
    LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

    def trade(self, type, item, quantity):
        item_link = self.LIST_API.format(item['id'])
        item_json = json.loads(requests.get(item_link).content)
        if type.lower() == 'b':
            item_ordr = item_json['buys'][0]['unit_price']
            item_inst = item_json['sells']
            modifier = 1
        elif type.lower() == 's':
            item_ordr = item_json['sells'][0]['unit_price']
            item_inst = item_json['buys']
            modifier = 0.85
        ordr_totl = item_ordr * quantity
        inst_totl = self._complete_instant(item_inst, quantity)
        ordr_unit = int(round((ordr_totl / quantity)))
        inst_unit = int(round((inst_totl / quantity)))
        totl_price = {'O': ordr_totl * modifier, 'I': inst_totl * modifier}
        unit_price = {'O': ordr_unit, 'I': inst_unit}
        return {'T': totl_price, 'U': unit_price}

    def currency_conv(self, amounit):
        copper = int(round(amounit % 100))
        silver = int((amounit % 10000) / 100)
        gold = int(amounit / 10000)
        sign = '+' if amounit >= 0 else '-'
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
    #enddef
