from __future__ import division
from calculations import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

class T6Graph:
    ITEM_IDS = [
        [24294, 24295, 'Blood'],
        [24341, 24358, 'Bone'],
        [24350, 24351, 'Claw'],
        [24356, 24357, 'Fang'],
        [24288, 24289, 'Scale'],
        [24299, 24300, 'Totem'],
        [24282, 24283, 'Venom']
    ]
    COLOR_CATEGORY = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
    TYPES = 7
    N_BAR = 4
    INDEX = range(TYPES)
    WIDTH = 0.16
    TITLE = 'T6 Trophy Crafting Profit Per Stack\nDust BO: {}'
    LABEL = ''

    def __init__(self, stacks=1, dustPrice=None):
        self.stacks = stacks
        self.matsQuantity = 250 * stacks
        self.dustQuantity = 25 * stacks
        self.prodQuantity = 30 * stacks
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.selected = -1
        try:
            self.fixedDustPrice = int(dustPrice)
        except (TypeError, ValueError):
            self.fixedDustPrice = None
        #endexcept
        self.initGraph()
        self.updateGraph()
    #enddef

    def getItemPrices(self):
        self.itemPrices = []
        self.itemUnitPrices = []
        self.itemTotalProfit = []

        if self.fixedDustPrice:
            self.dustPrice     = [self.fixedDustPrice * self.dustQuantity] * 2
            self.dustUnitPrice = self.fixedDustPrice
        else:
            self.dustPrice     = [bOrdr(24277, self.dustQuantity), bInst(24277, self.dustQuantity)]
            self.dustUnitPrice = self.dustPrice[0]['unitPrice']
        #endelse
        for i in range(self.TYPES):
            self.itemPrices.append([
                bOrdr(self.ITEM_IDS[i][0], self.matsQuantity),
                bInst(self.ITEM_IDS[i][0], self.matsQuantity),
                sOrdr(self.ITEM_IDS[i][1], self.prodQuantity),
                sInst(self.ITEM_IDS[i][1], self.prodQuantity)
            ])
            self.itemUnitPrices.append([
                self.itemPrices[i][0]['unitPrice'],
                self.itemPrices[i][2]['unitPrice']
            ])
            self.itemTotalProfit.append([
                self.itemPrices[i][2]['totalPrice'] - self.itemPrices[i][0]['totalPrice'] - self.dustPrice[0]['totalPrice'],
                self.itemPrices[i][2]['totalPrice'] - self.itemPrices[i][1]['totalPrice'] - self.dustPrice[1]['totalPrice'],
                self.itemPrices[i][3]['totalPrice'] - self.itemPrices[i][0]['totalPrice'] - self.dustPrice[0]['totalPrice'],
                self.itemPrices[i][3]['totalPrice'] - self.itemPrices[i][1]['totalPrice'] - self.dustPrice[1]['totalPrice']
            ])
        #endfor
    #enddef

    def initGraph(self):
        self.allBars = [self.ax.bar([x + i * self.WIDTH for x in self.INDEX], [i] * self.TYPES, self.WIDTH, color=self.COLOR_CATEGORY[i], bottom=0) for i in range(self.N_BAR)]
        self.allLabels = [self.ax.text(i, i, '', ha='center', va='center') for i in range(self.TYPES)]

        self.fig.canvas.mpl_connect('motion_notify_event', self.onhover)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.ax.set_xlabel('Trophy Type [BO | SO]', labelpad=10)
        self.ax.set_ylabel('Net Profit')
        self.ax.set_xticks([x + 2 * self.WIDTH for x in self.INDEX])
        self.ax.legend(
            [subBar[0] for subBar in self.allBars],
            ['Buy Order; Sell Order', 'Buy Instant; Sell Order', 'Buy Order; Sell Instant', 'Buy Instant; Sell Instant'],
            loc='best',
            fancybox=True,
            framealpha=0.5
        )
        self.ax.grid(True)
    #enddef

    def updateGraph(self):
        self.getItemPrices()
        for i in range(self.N_BAR):
            for j in range(self.TYPES):
                self.allBars[i].patches[j].set_height(self.itemTotalProfit[j][i])
            #endfor
        #endfor
        self.ax.set_title(self.TITLE.format(self.dustUnitPrice))
        self.ax.set_xticklabels(
            ['{}\n{} | {}'.format(self.ITEM_IDS[i][2], self.itemUnitPrices[i][0], self.itemUnitPrices[i][1]) for i in range(self.TYPES)],
            ha='center'
        )
        self.ax.relim()
        self.ax.autoscale_view()
        plt.show()
    #enddef

    ## Attach a text label above each bar displaying its height.
    def updateLabel(self, subBar):
        for i in range(self.TYPES):
            rect  = subBar[i]
            label = self.allLabels[i]
            rectWidth  = rect.get_width()
            rectHeight = rect.get_height()
            label.set_text(currencyConv(rectHeight))
            label.set_position((rect.get_x() + rectWidth /  2, rectHeight + np.sign(rectHeight) * 300))
        #endfor
    #enddef

    ## Highlights focued sub bars.
    def updateFocus(self, focusIndex):
        for i in range(self.N_BAR):
            subBar = self.allBars[i]
            if focusIndex != i:
                for rect in subBar:
                    rect.set_facecolor(self.COLOR_CATEGORY[i] + '94')
                #endfor
            #endif
            elif focusIndex == i:
                for rect in subBar:
                    rect.set_facecolor(self.COLOR_CATEGORY[i])
                #endfor
            #endelif
        #endfor
    #enddef

    ## Remove labels and highlights.
    def resetLabelAndFocus(self):
        for label in self.allLabels:
            label.set_text('')
        #endfor
        for i in range(self.N_BAR):
            subBar = self.allBars[i]
            for rect in subBar:
                rect.set_facecolor(self.COLOR_CATEGORY[i])
            #endfor
        #endfor
    #enddef

    ## Handles mouse hover events.
    def onhover(self, event):
        if event.inaxes != self.ax and self.selected > -1:
            self.resetLabelAndFocus()
            self.selected = -1
            plt.show()
            return
        #endif
        for i in range(self.N_BAR):
            subBar = self.allBars[i]
            for rect in subBar:
                contains, attrd = rect.contains(event)
                if contains:
                    self.updateLabel(subBar)
                    self.updateFocus(i)
                    self.selected = i
                    plt.show()
                    return
                #endif
            #endfor
        #endfor
        self.resetLabelAndFocus()
        self.selected = -1
        plt.show()
    #enddef

    ## Handles mouse click events.
    def onclick(self, event):
        if event.inaxes != self.ax:
            return
        #endif
        self.ax.set_title(self.TITLE.format('Loading...'))
        self.ax.set_xticklabels(
            ['{}\n{}'.format(self.ITEM_IDS[i][2], 'Loading...') for i in range(self.TYPES)],
            ha='center'
        )
        plt.show()
        self.updateGraph()
    #enddef
#endclass

T6Graph()

# stacks = 1
#
# matsQuantity = 250 * stacks
# dustQuantity = 25 * stacks
# prodQuantity = 30 * stacks
#
# itemIds = [
#     [24294, 24295, 'Blood'],
#     [24341, 24358, 'Bone'],
#     [24350, 24351, 'Claw'],
#     [24356, 24357, 'Fang'],
#     [24288, 24289, 'Scale'],
#     [24299, 24300, 'Totem'],
#     [24282, 24283, 'Venom']
# ]
#
# ## Calculations of prices.
# dustPrice     = np.array([bOrdr(24277, dustQuantity), bInst(24277, dustQuantity)])
# dustUnitPrice = dustPrice[0]['unitPrice']
#
# itemPrices      = []
# itemUnitPrices  = np.empty([7, 2])
# itemTotalProfit = np.empty([7, 4])
#
# for i in range(7):
#     itemPrices.append([
#         bOrdr(itemIds[i][0], matsQuantity),
#         bInst(itemIds[i][0], matsQuantity),
#         sOrdr(itemIds[i][1], prodQuantity),
#         sInst(itemIds[i][1], prodQuantity)
#     ])
#
#     itemUnitPrices[i] = [
#         itemPrices[i][0]['unitPrice'],
#         itemPrices[i][2]['unitPrice']
#     ]
#
#     itemTotalProfit[i] = [
#         itemPrices[i][2]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
#         itemPrices[i][2]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice'],
#         itemPrices[i][3]['totalPrice'] - itemPrices[i][0]['totalPrice'] - dustPrice[0]['totalPrice'],
#         itemPrices[i][3]['totalPrice'] - itemPrices[i][1]['totalPrice'] - dustPrice[1]['totalPrice']
#     ]
# #endfor
#
# ## Plotting.
# N = 7
# colorCategory = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
# width   = 0.16
# indices = np.arange(N)
# fig, ax = plt.subplots(figsize=(14, 7))
#
# boso = itemTotalProfit[:, 0]
# biso = itemTotalProfit[:, 1]
# bosi = itemTotalProfit[:, 2]
# bisi = itemTotalProfit[:, 3]
#
# subBar1 = ax.bar(indices, boso, width, color=colorCategory[0], bottom=0)
# subBar2 = ax.bar(indices + width, biso, width, color=colorCategory[1], bottom=0)
# subBar3 = ax.bar(indices + 2 * width, bosi, width, color=colorCategory[2], bottom=0)
# subBar4 = ax.bar(indices + 3 * width, bisi, width, color=colorCategory[3], bottom=0)
# allBars = [subBar1, subBar2, subBar3, subBar4]
#
# ax.set_title('T6 Trophy Crafting Profit Per Stack\nDust BO: {}'.format(dustUnitPrice))
# ax.set_xticklabels([
#     'Blood\n{} | {}'.format(itemUnitPrices[0, 0], itemUnitPrices[0, 1]),
#     'Bone\n{} | {}'.format(itemUnitPrices[1, 0], itemUnitPrices[1, 1]),
#     'Claw\n{} | {}'.format(itemUnitPrices[2, 0], itemUnitPrices[2, 1]),
#     'Fang\n{} | {}'.format(itemUnitPrices[3, 0], itemUnitPrices[3, 1]),
#     'Scale\n{} | {}'.format(itemUnitPrices[4, 0], itemUnitPrices[4, 1]),
#     'Totem\n{} | {}'.format(itemUnitPrices[5, 0], itemUnitPrices[5, 1]),
#     'Venom\n{} | {}'.format(itemUnitPrices[6, 0], itemUnitPrices[6, 1])
# ], ha='center')
#
# ## Mouse event handling.
# allLabels = [ax.text(i, i, '', ha='center', va='center') for i in range(7)]
# selected  = -1
#
# ## Attach a text label above each bar displaying its height.
# def updateLabel(subBar):
#     for i in range(len(subBar)):
#         rect  = subBar[i]
#         label = allLabels[i]
#         rectWidth  = rect.get_width()
#         rectHeight = rect.get_height()
#         label.set_text(currencyConv(rectHeight))
#         label.set_position((rect.get_x() + rectWidth /  2, rectHeight + np.sign(rectHeight) * 300))
#     #endfor
# #enddef
#
# ## Highlights focued sub bars.
# def updateFocus(allBars, focusIndex):
#     for i in range(len(allBars)):
#         subBar = allBars[i]
#         if focusIndex != i:
#             for rect in subBar:
#                 rect.set_facecolor(colorCategory[i] + '94')
#             #endfor
#         #endif
#         elif focusIndex == i:
#             for rect in subBar:
#                 rect.set_facecolor(colorCategory[i])
#             #endfor
#         #endelif
#     #endfor
# #enddef
#
# ## Remove labels and highlights.
# def resetLabelAndFocus():
#     for label in allLabels:
#         label.set_text('')
#     #endfor
#     for i in range(len(allBars)):
#         subBar = allBars[i]
#         for rect in subBar:
#             rect.set_facecolor(colorCategory[i])
#         #endfor
#     #endfor
# #enddef
#
# ## Handles mouse hover events.
# def onhover(event):
#     global selected
#     if event.inaxes != ax and selected > -1:
#         resetLabelAndFocus()
#         selected = -1
#         plt.show()
#         return
#     #endif
#     for i in range(len(allBars)):
#         subBar = allBars[i]
#         for rect in subBar:
#             contains, attrd = rect.contains(event)
#             if contains:
#                 updateLabel(subBar)
#                 updateFocus(allBars, i)
#                 selected = i
#                 plt.show()
#                 return
#             #endif
#         #endfor
#     #endfor
#     resetLabelAndFocus()
#     selected = -1
#     plt.show()
# #enddef
#
# ## Handles click events.
# def onclick(event):
#     global selected
#     if event.inaxes != ax and selected > -1:
#         resetLabelAndFocus()
#         selected = -1
#         plt.show()
#         return
#     #endif
#     for i in range(len(allBars)):
#         subBar = allBars[i]
#         for rect in subBar:
#             contains, attrd = rect.contains(event)
#             if contains and selected != i:
#                 updateLabel(subBar)
#                 updateFocus(allBars, i)
#                 selected = i
#                 plt.show()
#                 return
#             #endif
#         #endfor
#     #endfor
# #enddef
#
# # fig.canvas.mpl_connect('button_press_event', onclick)
# fig.canvas.mpl_connect('motion_notify_event', onhover)
#
# ax.set_xlabel('Trophy Type [BO | SO]', labelpad=10)
# ax.set_ylabel('Net Profit')
# ax.set_xticks(indices + 2 * width)
# ax.legend((
#     subBar1[0], subBar2[0], subBar3[0], subBar4[0]),
#     ('Buy Order; Sell Order', 'Buy Instant; Sell Order', 'Buy Order; Sell Instant', 'Buy Instant; Sell Instant'
# ))
# ax.autoscale_view()
# ax.grid(True)
# plt.show()
