from __future__ import division
from calculations import *

import string
import matplotlib.pyplot as plt
import numpy as np

itemTotalProfit = np.array([
    [14185.5, 10388., 11023.5, 7226.5],
    [10682., 7832., 8904.65, 6054.65],
    [6097.5, 2747.5, 4261.5, 911.5],
    [8596.5, 5746.5, 5630., 2780.],
    [10498.5,  5148.5, 9070.5, 3720.5],
    [11105.5, 5541.5, 8817.3, 3253.32],
    [1670.5, -1679.5, -1899.5, -5249.5]
])
stacks = 1

matsQuantity = 250 * stacks
dustQuantity = 25 * stacks
prodQuantity = 30 * stacks

## Plotting.
N = 7
colorCategory = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
width   = 0.16
indices = np.arange(N)
fig, ax = plt.subplots(figsize=(14, 7))

boso = itemTotalProfit[:, 0]
biso = itemTotalProfit[:, 1]
bosi = itemTotalProfit[:, 2]
bisi = itemTotalProfit[:, 3]

subBar1 = ax.bar(indices, boso, width, color=colorCategory[0], bottom=0)
subBar2 = ax.bar(indices + width, biso, width, color=colorCategory[1], bottom=0)
subBar3 = ax.bar(indices + 2 * width, bosi, width, color=colorCategory[2], bottom=0)
subBar4 = ax.bar(indices + 3 * width, bisi, width, color=colorCategory[3], bottom=0)
allBars = [subBar1, subBar2, subBar3, subBar4]

ax.set_title('T6 Trophy Crafting Profit Per Stack\nDust BO: {}')
ax.set_xticklabels([
    'Blood\n{} | {}',
    'Bone\n{} | {}',
    'Claw\n{} | {}',
    'Fang\n{} | {}',
    'Scale\n{} | {}',
    'Totem\n{} | {}',
    'Venom\n{} | {}'
], ha='center')

## Mouse event handling.
allLabels = [ax.text(i, i, '', ha='center', va='center') for i in range(7)]
selected  = -1

## Attach a text label above each bar displaying its height.
def updateLabel(subBar):
    for i in range(len(subBar)):
        rect  = subBar[i]
        label = allLabels[i]
        rectWidth  = rect.get_width()
        rectHeight = rect.get_height()
        label.set_text(currencyConv(rectHeight))
        label.set_position((rect.get_x() + rectWidth /  2, rectHeight + np.sign(rectHeight) * 300))
    #endfor
#enddef

## Highlights focued sub bars.
def updateFocus(allBars, focusIndex):
    for i in range(len(allBars)):
        subBar = allBars[i]
        if focusIndex != i:
            for rect in subBar:
                rect.set_facecolor(colorCategory[i] + '94')
            #endfor
        #endif
        elif focusIndex == i:
            for rect in subBar:
                rect.set_facecolor(colorCategory[i])
            #endfor
        #endelif
    #endfor
#enddef

## Remove labels and highlights.
def resetLabelAndFocus():
    for label in allLabels:
        label.set_text('')
    #endfor
    for i in range(len(allBars)):
        subBar = allBars[i]
        for rect in subBar:
            rect.set_facecolor(colorCategory[i])
        #endfor
    #endfor
#enddef

## Handles mouse hover events.
def onhover(event):
    global selected
    if event.inaxes != ax and selected > -1:
        resetLabelAndFocus()
        selected = -1
        fig.canvas.draw_idle()
        return
    #endif
    for i in range(len(allBars)):
        subBar = allBars[i]
        for rect in subBar:
            contains, attrd = rect.contains(event)
            if contains:
                updateLabel(subBar)
                updateFocus(allBars, i)
                selected = i
                fig.canvas.draw_idle()
                return
            #endif
        #endfor
    #endfor
    resetLabelAndFocus()
    selected = -1
    fig.canvas.draw_idle()
#enddef

## Handles click events.
def onclick(event):
    global selected
    if event.inaxes != ax and selected > -1:
        resetLabelAndFocus()
        selected = -1
        fig.canvas.draw_idle()
        return
    #endif
    for i in range(len(allBars)):
        subBar = allBars[i]
        for rect in subBar:
            contains, attrd = rect.contains(event)
            if contains and selected != i:
                updateLabel(subBar)
                updateFocus(allBars, i)
                selected = i
                fig.canvas.draw_idle()
                return
            #endif
        #endfor
    #endfor
#enddef

# fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('motion_notify_event', onhover)

ax.set_xlabel('Trophy Type [BO | SO]', labelpad=10)
ax.set_ylabel('Net Profit')
ax.set_xticks(indices + 2 * width)
ax.legend((
    subBar1[0], subBar2[0], subBar3[0], subBar4[0]),
    ('Buy Order; Sell Order', 'Buy Instant; Sell Order', 'Buy Order; Sell Instant', 'Buy Instant; Sell Instant'
))
ax.autoscale_view()
ax.grid(True)
plt.show()
