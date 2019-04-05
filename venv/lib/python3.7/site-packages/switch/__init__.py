# -*- coding: utf-8 -*-

from __future__ import with_statement

__version__ = '1.1.0'
__all__ = ['CSwitch', 'Switch']

import re


class Switch(object):
    """
    Switch, simple implementation of switch statement for Python, eg:

    >>> def test_switch(val):
    ...   ret = []
    ...   with Switch(val) as case:
    ...     if case(1, fall_through=True):
    ...       ret.append(1)
    ...     if case.match('2|two', '7|seven'):
    ...       ret.append('2 or two or 7 or seven')
    ...     if case.call(lambda v: 2 < v < 4):
    ...       ret.append(3)
    ...     if case.call(lambda v: 3 < v < 5, fall_through=True):
    ...       ret.append(4)
    ...     if case(5, 10):
    ...       ret.append('5 or 10')
    ...     if case.default:
    ...       ret.append(6)
    ...   return ret
    ...
    >>> test_switch(1)
    [1, '2 or two or 7 or seven']

    >>> test_switch(2)
    ['2 or two or 7 or seven']

    >>> test_switch(3)
    [3]

    >>> test_switch(4)
    [4, '5 or 10']

    >>> test_switch(5)
    ['5 or 10']

    >>> test_switch('seven')
    ['2 or two or 7 or seven']

    >>> test_switch(10)
    ['5 or 10']

    >>> test_switch(8)
    [6]


    >>> def test_switch_default_fall_through(val):
    ...   ret = []
    ...   with Switch(val, fall_through=True) as case:
    ...     if case(1):
    ...       ret.append(1)
    ...     if case(2):
    ...       ret.append(2)
    ...     if case.call(lambda v: 2 < v < 4):
    ...       ret.append(3)
    ...     if case.call(lambda v: 3 < v < 5, fall_through=False):
    ...       ret.append(4)
    ...     if case(5):
    ...       ret.append(5)
    ...     if case.default:
    ...       ret.append(6)
    ...   return ret
    ...
    >>> test_switch_default_fall_through(1)
    [1, 2, 3, 4]

    >>> test_switch_default_fall_through(2)
    [2, 3, 4]

    >>> test_switch_default_fall_through(3)
    [3, 4]

    >>> test_switch_default_fall_through(4)
    [4]

    >>> test_switch_default_fall_through(5)
    [5]

    >>> test_switch_default_fall_through(7)
    [6]
    """

    class StopExecution(Exception):
        pass

    def __init__(self, switch_value, fall_through=False):
        self._switch_value = switch_value
        self._default_fall_through = fall_through
        self._fall_through = False
        self._matched_case = False
        self._default_used = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is self.StopExecution

    def __call__(self, case_value, *case_values, **kwargs):
        return self.call(
            lambda switch_value: any(switch_value == v for v in (case_value, ) + case_values),
            **kwargs
        )

    def match(self, match_value, *match_values, **kwargs):
        def test(switch_value):
            # It is safe to call `re.compile()` on a compiled pattern:
            # a=re.compile('test'); assert a is re.compile(a)
            str_switch_value = str(switch_value)
            re_tests = (re.compile(v) for v in (match_value, ) + match_values)
            return any(regex.match(str_switch_value) for regex in re_tests)

        return self.call(test, **kwargs)

    def call(self, test, fall_through=None):
        if self._default_used:
            raise SyntaxError('Case after default is prohibited')

        self._check_finished()
        if self._fall_through or test(self._switch_value):
            self._matched_case = True
            self._fall_through = fall_through if fall_through is not None else self._default_fall_through
            return True

        return False

    @property
    def default(self):
        self._check_finished()
        self._default_used = True

        return not self._matched_case

    def _check_finished(self):
        if self._matched_case is True and self._fall_through is False:
            raise self.StopExecution


class CSwitch(Switch):
    """
    CSwitch is a shortcut to call Switch(test_value, fall_through=True)
    """
    def __init__(self, switch_value):
        super(CSwitch, self).__init__(switch_value, fall_through=True)
