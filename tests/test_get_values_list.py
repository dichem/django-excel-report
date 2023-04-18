from django.test import TestCase
from decimal import Decimal
import datetime

from django_excel_report.writer.accessors import get_values_list


class DefaultSettingsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        def not_iterable1(*args): return "s"
        def not_iterable2(*args): return 12
        def not_iterable3(*args): return Decimal("12.1")
        def not_iterable4(*args, d=datetime.datetime.now()): return d
        cls.not_iterable_funcs = [not_iterable1, not_iterable2, not_iterable3, not_iterable4]

    def test_not_iterable(self):
        for func in self.not_iterable_funcs:
            self.assertListEqual(
                get_values_list(func)(1, 1),
                [func().__str__()]
            )

    def test_iterable(self):
        def iterable1(*args): return [["2", Decimal("1.2")], 12, [], []]
        self.assertListEqual(
            get_values_list(iterable1)(1, 1),
            ["2", "1.2", "12"]
        )

        def iterable2(*args): return [["2", Decimal("1.2")], 12, [""], [""]]
        self.assertListEqual(
            get_values_list(iterable2)(1, 1),
            ["2", "1.2", "12", "", ""]
        )

        def iterable3(*args): return [[[[[[[]]]]]]]
        self.assertListEqual(
            get_values_list(iterable3)(1, 1),
            [""]
        )

        def iterable4(*args): return [None, [None, None]]
        self.assertListEqual(
            get_values_list(iterable4)(1, 1),
            [""]
        )
