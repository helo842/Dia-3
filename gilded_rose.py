# -*- coding: utf-8 -*-

class GildedRose(object):

    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == self.SULFURAS:
                continue

            self._update_quality(item)
            self._decrease_sell_in(item)
            self._update_expired_item(item)

    def _update_quality(self, item):
        if item.name == self.AGED_BRIE:
            self._increase_quality(item)
            return

        if item.name == self.BACKSTAGE_PASS:
            self._increase_quality(item)
            if item.sell_in < 11:
                self._increase_quality(item)
            if item.sell_in < 6:
                self._increase_quality(item)
            return

        self._decrease_quality(item)

    def _decrease_sell_in(self, item):
        item.sell_in -= 1

    def _update_expired_item(self, item):
        if item.sell_in >= 0:
            return

        if item.name == self.AGED_BRIE:
            self._increase_quality(item)
        elif item.name == self.BACKSTAGE_PASS:
            item.quality = 0
        else:
            self._decrease_quality(item)

    def _increase_quality(self, item):
        if item.quality < 50:
            item.quality += 1

    def _decrease_quality(self, item):
        if item.quality > 0:
            item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)