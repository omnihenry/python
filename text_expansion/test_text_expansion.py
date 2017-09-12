#!/usr/bin/python
# title           :test_text_expansion.py
# description     :This is the unittest script for text_expansion
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :python test_text_expansion.py
# notes           :
# python_version  : 2.7.10 and above
#==============================================================================

import unittest
from text_expansion import *


class test_text_expansion(unittest.TestCase):

    def test_expand_text_case_1(self):
        string = '2 tab b.d. pc'
        self.assertEqual(expand_text(string, ABBR_MAPPING, 2), '2 tablet twice daily after meals')

    def test_expand_text_case_2(self):
        string = 'Private Sergeant Lieutenant'
        self.assertEqual(expand_text(string, PROMOTION_MAPPING, 5), 'Captain Colonel General')


if __name__ == '__main__':
    unittest.main()