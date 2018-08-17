from __future__ import division
import requests, json

class Merchant:
    LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

    def trade(self, type, item, quantity):
        itemJson = json.loads(
            requests.get(self.LIST_API.format(item['id'])).content)
        if type.lower() == 'b':
            itemWait = itemJson['buys'][0]['unit_price']
            itemInst = itemJson['sells']
            modifier = 1
        elif type.lower() == 's':
            itemWait = itemJson['sells'][0]['unit_price']
            itemInst = itemJson['buys']
            modifier = 0.85
        #endelif
        waitTotl = itemWait * quantity
        instTotl = self.completeInstant(itemInst, quantity)
        waitUnit = self.roundWhole(waitTotl / quantity)
        instUnit = self.roundWhole(instTotl / quantity)
        totlPrices = {'O': waitTotl * modifier, 'I': instTotl * modifier}
        unitPrices = {'O': waitUnit, 'I': instUnit}
        return {'totl': totlPrices, 'unit': unitPrices}
    #enddef

    def completeInstant(self, listing, remainder):
        value = 0
        for i in range(len(listing)):
            currentEntry = listing[i]
            ## Successfully finish selling.
            if currentEntry['quantity'] >= remainder:
                value += remainder * currentEntry['unit_price']
                remainder = 0
                break
            ## Insufficient offers, extrapolated result.
            elif i == len(listing):
                value += remainder * currentEntry['unit_price']
                remainder = 0
                break
            ## Main loop.
            else:
                value += currentEntry['quantity'] * currentEntry['unit_price']
                remainder -= currentEntry['quantity']
            #endelse
        #endfor
        return value
    #enddef

    def currencyConv(self, amount):
        copper = int(round(amount % 100))
        silver = int((amount % 10000) / 100)
        gold   = int(amount / 10000)
        sign   = '+' if amount >= 0 else '-'
        return '{} {}g {}s {}c'.format(sign, gold, silver, copper)
    #enddef

    def roundWhole(self, num):
        return int(round(num))
    #enddef
#endclass
