from __future__ import division
import requests, json

class Merchant:
    LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

    def bItem(self, item):
        itemJson = json.loads(requests.get(self.LIST_API.format(item['id'])).content)
        itemWait = itemJson['buys'][0]['unit_price']
        itemInst = itemJson['sells']
        waitCost = itemWait * item['quantity']
        instCost = 0
        instRemd = item['quantity']
        for i in range(len(itemInst)):
            currentEntry = itemInst[i]
            ## Successfully finish buying.
            if currentEntry['quantity'] >= instRemd:
                instCost += instRemd * currentEntry['unit_price']
                instRemd  = 0
                break
            ## Insufficient supply, extrapolated result.
            elif i == len(itemInst):
                instCost += instRemd * currentEntry['unit_price']
                instRemd  = 0
                break
            ## Main loop.
            else:
                instCost += currentEntry['quantity'] * currentEntry['unit_price']
                instRemd -= currentEntry['quantity']
            #endelse
        #endfor
        waitPrices = { 'totalPrice': waitCost, 'unitPrice': itemWait }
        instPrices = { 'totalPrice': instCost, 'unitPrice': instCost / item['quantity'] }
        return { 'order': waitPrices, 'instant': instPrices }
    #enddef

    def sItem(self, item):
        itemJson = json.loads(requests.get(self.LIST_API.format(item['id'])).content)
        itemWait = itemJson['sells'][0]['unit_price']
        itemInst = itemJson['buys']
        waitGain = itemWait * item['quantity']
        instGain = 0
        instRemd = item['quantity']
        for i in range(len(itemInst)):
            currentEntry = itemInst[i]
            ## Successfully finish selling.
            if currentEntry['quantity'] >= instRemd:
                instGain += instRemd * currentEntry['unit_price']
                instRemd  = 0
                break
            ## Insufficient offers, extrapolated result.
            elif i == len(itemInst):
                instGain += instRemd * currentEntry['unit_price']
                instRemd  = 0
                break
            ## Main loop.
            else:
                instGain += currentEntry['quantity'] * currentEntry['unit_price']
                instRemd -= currentEntry['quantity']
            #endelse
        #endfor
        waitPrices = { 'totalPrice': waitGain * 0.85, 'unitPrice': itemWait }
        instPrices = { 'totalPrice': instGain * 0.85, 'unitPrice': instGain / item['quantity'] }
        return { 'order': waitPrices, 'instant': instPrices }
    #enddef

    def currencyConv(amount):
        copper = int(round(amount % 100))
        silver = int((amount % 10000) / 100)
        gold   = int(amount / 10000)
        sign   = '+' if amount >= 0 else '-'
        return '{} {}g {}s {}c'.format(sign, gold, silver, copper)
    #enddef

    def niceRound(num, maxDp):
        numComp = str(num).split('.')
        if float(num).is_integer():
            return int(num)
        elif len(numComp[1]) < maxDp:
            return num
        else:
            return float('{}.{}'.format(numComp[0], numComp[1][:maxDp]))
        #endelse
    #enddef
#endclass
