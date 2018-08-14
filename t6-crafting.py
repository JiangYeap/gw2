from __future__ import division
import requests, cjson, sys

LIST_API = 'https://api.guildwars2.com/v2/commerce/listings/{}'

if __name__ == '__main__':
    print 'Enter number of stacks, defaults to 1 (250 base materials per stack).'

    try:
        stacks = float(raw_input())
    except ValueError:
        print 'Using 1 stack.'
        stacks = 1
    #endexcept

    if stacks <= 0:
        print 'Must be one or more stacks!'
        sys.exit()
    #endif

    print 'Enter prefixed dust price if applicable, ignore if none.'

    try:
        prefixDustPrice = int(raw_input())
    except ValueError:
        prefixDustPrice = -1
    #endexcept

    itemIds = [
        (24294, 24295, 'Blood'),
        (24341, 24358, 'Bone'),
        (24350, 24351, 'Claw'),
        (24356, 24357, 'Fang'),
        (24288, 24289, 'Scale'),
        (24299, 24300, 'Totem'),
        (24282, 24283, 'Venom')
    ]

    itemPrice = []

    if prefixDustPrice < 0:
        dustJson = cjson.decode(requests.get(LIST_API.format(24277)).content)
        dustWait = dustJson['buys'][0]
        dustInst = dustJson['sells']

        dustWaitPrice = stacks * 25 * dustWait['unit_price']
        dustInstPrice = 0

        print 'Using dust price from market.'
        print 'Dust Buy Order Price: {}'.format(dustWaitPrice / (stacks * 25))

        # Calculation for instant price.
        dustRemainder = stacks * 25
        for i in range(len(dustInst)):
            listEntry = dustInst[i]
            if listEntry['quantity'] >= dustRemainder:
                dustInstPrice += dustRemainder * listEntry['unit_price']
                dustRemainder  = 0
                break
            elif i == len(dustInst):
                print 'Insufficient Dust in market. Prices estimated using extrapolation.'
                dustInstPrice += dustRemainder * listEntry['unit_price']
                dustRemainder  = 0
                break
            else:
                dustInstPrice += listEntry['quantity'] * listEntry['unit_price']
                dustRemainder -= listEntry['quantity']
            #endelse
        #endfor
    #endif

    print '\nLoading materials information...'

    for mats, prod, name in itemIds:
        matsJson = cjson.decode(requests.get(LIST_API.format(mats)).content)
        matsWait = matsJson['buys'][0]
        matsInst = matsJson['sells']

        matsWaitPrice = stacks * 250 * matsWait['unit_price']
        matsInstPrice = 0

        # Calculation for instant price.
        matsRemainder = stacks * 250
        for i in range(len(matsInst)):
            listEntry = matsInst[i]
            if listEntry['quantity'] >= matsRemainder:
                matsInstPrice += matsRemainder * listEntry['unit_price']
                matsRemainder  = 0
                break
            elif i == len(matsInst):
                print 'Insufficient {} mats in market. Prices estimated using extrapolation.'.format(name)
                matsInstPrice += matsRemainder * listEntry['unit_price']
                matsRemainder  = 0
                break
            else:
                matsInstPrice += listEntry['quantity'] * listEntry['unit_price']
                matsRemainder -= listEntry['quantity']
            #endelse
        #endfor

        prodJson = cjson.decode(requests.get(LIST_API.format(prod)).content)
        prodWait = prodJson['sells'][0]
        prodInst = prodJson['buys']

        prodWaitPrice = stacks * 30 * prodWait['unit_price'] * 0.85
        prodInstPrice = 0

        # Calculation for instant price.
        prodRemainder = stacks * 30
        for i in range(len(prodInst)):
            listEntry = prodInst[i]
            if listEntry['quantity'] >= prodRemainder:
                prodInstPrice += prodRemainder * listEntry['unit_price']
                prodRemainder  = 0
                break
            elif i == len(prodInst):
                print 'Insufficient Big {} demand in market. Prices estimated using extrapolation.'.format(name)
                prodInstPrice += prodRemainder * listEntry['unit_price']
                prodRemainder  = 0
                break
            else:
                prodInstPrice += listEntry['quantity'] * listEntry['unit_price']
                prodRemainder -= listEntry['quantity']
            #endelse
        #endfor

        prodInstPrice *= 0.85

        itemPrice.append((matsWaitPrice, matsInstPrice, prodWaitPrice, prodInstPrice, name))
    #endfor

    # Patient buy and sell.
    print '\nBUY ORDER MATS; SELL ORDER PRODUCT.'

    for matsWaitPrice, _, prodWaitPrice, _, name in itemPrice:
        if prefixDustPrice >= 0:
            totalCost = matsWaitPrice + stacks * 25 * prefixDustPrice 
        else:
            totalCost = matsWaitPrice + dustWaitPrice
        #endelse

        print '{} ROI: {} - (Buy Order Price: {}, Sell Order Price: {})'.format(name, prodWaitPrice - totalCost, matsWaitPrice / (stacks * 250), prodWaitPrice / (stacks * 30 * 0.85))
    #endfor

    # Patient buy and instant sell.
    print '\nBUY ORDER MATS; INSTANT SELL PRODUCT.'

    for matsWaitPrice, _, _, prodInstPrice, name in itemPrice:
        if prefixDustPrice >= 0:
            totalCost = matsWaitPrice + stacks * 25 * prefixDustPrice 
        else:
            totalCost = matsWaitPrice + dustWaitPrice
        #endelse

        print '{} ROI: {} - (Buy Order Price: {}, Total Sales: {})'.format(name, prodInstPrice - totalCost, matsWaitPrice / (stacks * 250), prodInstPrice)
    #endfor

    # Instant buy and patient sell.
    print '\nINSTANT BUY MATS; SELL ORDER PRODUCT.'

    for _, matsInstPrice, prodWaitPrice, _, name in itemPrice:
        if prefixDustPrice >= 0:
            totalCost = matsInstPrice + stacks * 25 * prefixDustPrice 
        else:
            totalCost = matsInstPrice + dustInstPrice
        #endelse

        print '{} ROI: {} - (Total Costs: {}, Sell Order Price: {})'.format(name, prodWaitPrice - totalCost, totalCost, prodWaitPrice / (stacks * 30 * 0.85))
    #endfor

    # Instant buy and instant sell.
    print '\nINSTANT BUY MATS; INSTANT SELL PRODUCT.'

    for _, matsInstPrice, _, prodInstPrice, name in itemPrice:
        if prefixDustPrice >= 0:
            totalCost = matsInstPrice + stacks * 25 * prefixDustPrice 
        else:
            totalCost = matsInstPrice + dustInstPrice
        #endelse

        print '{} ROI: {} - (Total Costs: {}, Total Sales: {})'.format(name, prodInstPrice - totalCost, totalCost, prodInstPrice)
    #endfor
#endif
