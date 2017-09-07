
PROMOTION_MAPPING = {'Private':'Corporal', 'Corporal':'Sergeant', 'Sergeant':'Warrant-Officer', 
                     'Warrant-Officer':'Lieutenant', 'Lieutenant':'Captain', 'Captain':'Major', 
                     'Major':'Colonel', 'Colonel':'General'}

MAX_LEVEL = 5


def promotion(string, mapping, loop):
    '''
    Find mapping recursively until the max loop
    '''
    loop -= 1 
    if loop < 0:
        return string

    word_list = []
    for word in string.split():
        if word in mapping:
            word_list.append(promotion(mapping[word], mapping, loop))
        else:
            word_list.append(word)
    return ' '.join(word_list)



if __name__ == '__main__':

    string = 'Private Captain Sergeant'

    res = promotion(string, PROMOTION_MAPPING, MAX_LEVEL)

    print(res)

