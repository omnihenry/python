#!/usr/bin/python
# title           :text_expansion.py
# description     :This script demonstrates (through 2 examples) the use of 
#                  a recursive function that expands a given text (to a max
#                  level) based on the pre-defined mapping 
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :python text_expansion.py
# notes           :
# python_version  : > 3
#==============================================================================

def expand_text(string, mapping, loop):
    '''
    Find mapping recursively until the max loop
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



if __name__ == '__main__':

    MAX_LEVEL = 2       # maximum levels of mapping to search

    # Example 1
    ABBR_MAPPING = {'aa':'ana', 'ana':'of each', 'agit.':'agita', 'agita':'agitate', 'agitate':'stir or shake', 
                    'b.d.':'bis indies', 'bis':'twice', 'EOD':'every other day',  'indies':'daily', 
                    'pc':'after meals', 'tab':'tabella', 'tabella':'tablet'}

    initial_string = '2 tab b.d. pc'
    res = expand_text(initial_string, ABBR_MAPPING, MAX_LEVEL)

    # Example 2
    '''    
    PROMOTION_MAPPING = {'Private':'Corporal', 'Corporal':'Sergeant', 'Sergeant':'Warrant-Officer', 
                         'Warrant-Officer':'Lieutenant', 'Lieutenant':'Captain', 'Captain':'Major', 
                         'Major':'Colonel', 'Colonel':'General'}

    initial_string = 'Private Captain Sergeant'
    res = expand_text(initial_string, PROMOTION_MAPPING, MAX_LEVEL)
    '''
    print(res)

