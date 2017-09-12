#!/usr/bin/python
# title           :text_expansion.py
# description     :This script contains the definition of a recursive function 
#                  that expands a given text (to a max level) based on the 
#                  pre-defined mapping.
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :to be imported
# notes           :
# python_version  : 2.7.10 and above
#==============================================================================

def expand_text(string, mapping, loop):
    '''
    Find mapping recursively until the max loop

    :param string: the text that contains space-separated words to expand
    :param mapping: the dictionary needed to find out mapping
    :param loop: the maximum rounds of looking up the dictionary
    :type string: str
    :type mapping: dict
    :type loop: int
    :returns: a string that contains the expanded text
    :rtype: str
    '''
    loop -= 1 
    if loop < 0:
        return string

    word_list = []          # used to save the result
    for word in string.split():
        if word in mapping:
            word_list.append(expand_text(mapping[word], mapping, loop))
        else:
            word_list.append(word)
    return ' '.join(word_list)


