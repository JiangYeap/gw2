#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from trend_observer import TrendObserver
from merchant import Merchant
from item import Item

import thread
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

class T6Graph:
    N_TYPE = 7
    N_CLS = 4
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
        self._blm.init_trend_observers()
        self._price_type = 'O'
        self._updating = False
        self._init_graph()
        self._update_graph()
        plt.show()

    def _init_graph(self):
        self._all_bars = []
        for i in range(self.N_CLS):
            bar_cls_pos = [j + i * self.WIDTH for j in range(self.N_TYPE)]
            bar_cls = self._ax.bar(bar_cls_pos, [i] * self.N_TYPE, self.WIDTH,
                                   color=self.COLOR_CATEGORY[i], bottom=0)
            self._all_bars.append(bar_cls)
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
        self._blm.compute_all_trends()
        for i in range(self.N_CLS):
            for j in range(self.N_TYPE):
                rect = self._all_bars[i].patches[j]
                rect.set_height(self._blm.get_net_profit()[j][i])
            #endfor
        self._ax.relim()
        self._ax.autoscale_view()
        self._show_unit_price_labels()
        plt.draw()
        self._updating = False

    def _onhover(self, event):
        hovered = False
        for i in range(self.N_CLS):
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

    def _annotate_bars(self, index):
        bar_cls = self._all_bars[index]
        for i in range(self.N_TYPE):
            rect = bar_cls[i]
            rect_annot = self._bar_annots[i]
            rect_width = rect.get_width()
            rect_height = rect.get_height()
            x_pos = rect.get_x() + rect_width /  2
            y_pos = rect_height + np.sign(rect_height) * 300
            rect_annot.set_text(self._blm.currency_conv(rect_height))
            rect_annot.set_position((x_pos, y_pos))
        #endfor

    def _highlight_bars(self, index):
        for i in range(self.N_CLS):
            bar_cls = self._all_bars[i]
            if index != i:
                for rect in bar_cls:
                    rect.set_facecolor(self.COLOR_CATEGORY[i] + self.ALPHA)
                #endfor
            elif index == i:
                for rect in bar_cls:
                    rect.set_facecolor(self.COLOR_CATEGORY[i])
                #endfor
            #endelif
        #endfor

    def _hide_bar_focus(self):
        for bar_lbl in self._bar_annots:
            bar_lbl.set_text('')
        for i in range(self.N_CLS):
            bar_cls = self._all_bars[i]
            for rect in bar_cls:
                rect.set_facecolor(self.COLOR_CATEGORY[i])
            #endfor
        #endfor

    def _onclick(self, event):
        if not self._updating:
            if event.inaxes != self._ax:
                self._toggle_price_type()
            else:
                self._show_loading_labels()
                plt.draw()
                thread.start_new_thread(self._update_graph, ())
            #endelse
        #endif

    def _toggle_price_type(self):
        if not self._updating:
            self._price_type = 'I' if self._price_type == 'O' else 'O'
            self._show_unit_price_labels()
            plt.draw()
        #endif

    def _show_loading_labels(self):
        prod_names = [item['name'] for item in self._blm.get_prod_items()]
        tick_labels = [self.T_LABEL.format(prod_names[i], self.LOAD)
                       for i in range(self.N_TYPE)]
        self._ax.set_title(self.TITLE.format(self._price_type, self.LOAD))
        self._ax.set_xlabel(self.X_LABEL.format(self._price_type), labelpad=10)
        self._ax.set_xticklabels(tick_labels, ha='center')

    def _show_unit_price_labels(self):
        self._update_unit_trends_labels()
        self._ax.set_title(self.TITLE.format(self._price_type, self._dust_lbl))
        self._ax.set_xlabel(self.X_LABEL.format(self._price_type), labelpad=10)
        self._ax.set_xticklabels(self._tick_lbls, ha='center')

    def _update_unit_trends_labels(self):
        dust_up = self._blm.get_dust_unit_price()[self._price_type]
        dust_trd = self._blm.get_dust_trend()
        dust_ut = dust_trd[self._price_type] if dust_trd else None
        self._dust_lbl = str(dust_up) + self._format_trend(dust_ut)
        self._tick_lbls = []
        for i in range(self.N_TYPE):
            mats_up = self._blm.get_mats_unit_prices()[i][self._price_type]
            prod_up = self._blm.get_prod_unit_prices()[i][self._price_type]
            mats_trd = self._blm.get_mats_trends()[i]
            prod_trd = self._blm.get_prod_trends()[i]
            mats_ut = mats_trd[self._price_type] if mats_trd else None
            prod_ut = prod_trd[self._price_type] if prod_trd else None
            mats_lbl = str(mats_up) + self._format_trend(mats_ut)
            prod_lbl = str(prod_up) + self._format_trend(prod_ut)
            prod_name = self._blm.get_prod_items()[i]['name']
            mats_prod = '{} | {}'.format(mats_lbl, prod_lbl)
            self._tick_lbls.append(self.T_LABEL.format(prod_name, mats_prod))
        #endfor

    def _format_trend(self, trend):
        try:
            abs = np.abs(trend)
            rounded = round(abs, 1)
            if abs < 0.1:
                trend_str = r' $_{{\bf{{\textasciitilde}}}}$'
            elif trend < 0:
                trend_str = r' $_{{\bf{{- {}\%}}}}$'.format(rounded)
            else:
                trend_str = r' $_{{\bf{{+ {}\%}}}}$'.format(rounded)
            #endelse
        except TypeError:
            trend_str = ''
        return trend_str
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
        self._mats_items = [Item(self.MATS_ID[i]) for i in range(self.N_TYPE)]
        self._prod_items = [Item(self.PROD_ID[i]) for i in range(self.N_TYPE)]

    def update_prices(self):
        if self._fixed_dust_price is None:
            dp = self.trade('B', self._dust_item, self._dust_qty)
        else:
            fdp = self._fixed_dust_price
            dp = self.fixed_trade('B', self._dust_item, self._dust_qty, fdp)
        self._net_profit = np.empty((7, 4))
        self._dust_unit_price = dp['U']
        self._mats_unit_prices = []
        self._prod_unit_prices = []
        for i in range(self.N_TYPE):
            mp = self.trade('B', self._mats_items[i], self._mats_qty)
            pp = self.trade('S', self._prod_items[i], self._prod_qty)
            self._prod_unit_prices.append(pp['U'])
            self._mats_unit_prices.append(mp['U'])
            self._net_profit[i][0] = pp['T']['O'] - mp['T']['O'] - dp['T']['O']
            self._net_profit[i][1] = pp['T']['O'] - mp['T']['I'] - dp['T']['I']
            self._net_profit[i][2] = pp['T']['I'] - mp['T']['O'] - dp['T']['O']
            self._net_profit[i][3] = pp['T']['I'] - mp['T']['I'] - dp['T']['I']
        #endfor

    def get_dust_item(self):
        return self._dust_item

    def get_mats_items(self):
        return self._mats_items

    def get_prod_items(self):
        return self._prod_items

    def get_net_profit(self):
        return self._net_profit

    def get_dust_unit_price(self):
        return self._dust_unit_price

    def get_mats_unit_prices(self):
        return self._mats_unit_prices

    def get_prod_unit_prices(self):
        return self._prod_unit_prices

    def init_trend_observers(self):
        self._profit_tos = TrendObserver()
        self._dust_to = TrendObserver()
        self._mats_tos = [TrendObserver() for i in range(self.N_TYPE)]
        self._prod_tos = [TrendObserver() for i in range(self.N_TYPE)]

    def compute_all_trends(self):
        self._profit_tos.compute_trend(self._net_profit)
        self._dust_to.compute_trend(self._dust_unit_price)
        for i in range(self.N_TYPE):
            self._mats_tos[i].compute_trend(self._mats_unit_prices[i])
            self._prod_tos[i].compute_trend(self._prod_unit_prices[i])
        #endfor

    def get_profit_trend(self):
        return self._profit_tos.get_trend()

    def get_dust_trend(self):
        return self._dust_to.get_trend()

    def get_mats_trends(self):
        return [mto.get_trend() for mto in self._mats_tos]

    def get_prod_trends(self):
        return [pto.get_trend() for pto in self._prod_tos]
    #enddef

T6Graph()
