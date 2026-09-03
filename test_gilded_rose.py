# -*- coding: utf-8 -*-
import pytest

from gilded_rose import GildedRose, Item


def update(name, sell_in, quality, days=1):
    item = Item(name, sell_in, quality)
    shop = GildedRose([item])
    for _ in range(days):
        shop.update_quality()
    return item


class TestNormalItems:
    def test_quality_decreases_by_one_before_sell_date(self):
        item = update("Elixir of the Mongoose", sell_in=10, quality=20)
        assert item.sell_in == 9
        assert item.quality == 19

    def test_quality_decreases_twice_as_fast_after_sell_date(self):
        item = update("Elixir of the Mongoose", sell_in=0, quality=20)
        assert item.sell_in == -1
        assert item.quality == 18

    def test_quality_decreases_twice_as_fast_when_already_expired(self):
        item = update("+5 Dexterity Vest", sell_in=-1, quality=10)
        assert item.sell_in == -2
        assert item.quality == 8

    def test_quality_never_goes_negative(self):
        item = update("Elixir of the Mongoose", sell_in=5, quality=0)
        assert item.quality == 0

    def test_quality_never_goes_negative_when_expired(self):
        item = update("Elixir of the Mongoose", sell_in=0, quality=1)
        assert item.quality == 0

    def test_quality_never_goes_negative_from_zero_when_expired(self):
        item = update("Elixir of the Mongoose", sell_in=0, quality=0)
        assert item.quality == 0

    def test_sell_in_decreases_each_day(self):
        item = update("foo", sell_in=1, quality=5, days=3)
        assert item.sell_in == -2
        assert item.quality == 0


class TestAgedBrie:
    def test_quality_increases_by_one_before_sell_date(self):
        item = update(GildedRose.AGED_BRIE, sell_in=10, quality=20)
        assert item.sell_in == 9
        assert item.quality == 21

    def test_quality_increases_by_two_after_sell_date(self):
        item = update(GildedRose.AGED_BRIE, sell_in=0, quality=20)
        assert item.sell_in == -1
        assert item.quality == 22

    def test_quality_increases_by_two_when_already_expired(self):
        item = update(GildedRose.AGED_BRIE, sell_in=-5, quality=10)
        assert item.quality == 12

    def test_quality_never_exceeds_50_before_sell_date(self):
        item = update(GildedRose.AGED_BRIE, sell_in=5, quality=50)
        assert item.quality == 50

    def test_quality_never_exceeds_50_from_49_before_sell_date(self):
        item = update(GildedRose.AGED_BRIE, sell_in=5, quality=49)
        assert item.quality == 50

    def test_quality_never_exceeds_50_when_expired(self):
        item = update(GildedRose.AGED_BRIE, sell_in=0, quality=49)
        assert item.quality == 50

    def test_quality_never_exceeds_50_from_50_when_expired(self):
        item = update(GildedRose.AGED_BRIE, sell_in=0, quality=50)
        assert item.quality == 50


class TestSulfuras:
    def test_quality_and_sell_in_never_change(self):
        item = update(GildedRose.SULFURAS, sell_in=0, quality=80)
        assert item.sell_in == 0
        assert item.quality == 80

    def test_unchanged_when_sell_in_is_positive(self):
        item = update(GildedRose.SULFURAS, sell_in=10, quality=80)
        assert item.sell_in == 10
        assert item.quality == 80

    def test_unchanged_when_sell_in_is_negative(self):
        item = update(GildedRose.SULFURAS, sell_in=-1, quality=80)
        assert item.sell_in == -1
        assert item.quality == 80

    def test_unchanged_over_multiple_days(self):
        item = update(GildedRose.SULFURAS, sell_in=5, quality=80, days=10)
        assert item.sell_in == 5
        assert item.quality == 80


class TestBackstagePasses:
    def test_quality_increases_by_one_when_more_than_10_days(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=15, quality=20)
        assert item.sell_in == 14
        assert item.quality == 21

    def test_quality_increases_by_one_on_day_11(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=11, quality=20)
        assert item.sell_in == 10
        assert item.quality == 21

    def test_quality_increases_by_two_when_10_days_or_less(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=10, quality=20)
        assert item.sell_in == 9
        assert item.quality == 22

    def test_quality_increases_by_two_on_day_6(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=6, quality=20)
        assert item.sell_in == 5
        assert item.quality == 22

    def test_quality_increases_by_three_when_5_days_or_less(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=5, quality=20)
        assert item.sell_in == 4
        assert item.quality == 23

    def test_quality_increases_by_three_on_day_1(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=1, quality=20)
        assert item.sell_in == 0
        assert item.quality == 23

    def test_quality_drops_to_zero_after_concert(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=0, quality=20)
        assert item.sell_in == -1
        assert item.quality == 0

    def test_quality_stays_zero_after_concert(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=-1, quality=0)
        assert item.quality == 0

    def test_quality_never_exceeds_50_when_more_than_10_days(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=15, quality=50)
        assert item.quality == 50

    def test_quality_capped_at_50_when_increasing_by_two(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=10, quality=49)
        assert item.quality == 50

    def test_quality_capped_at_50_when_increasing_by_three(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=5, quality=48)
        assert item.quality == 50

    def test_quality_capped_at_50_from_49_when_increasing_by_three(self):
        item = update(GildedRose.BACKSTAGE_PASS, sell_in=5, quality=49)
        assert item.quality == 50


class TestMultipleItems:
    def test_updates_each_item_independently(self):
        items = [
            Item("Elixir of the Mongoose", 5, 10),
            Item(GildedRose.AGED_BRIE, 2, 0),
            Item(GildedRose.SULFURAS, 0, 80),
            Item(GildedRose.BACKSTAGE_PASS, 15, 20),
        ]
        GildedRose(items).update_quality()

        assert (items[0].sell_in, items[0].quality) == (4, 9)
        assert (items[1].sell_in, items[1].quality) == (1, 1)
        assert (items[2].sell_in, items[2].quality) == (0, 80)
        assert (items[3].sell_in, items[3].quality) == (14, 21)

    def test_empty_inventory_does_not_raise(self):
        GildedRose([]).update_quality()


class TestItemRepr:
    def test_repr_includes_name_sell_in_and_quality(self):
        item = Item("foo", 1, 2)
        assert repr(item) == "foo, 1, 2"


@pytest.mark.parametrize(
    "name,sell_in,quality,expected_sell_in,expected_quality",
    [
        ("foo", 10, 20, 9, 19),
        ("foo", 0, 20, -1, 18),
        ("foo", 0, 0, -1, 0),
        (GildedRose.AGED_BRIE, 2, 0, 1, 1),
        (GildedRose.AGED_BRIE, 0, 0, -1, 2),
        (GildedRose.AGED_BRIE, 2, 50, 1, 50),
        (GildedRose.SULFURAS, 0, 80, 0, 80),
        (GildedRose.BACKSTAGE_PASS, 20, 20, 19, 21),
        (GildedRose.BACKSTAGE_PASS, 10, 20, 9, 22),
        (GildedRose.BACKSTAGE_PASS, 5, 20, 4, 23),
        (GildedRose.BACKSTAGE_PASS, 0, 20, -1, 0),
    ],
)
def test_update_quality_table(name, sell_in, quality, expected_sell_in, expected_quality):
    item = update(name, sell_in, quality)
    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality
