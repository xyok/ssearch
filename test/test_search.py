#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 2018/11/23

import unittest
from unittest.mock import patch

from ssearch.ssearch import search


class SearchTest(unittest.TestCase):

    def test_search(self):
        with patch('builtins.print') as mocked_print:
            search('notorio')
            mocked_print.assert_any_call('      text : notorio')


if __name__ == '__main__':
    unittest.main()
