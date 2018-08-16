from __future__ import division
from calculations import *

import string
import matplotlib.pyplot as plt
import numpy as np

# fig, ax = plt.subplots()
# b = ax.bar(range(9), range(1, 10), align='center')
# labels = string.ascii_uppercase[:9]
# ax.set(xticks=range(9), xticklabels=labels, title='Hover over a bar')
#
# # By default, the "popup" annotation will appear at the mouse's position.
# # Instead, you might want it to appear centered at the top of the rectangle in
# # the bar plot. By changing the x and y values using the "props_override"
# # option, we can customize where the "popup" appears.
#
# txt = ax.text(0, 0, '', ha='center', va='center')
#
# def autolabel(rect):
#     rectWidth  = rect.get_width()
#     rectHeight = rect.get_height()
#     txt.set_position((rect.get_x() + rectWidth / 2, rectHeight + np.sign(rectHeight) * .25))
#     txt.set_text(int(rectHeight))
#     plt.draw()
# #enddef
#
# def on_press(event):
#     if event.inaxes != ax and txt:
#         print 'hi'
#         txt.set_text('')
#         plt.draw()
#     #endif
#
#     contained = -1
#     for i in range(9):
#         rect = b[i]
#         contains, attrd = rect.contains(event)
#
#         if contains and contained != i:
#             autolabel(rect)
#             contained = i
#         #endif
#     #endfor
#     if contained == -1:
#         txt.set_text('')
#         plt.draw()
# #enddef
#
# fig.canvas.mpl_connect('button_press_event', on_press)
#
# plt.show()

## Plotting.
N = 7
colorCategory = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']

itemTotalProfit = np.array([
    [14185.5, 10388., 11023.5, 7226.5],
    [10682., 7832., 8904.65, 6054.65],
    [6097.5, 2747.5, 4261.5, 911.5],
    [8596.5, 5746.5, 5630., 2780.],
    [10498.5,  5148.5, 9070.5, 3720.5],
    [11105.5, 5541.5, 8817.3, 3253.32],
    [1670.5, -1679.5, -1899.5, -5249.5]
])

boso = itemTotalProfit[:, 0]
biso = itemTotalProfit[:, 1]
bosi = itemTotalProfit[:, 2]
bisi = itemTotalProfit[:, 3]

fig, ax = plt.subplots(figsize=(14, 7))

width = 0.16

ind = np.arange(N)
subBar1 = ax.bar(ind, boso, width, color=colorCategory[0], bottom=0)
subBar2 = ax.bar(ind + width, biso, width, color=colorCategory[1], bottom=0)
subBar3 = ax.bar(ind + 2 * width, bosi, width, color=colorCategory[2], bottom=0)
subBar4 = ax.bar(ind + 3 * width, bisi, width, color=colorCategory[3], bottom=0)

ax.set_title('T6 Trophy Crafting')
ax.set_xlabel('Trophy Type [BO/SO]', labelpad=10)
ax.set_ylabel('Net Profit')

ax.set_xticks(ind + 2 * width)
ax.set_xticklabels([
    'Blood\n{}/{}',
    'Bone\n{}/{}',
    'Claw\n{}/{}',
    'Fang\n{}/{}',
    'Scale\n{}/{}',
    'Totem\n{}/{}',
    'Venom\n{}/{}'
], ha='center')
ax.legend((
    subBar1[0], subBar2[0], subBar3[0], subBar4[0]),
    ('Buy Order; Sell Order', 'Buy Instant; Sell Order', 'Buy Order; Sell Instant', 'Buy Instant; Sell Instant'
))

ax.grid(True)
ax.autoscale_view()

allBars   = [subBar1, subBar2, subBar3, subBar4]
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
        label.set_position((rect.get_x() + rectWidth / 2, rectHeight + np.sign(rectHeight) * 500))
    #endfor
#enddef

def updateFocus(allBars, focusIndex):
    for i in range(len(allBars)):
        subBar = allBars[i]
        if focusIndex != i:
            for rect in subBar:
                rect.set_facecolor(colorCategory[i] + '94')
            #endfor
        elif focusIndex == i:
            for rect in subBar:
                rect.set_facecolor(colorCategory[i])
            #endfor
        #endelif
    #endfor
#enddef

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

def onclick(event):
    global selected
    if event.inaxes != ax and selected > -1:
        resetLabelAndFocus()
        selected = -1
        plt.draw()
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
                plt.draw()
                return
            #endif
        #endfor
    #endfor
#enddef

def onhover(event):
    global selected

    if event.inaxes != ax and selected > -1:
        resetLabelAndFocus()
        selected = -1
        plt.draw()
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
                plt.draw()
                return
            #endif
        #endfor
    #endfor

    resetLabelAndFocus()
    selected = -1
    plt.draw()
#enddef

fig.canvas.mpl_connect('motion_notify_event', onhover)

plt.show()
