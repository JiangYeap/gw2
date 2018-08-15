import numpy as np
import matplotlib.pyplot as plt
from calculations import *

N = 7
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

itemPrices      = np.empty([7, 4])
itemUnitPrices  = np.empty([7, 2])
itemTotalProfit = np.empty([7, 4])

for i in range(7):
    itemPrices[i] = [
        bOrdr(itemIds[i][0], matsQuantity),
        bInst(itemIds[i][0], matsQuantity),
        sOrdr(itemIds[i][1], prodQuantity),
        sInst(itemIds[i][1], prodQuantity)
    ]

    itemUnitPrices[i] = [
        itemPrices[i][0]['unitPrice'],
        itemPrices[i][2]['unitPrice']
    ]

    itemTotalProfit[i] = [
        itemPrices[i][2]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
        itemPrices[i][3]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
        itemPrices[i][2]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice'],
        itemPrices[i][3]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice']
    ]
#endfor

bloodProfit = itemTotalProfit[0]
boneProfit  = itemTotalProfit[1]
clawProfit  = itemTotalProfit[2]
fangProfit  = itemTotalProfit[3]
scaleProfit = itemTotalProfit[4]
totemProfit = itemTotalProfit[5]
venomProfit = itemTotalProfit[6]

print itemTotalProfit

# menMeans = (150, 160, 146, 172, 155)
#
# fig, ax = plt.subplots()
#
# ind = np.arange(N)    # the x locations for the groups
# width = 0.35         # the width of the bars
# p1 = ax.bar(ind, menMeans, width, color='r', bottom=0, yerr=menStd)
#
#
# womenMeans = (145, 149, 172, 165, 200)
# womenStd = (30, 25, 20, 31, 22)
# p2 = ax.bar(ind + width, womenMeans, width,
#             color='y', bottom=0, yerr=womenStd)
#
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
#
# ax.legend((p1[0], p2[0]), ('Men', 'Women'))
# ax.autoscale_view()
#
# plt.show()
