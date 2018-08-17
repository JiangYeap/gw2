from __future__ import division
from merchant import *
from item import *

import thread
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

class T6Graph:
    PROD_IDS = [
        [24295, 'Blood'],
        [24358, 'Bone'],
        [24351, 'Claw'],
        [24357, 'Fang'],
        [24289, 'Scale'],
        [24300, 'Totem'],
        [24283, 'Venom']
    ]
    MATS_IDS = [
        [24294, 'Vial of Potent Blood'],
        [24341, 'Large Bone'],
        [24350, 'Large Claw'],
        [24356, 'Large Fang'],
        [24288, 'Large Scale'],
        [24299, 'Intricate Totem'],
        [24282, 'Potent Venom'],
        [24277, 'Pile of Crystalline Dust']
    ]
    TYPES = 7
    N_BAR = 4
    WIDTH = 0.16
    TITLE = 'T6 Trophy Crafting Profit Per Stack\nDust B{}: {}'
    LABEL = 'Trophy Type [B{0} | S{0}]'
    LEGEND_LABELS = [
        'Buy Order; Sell Order',
        'Buy Instant; Sell Order',
        'Buy Order; Sell Instant',
        'Buy Instant; Sell Instant'
    ]
    COLOR_CATEGORY = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']

    def __init__(self, stacks=1, dustPrice=None):
        self.dustQuantity = 25 * stacks
        self.matsQuantity = 250 * stacks
        self.prodQuantity = 30 * stacks
        self.fixedDustPrice = dustPrice
        self.prodItems = [Item(self.PROD_IDS[i][0], self.PROD_IDS[i][1]) for i in range(self.TYPES)]
        self.matsItems = [Item(self.MATS_IDS[i][0], self.MATS_IDS[i][1]) for i in range(self.TYPES)]
        self.matsItems.append(Item(self.MATS_IDS[7][0], self.MATS_IDS[7][1]))
        self.merchant = Merchant()
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.priceType = 'O'
        self.updating = False
        self.selected = -1
        self.initGraph()
        self.updateGraph()
        plt.show()
    #enddef

    def initGraph(self):
        self.allBars = [self.ax.bar([j + i * self.WIDTH for j in range(self.TYPES)], [i] * self.TYPES, self.WIDTH, color=self.COLOR_CATEGORY[i], bottom=0) for i in range(self.N_BAR)]
        self.allBarlabels = [self.ax.text(i, i, '', ha='center', va='center') for i in range(self.TYPES)]
        self.fig.canvas.mpl_connect('motion_notify_event', self.onhover)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.ax.set_ylabel('Net Profit')
        self.ax.set_xticks([i + 1.5 * self.WIDTH for i in range(self.TYPES)])
        self.ax.legend([subBar[0] for subBar in self.allBars], self.LEGEND_LABELS, loc='best', fancybox=True, framealpha=0.5)
        self.ax.grid(True)
    #enddef

    def updateGraph(self):
        self.updating = True
        self.getItemPrices()
        for i in range(self.N_BAR):
            for j in range(self.TYPES):
                self.allBars[i].patches[j].set_height(self.netProfits[j][i])
            #endfor
        #endfor
        self.updateTickLabel('price')
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()
        self.updating = False
    #enddef

    def getItemPrices(self):
        prodPrices = [self.merchant.trade('s', self.prodItems[i], self.prodQuantity) for i in range(self.TYPES)]
        matsPrices = [self.merchant.trade('b', self.matsItems[i], self.matsQuantity) for i in range(self.TYPES)]
        if self.fixedDustPrice is not None:
            dustUnit = int(self.fixedDustPrice)
            assert dustUnit >= 0
            totlPrices = {'O': dustUnit * self.dustQuantity, 'I': dustUnit * self.dustQuantity}
            unitPrices = {'O': dustUnit, 'I': dustUnit}
            matsPrices.append({'totl': totlPrices, 'unit': unitPrices})
        else:
            matsPrices.append(self.merchant.trade('b', self.matsItems[7], self.dustQuantity))
        #endelse
        self.netProfits = [[
            prodPrices[i]['totl']['O'] - matsPrices[i]['totl']['O'] - matsPrices[7]['totl']['O'],
            prodPrices[i]['totl']['O'] - matsPrices[i]['totl']['I'] - matsPrices[7]['totl']['I'],
            prodPrices[i]['totl']['I'] - matsPrices[i]['totl']['O'] - matsPrices[7]['totl']['O'],
            prodPrices[i]['totl']['I'] - matsPrices[i]['totl']['I'] - matsPrices[7]['totl']['I']
        ] for i in range(self.TYPES)]
        self.prodUnitPrices = [prodPrices[i]['unit'] for i in range(self.TYPES)]
        self.matsUnitPrices = [matsPrices[i]['unit'] for i in range(8)]
    #enddef

    ## Handles mouse hover events.
    def onhover(self, event):
        if event.inaxes != self.ax and self.selected > -1:
            self.resetBarlabelAndFocus()
            self.selected = -1
            plt.draw()
            return
        #endif
        for i in range(self.N_BAR):
            subBar = self.allBars[i]
            for rect in subBar:
                contains, attrd = rect.contains(event)
                if contains:
                    self.updateBarlabel(subBar)
                    self.updateFocus(i)
                    self.selected = i
                    plt.draw()
                    return
                #endif
            #endfor
        #endfor
        self.resetBarlabelAndFocus()
        self.selected = -1
        plt.draw()
    #enddef

    ## Handles mouse click events.
    def onclick(self, event):
        if self.updating:
            return
        #endif
        if event.inaxes != self.ax:
            self.updatePriceType()
            return
        #endif
        self.updateTickLabel('load')
        plt.draw()
        thread.start_new_thread(self.updateGraph, ())
    #enddef

    ## Attach a text label above each bar displaying its height.
    def updateBarlabel(self, subBar):
        for i in range(self.TYPES):
            rect = subBar[i]
            barlabel = self.allBarlabels[i]
            rectWidth = rect.get_width()
            rectHeight = rect.get_height()
            barlabel.set_text(self.merchant.currencyConv(rectHeight))
            barlabel.set_position((rect.get_x() + rectWidth /  2, rectHeight + np.sign(rectHeight) * 300))
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
    def resetBarlabelAndFocus(self):
        for barlabel in self.allBarlabels:
            barlabel.set_text('')
        #endfor
        for i in range(self.N_BAR):
            subBar = self.allBars[i]
            for rect in subBar:
                rect.set_facecolor(self.COLOR_CATEGORY[i])
            #endfor
        #endfor
    #enddef

    def updatePriceType(self):
        if self.updating:
            return
        #endif
        if self.priceType == 'O':
            self.priceType = 'I'
        else:
            self.priceType = 'O'
        #endelse
        self.updateTickLabel('price')
        plt.draw()
    #enddef

    def updateTickLabel(self, type):
        if type == 'load':
            titleFormat = 'Loading...'
            tickFormats = ['Loading...'] * 7
        elif type == 'price':
            titleFormat = self.matsUnitPrices[7][self.priceType]
            tickFormats = [
                '{} | {}'.format(self.matsUnitPrices[i][self.priceType], self.prodUnitPrices[i][self.priceType])
            for i in range(self.TYPES)]
        #endelif
        tickLabels = ['{}\n{}'.format(self.prodItems[i]['name'], tickFormats[i]) for i in range(self.TYPES)]
        self.ax.set_title(self.TITLE.format(self.priceType, titleFormat))
        self.ax.set_xlabel(self.LABEL.format(self.priceType), labelpad=10)
        self.ax.set_xticklabels(tickLabels, ha='center')
    #enddef
#endclass

T6Graph()
