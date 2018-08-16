from __future__ import division
import requests, json

LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

def currencyConv(amount):
    copper = int(round(amount % 100))
    silver = int((amount % 10000) / 100)
    gold   = int(amount / 10000)
    sign   = '+' if amount >= 0 else '-'

    return '{} {}g {}s {}c'.format(sign, gold, silver, copper)
#enddef

def bOrdr(itemId, quantity):
    matsJson = json.loads(requests.get(LIST_API.format(itemId)).content)
    matsWait = matsJson['buys'][0]['unit_price']
    matsCost = matsWait * quantity

    return { 'totalPrice': matsCost , 'unitPrice': matsWait }
#enddef

def bInst(itemId, quantity):
    matsJson = json.loads(requests.get(LIST_API.format(itemId)).content)
    matsInst = matsJson['sells']
    matsCost = 0
    matsRemd = quantity

    for i in range(len(matsInst)):
        currentEntry = matsInst[i]
        ## Successfully finish buying.
        if currentEntry['quantity'] >= matsRemd:
            matsCost += matsRemd * currentEntry['unit_price']
            matsRemd  = 0
            break
        ## Insufficient supply, extrapolated result.
        elif i == len(matsInst):
            matsCost += matsRemd * currentEntry['unit_price']
            matsRemd  = 0
            break
        ## Main loop.
        else:
            matsCost += currentEntry['quantity'] * currentEntry['unit_price']
            matsRemd -= currentEntry['quantity']
        #endelse
    #endfor

    return { 'totalPrice': matsCost , 'unitPrice': matsCost / quantity }
#enddef

def sOrdr(itemId, quantity):
    prodJson = json.loads(requests.get(LIST_API.format(itemId)).content)
    prodWait = prodJson['sells'][0]['unit_price']
    prodGain = prodWait * quantity

    return { 'totalPrice': prodGain * 0.85 , 'unitPrice': prodWait }
#enddef

def sInst(itemId, quantity):
    prodJson = json.loads(requests.get(LIST_API.format(itemId)).content)
    prodInst = prodJson['buys']
    prodGain = 0
    prodRemd = quantity

    for i in range(len(prodInst)):
        currentEntry = prodInst[i]
        ## Successfully finish selling.
        if currentEntry['quantity'] >= prodRemd:
            prodGain += prodRemd * currentEntry['unit_price']
            prodRemd  = 0
            break
        ## Insufficient offers, extrapolated result.
        elif i == len(prodInst):
            prodGain += prodRemd * currentEntry['unit_price']
            prodRemd  = 0
            break
        ## Main loop.
        else:
            prodGain += currentEntry['quantity'] * currentEntry['unit_price']
            prodRemd -= currentEntry['quantity']
        #endelse
    #endfor

    return { 'totalPrice': prodGain * 0.85 , 'unitPrice': prodGain / quantity }
#enddef
