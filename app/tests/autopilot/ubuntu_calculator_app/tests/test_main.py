# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

"""Calculator app autopilot tests."""

from autopilot.matchers import Eventually
from testtools.matchers import Equals

from ubuntu_calculator_app.tests import CalculatorAppTestCase


class MainTestCase(CalculatorAppTestCase):

    def setUp(self):
        super(MainTestCase, self).setUp()

    def test_temporarly_result(self):
        self.app.main_view.insert('2450.1*369+')

        self._assert_result_is(u'904086.9+')
        self.app.main_view.insert('3.1=')

        self._assert_result_is(u'904090')
        self._assert_history_contains(u'2450.1×369+3.1=9.0409e+5')

    def test_addding_operator_after_calculation(self):
        self.app.main_view.insert('8*8.1=')

        self._assert_result_is(u'64.8')
        self._assert_history_contains(u'8×8.1=64.8')

        self.app.main_view.insert('+5.2=')

        self._assert_result_is(u'70')
        self._assert_history_contains(u'64.8+5.2=70')

    def test_addding_number_after_calculation(self):
        self.app.main_view.insert('3*3.1=')

        self._assert_result_is(u'9.3')
        self._assert_history_contains(u'3×3.1=9.3')

        self.app.main_view.insert('8-7=')

        self._assert_result_is(u'1')
        self._assert_history_contains(u'8−7=1')

    def test_operation_after_clear(self):
        self.app.main_view.insert('8*8=')

        self._assert_result_is(u'64')
        self._assert_history_contains(u'8×8=64')

        self.app.main_view.clear()
        self._assert_result_is(u'')
        self.app.main_view.insert('9*9=')

        self._assert_result_is(u'81')
        self._assert_history_contains(u'9×9=81')

    def test_small_numbers(self):
        self.app.main_view.insert('0.000000001+1=')
        self._assert_result_is(u'1.000000001')
        self._assert_history_contains(u'0.000000001+1=1.000000001')

        self.app.main_view.clear()

        self.app.main_view.insert('0.000000001/10=')
        self._assert_result_is(u'1e−10')
        self._assert_history_contains(u'0.000000001÷10=1e-10')

    def test_operators_precedence(self):
        self.app.main_view.insert('2+2*2=')

        self._assert_result_is(u'6')
        self._assert_history_contains(u'2+2×2=6')

        self.app.main_view.clear()
        self.app.main_view.insert('2-2*2=')

        self._assert_result_is(u'−2')
        self._assert_history_contains(u'2−2×2=-2')

        self.app.main_view.clear()
        self.app.main_view.insert('5+6/2=')

        self._assert_result_is(u'8')
        self._assert_history_contains(u'5+6÷2=8')

    def test_divide_with_zero(self):
        self.app.main_view.insert('0/5=')

        self._assert_result_is(u'0')
        self._assert_history_contains(u'0÷5=0')

    def test_divide_by_zero(self):
        self.app.main_view.insert('5/0=')

        self._assert_result_is(u'\u221e')
        self._assert_history_contains(u'5÷0=Infinity')

    def test_divide_zero_by_zero(self):
        self.app.main_view.insert('0/0=')

        self._assert_result_is(u"NaN")
        self._assert_history_contains(u'0÷0=NaN')

    def _assert_result_is(self, value):
        self.assertThat(self.app.main_view.get_result,
                        Eventually(Equals(value)))

    def _assert_history_contains(self, value):
        self.assertTrue(self.app.main_view.get_history().contains(value))
