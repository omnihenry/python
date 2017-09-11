#!/usr/bin/python
# title           :text_expansion.py
# description     :This script contains the definition of a recursive function 
#                  that expands a given text (to a max level) based on the 
#                  pre-defined mapping. Two test cases are also provided.
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :to be imported, the testing dictionaries are to be 
#                  substituted for real data
# notes           :
# python_version  : > 3
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


######################################################
#                                                    #  
# The following dictionaries are for testing purpose #
#                                                    #
######################################################

# Case 1
ABBR_MAPPING = {'aa':'ana', 'ana':'of each', 'agit.':'agita', 'agita':'agitate', 'agitate':'stir or shake', 
                'b.d.':'bis indies', 'bis':'twice', 'EOD':'every other day',  'indies':'daily', 
                'pc':'after meals', 'tab':'tabella', 'tabella':'tablet'}

# Case 2
PROMOTION_MAPPING = {'Private':'Corporal', 'Corporal':'Sergeant', 'Sergeant':'Warrant-Officer', 
                     'Warrant-Officer':'Lieutenant', 'Lieutenant':'Captain', 'Captain':'Major', 
                     'Major':'Colonel', 'Colonel':'General'}


