from __future__ import division
from merchant import *
from item import *

import thread
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

class T6Graph:
    N_TYPE = 7
    N_BAR = 4
    WIDTH = 0.16
    LOAD = 'Loading...'
    TITLE = 'T6 Trophy Crafting Profit Per Stack\nDust B{}: {}'
    X_LABEL = 'Trophy Type [B{0} | S{0}]'
    T_LABEL = '{}\n{}'
    LEGEND_LABELS = [
        'Buy Order; Sell Order',
        'Buy Instant; Sell Order',
        'Buy Order; Sell Instant',
        'Buy Instant; Sell Instant'
    ]
    COLOR_CATEGORY = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
    ALPHA = '94'

    def __init__(self, stacks=1, fixed_dust_price=None):
        self._fig, self._ax = plt.subplots(figsize=(14, 7))
        self._blm = T6BlackLionMerchant(stacks, fixed_dust_price)
        self._price_type = 'O'
        self._updating = False
        self._init_graph()
        self._update_graph()
        plt.show()

    def _init_graph(self):
        self._all_bars = []
        for i in range(self.N_BAR):
            sub_bars_pos = [j + i * self.WIDTH for j in range(self.N_TYPE)]
            sub_bars = self._ax.bar(sub_bars_pos, [i] * self.N_TYPE, self.WIDTH,
                                    color=self.COLOR_CATEGORY[i], bottom=0)
            self._all_bars.append(sub_bars)
        self._bar_annots = [self._ax.text(i, i, '', ha='center', va='center')
                            for i in range(self.N_TYPE)]
        self._ax.set_title(self.TITLE)
        self._ax.set_ylabel('Net Profit')
        self._ax.set_xlabel('Trophy Type')
        self._ax.set_xticks([i + 1.5 * self.WIDTH for i in range(self.N_TYPE)])
        self._ax.legend(self.LEGEND_LABELS, loc='best', framealpha=0.5)
        self._fig.canvas.mpl_connect('motion_notify_event', self._onhover)
        self._fig.canvas.mpl_connect('button_press_event', self._onclick)
        self._ax.grid(True)

    def _update_graph(self):
        self._updating = True
        self._blm.update_prices()
        for i in range(self.N_BAR):
            for j in range(self.N_TYPE):
                rect = self._all_bars[i].patches[j]
                rect.set_height(self._blm.get_net_profit()[j][i])
            #endfor
        self._ax.relim()
        self._ax.autoscale_view()
        self._show_unit_price_labels()
        plt.draw()
        self._updating = False

    def _show_loading_labels(self):
        prod_names = [item['name'] for item in self._blm.get_prod_item()]
        tick_labels = [self.T_LABEL.format(prod_names[i], self.LOAD)
                       for i in range(self.N_TYPE)]
        self._ax.set_title(self.TITLE.format(self._price_type, self.LOAD))
        self._ax.set_xlabel(self.X_LABEL.format(self._price_type), labelpad=10)
        self._ax.set_xticklabels(tick_labels, ha='center')

    def _show_unit_price_labels(self):
        dust_up = self._blm.get_dust_unit_price()[self._price_type]
        mats_ups = [item_up[self._price_type]
                    for item_up in self._blm.get_mats_unit_price()]
        prod_ups = [item_up[self._price_type]
                    for item_up in self._blm.get_prod_unit_price()]
        prod_names = [item['name'] for item in self._blm.get_prod_item()]
        tick_labels = []
        for i in range(self.N_TYPE):
            mats_prod = '{} | {}'.format(mats_ups[i], prod_ups[i])
            tick_labels.append(self.T_LABEL.format(prod_names[i], mats_prod))
        self._ax.set_title(self.TITLE.format(self._price_type, dust_up))
        self._ax.set_xlabel(self.X_LABEL.format(self._price_type), labelpad=10)
        self._ax.set_xticklabels(tick_labels, ha='center')

    def _onhover(self, event):
        hovered = False
        for i in range(self.N_BAR):
            for rect in self._all_bars[i]:
                contains, attrd = rect.contains(event)
                if contains:
                    hovered = True
                    self._annotate_bars(i)
                    self._highlight_bars(i)
                #endif
            #endfor
        if not hovered:
            self._hide_bar_focus()
        plt.draw()

    def _onclick(self, event):
        if self._updating:
            return None
        if event.inaxes != self._ax:
            self._change_price_type()
            return None
        self._show_loading_labels()
        plt.draw()
        thread.start_new_thread(self._update_graph, ())

    def _annotate_bars(self, index):
        sub_bars = self._all_bars[index]
        for i in range(self.N_TYPE):
            rect = sub_bars[i]
            rect_annot = self._bar_annots[i]
            rect_width = rect.get_width()
            rect_height = rect.get_height()
            x_pos = rect.get_x() + rect_width /  2
            y_pos = rect_height + np.sign(rect_height) * 300
            rect_annot.set_text(self._blm.currency_conv(rect_height))
            rect_annot.set_position((x_pos, y_pos))
        #endfor

    def _highlight_bars(self, index):
        for i in range(self.N_BAR):
            sub_bars = self._all_bars[i]
            if index != i:
                for rect in sub_bars:
                    rect.set_facecolor(self.COLOR_CATEGORY[i] + self.ALPHA)
                #endfor
            elif index == i:
                for rect in sub_bars:
                    rect.set_facecolor(self.COLOR_CATEGORY[i])
                #endfor
            #endelif
        #endfor

    def _hide_bar_focus(self):
        for bar_label in self._bar_annots:
            bar_label.set_text('')
        for i in range(self.N_BAR):
            sub_bars = self._all_bars[i]
            for rect in sub_bars:
                rect.set_facecolor(self.COLOR_CATEGORY[i])
            #endfor
        #endfor

    def _change_price_type(self):
        if self._updating:
            return None
        self._price_type = 'I' if self._price_type == 'O' else 'O'
        self._show_unit_price_labels()
        plt.draw()
    #enddef


class T6BlackLionMerchant(Merchant):
    N_TYPE = 7
    DUST_ID = [24277, 'Pile of Crystalline Dust']
    MATS_ID = [
        [24294, 'Vial of Potent Blood'],
        [24341, 'Large Bone'],
        [24350, 'Large Claw'],
        [24356, 'Large Fang'],
        [24288, 'Large Scale'],
        [24299, 'Intricate Totem'],
        [24282, 'Potent Venom']
    ]
    PROD_ID = [
        [24295, 'Blood'],
        [24358, 'Bone'],
        [24351, 'Claw'],
        [24357, 'Fang'],
        [24289, 'Scale'],
        [24300, 'Totem'],
        [24283, 'Venom']
    ]

    def __init__(self, stacks, fixed_dust_price=None):
        self._dust_qty = 25 * stacks
        self._mats_qty = 250 * stacks
        self._prod_qty = 30 * stacks
        self._fixed_dust_price = fixed_dust_price
        self._dust_item = Item(self.DUST_ID)
        self._mats_item = [Item(self.MATS_ID[i]) for i in range(self.N_TYPE)]
        self._prod_item = [Item(self.PROD_ID[i]) for i in range(self.N_TYPE)]

    def update_prices(self):
        if self._fixed_dust_price is None:
            dp = self.trade('B', self._dust_item, self._dust_qty)
        else:
            fdp = int(self._fixed_dust_price)
            assert fdp >= 0
            tp = {'O': fdp * self._dust_qty, 'I': fdp * self._dust_qty}
            up = {'O': fdp, 'I': fdp}
            dp = {'T': tp, 'U': up}
        self._net_profit = []
        self._dust_unit_price = dp['U']
        self._mats_unit_price = []
        self._prod_unit_price = []
        for i in range(self.N_TYPE):
            mp = self.trade('B', self._mats_item[i], self._mats_qty)
            pp = self.trade('S', self._prod_item[i], self._prod_qty)
            self._net_profit.append([
                pp['T']['O'] - mp['T']['O'] - dp['T']['O'],
                pp['T']['O'] - mp['T']['I'] - dp['T']['I'],
                pp['T']['I'] - mp['T']['O'] - dp['T']['O'],
                pp['T']['I'] - mp['T']['I'] - dp['T']['I']
            ])
            self._prod_unit_price.append(pp['U'])
            self._mats_unit_price.append(mp['U'])
        #endfor

    def get_dust_item(self):
        return self._dust_item

    def get_mats_item(self):
        return self._mats_item

    def get_prod_item(self):
        return self._prod_item

    def get_net_profit(self):
        return self._net_profit

    def get_dust_unit_price(self):
        return self._dust_unit_price

    def get_mats_unit_price(self):
        return self._mats_unit_price

    def get_prod_unit_price(self):
        return self._prod_unit_price
    #enddef


T6Graph()
