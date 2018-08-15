from __future__ import division
from calculations import *
from mpldatacursor import datacursor

import numpy as np
import matplotlib.pyplot as plt

stacks = 1

matsQuantity = 250 * stacks
dustQuantity = 25 * stacks
prodQuantity = 30 * stacks

dustPrice     = np.array([bOrdr(24277, dustQuantity), bInst(24277, dustQuantity)])
dustUnitPrice = dustPrice[0]['unitPrice']

itemIds = [
    [24294, 24295, 'Blood'],
    [24341, 24358, 'Bone'],
    [24350, 24351, 'Claw'],
    [24356, 24357, 'Fang'],
    [24288, 24289, 'Scale'],
    [24299, 24300, 'Totem'],
    [24282, 24283, 'Venom']
]

## Normal list used to store dicts.
itemPrices      = []
itemUnitPrices  = np.empty([7, 2])
itemTotalProfit = np.empty([7, 4])

for i in range(7):
    itemPrices.append([
        bOrdr(itemIds[i][0], matsQuantity),
        bInst(itemIds[i][0], matsQuantity),
        sOrdr(itemIds[i][1], prodQuantity),
        sInst(itemIds[i][1], prodQuantity)
    ])

    itemUnitPrices[i] = [
        itemPrices[i][0]['unitPrice'],
        itemPrices[i][2]['unitPrice']
    ]

    itemTotalProfit[i] = [
        itemPrices[i][2]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
        itemPrices[i][2]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice'],
        itemPrices[i][3]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
        itemPrices[i][3]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice']
    ]
#endfor

## Plotting.
N = 7

boso = itemTotalProfit[:, 0]
biso = itemTotalProfit[:, 1]
bosi = itemTotalProfit[:, 2]
bisi = itemTotalProfit[:, 3]

fig, ax = plt.subplots(figsize=(14, 7))

width = 0.12

ind = np.arange(N)
subBar1  = ax.bar(ind, boso, width, color='g', bottom=0)
subBar2  = ax.bar(ind + width, biso, width, color='b', bottom=0)
subBar3  = ax.bar(ind + 2 * width, bosi, width, color='y', bottom=0)
subBar4  = ax.bar(ind + 3 * width, bisi, width, color='r', bottom=0)

ax.set_title('T6 Trophy Crafting\nDust BO: {}\n'.format(dustUnitPrice))
ax.set_xlabel('Trophy Type [BO/SO]', labelpad=10)
ax.set_ylabel('Net Profit')

ax.set_xticks(ind + 2 * width)
ax.set_xticklabels([
    'Blood\n{}/{}'.format(itemUnitPrices[0, 0], itemUnitPrices[0, 1]),
    'Bone\n{}/{}'.format(itemUnitPrices[1, 0], itemUnitPrices[1, 1]),
    'Claw\n{}/{}'.format(itemUnitPrices[2, 0], itemUnitPrices[2, 1]),
    'Fang\n{}/{}'.format(itemUnitPrices[3, 0], itemUnitPrices[3, 1]),
    'Scale\n{}/{}'.format(itemUnitPrices[4, 0], itemUnitPrices[4, 1]),
    'Totem\n{}/{}'.format(itemUnitPrices[5, 0], itemUnitPrices[5, 1]),
    'Venom\n{}/{}'.format(itemUnitPrices[6, 0], itemUnitPrices[6, 1])
], ha='center')
ax.legend((
    subBar1[0], subBar2[0], subBar3[0], subBar4[0]),
    ('Buy Order; Sell Order', 'Buy Instant; Sell Order', 'Buy Order; Sell Instant', 'Buy Instant; Sell Instant'
))

ax.grid(True)
ax.autoscale_view()

print itemTotalProfit

## Attach a text label above each bar displaying its height.
def updateLabel(rects):
    for rect in rects:
        rectWidth  = rect.get_width()
        rectHeight = rect.get_height()
        txt = ax.text(rect.get_x() + rectWidth / 2, rectHeight + np.sign(rectHeight) * 600, int(rectHeight), ha='center', va='center')
    #endfor
#enddef

def onclick(event):
    if event.inaxes != ax and txt.get_text():
        txt.set_text('')
        plt.draw()
    #endif

    contained = -1
    for i in range(9):
        rect = b[i]
        contains, attrd = rect.contains(event)

        if contains and contained != i:
            autolabel(rect)
            contained = i
        #endif
    #endfor
    if contained == -1:
        txt.set_text('')
        plt.draw()
#enddef

def hover(event):
    # vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = subBar1.contains(event)
        if cont:
            if not txt: autolabel(subBar1)
            # annot.set_visible(True)
            # fig.canvas.draw_idle()
        else:
            if txt: txt.remove()
            #endif
        #endelse
    #endelse
#enddef

# fig.canvas.mpl_connect('motion_notify_event', hover)

plt.show()
