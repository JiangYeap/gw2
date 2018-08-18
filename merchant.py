from __future__ import division
import requests, json

class Merchant:
    LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

    def currency_conv(self, amount):
        copper = int(round(amount % 100))
        silver = int((amount % 10000) / 100)
        gold = int(amount / 10000)
        sign = '+' if amount >= 0 else '-'
        return '{} {}g {}s {}c'.format(sign, gold, silver, copper)
    #enddef

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
        #endecurr_itemf
        ordr_ttl = item_ordr * quantity
        inst_ttl = self._complete_instant(item_inst, quantity)
        ordr_unt = int(round((ordr_ttl / quantity)))
        inst_unt = int(round((inst_ttl / quantity)))
        ttl_price = {'O': ordr_ttl * modifier, 'I': inst_ttl * modifier}
        unt_price = {'O': ordr_unt, 'I': inst_unt}
        return {'T': ttl_price, 'U': unt_price}
    #enddef

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
        #endfor
        return value
    #enddef
#endclass
