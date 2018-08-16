from __future__ import division
from calculations import *

import thread
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
        plt.show()
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
        self.ax.set_xticks([x + 1.5 * self.WIDTH for x in self.INDEX])
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
        plt.draw()
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
            plt.draw()
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
                    plt.draw()
                    return
                #endif
            #endfor
        #endfor
        self.resetLabelAndFocus()
        self.selected = -1
        plt.draw()
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
        plt.draw()
        thread.start_new_thread(self.updateGraph, ())
    #enddef
#endclass

T6Graph()
