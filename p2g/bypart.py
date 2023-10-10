from .rules import low, mid, high, live, dead, low_single, low_pair, vowels_all
from .map_vectors import (CONSONANTS, 
                          CLUSTERS, 
                          VOWELS_SHORT, 
                          VOWELS_LONG, 
                          DIPTHONGS, 
                          CODAS)

def positionOnTable(ru, _consonant, _coda, _vowel, _level):
#     print(ru, _consonant, _coda, _vowel, _level,"@position") #position
    if _coda in live and _vowel in VOWELS_LONG:
        return f"{ru}-live-long-{_level}"
    
    if _coda in live and _vowel in VOWELS_SHORT:
        return f"{ru}-live-short-{_level}"
    
    if _coda in dead and _vowel in VOWELS_LONG:
        return f"{ru}-dead-long-{_level}"
    
    if _coda in dead and _vowel in VOWELS_SHORT:
        return f"{ru}-dead-short-{_level}"
    
    if _coda == 'z' or _coda=='':
        if _vowel in VOWELS_LONG:
            position = f"{ru}-live-long-{_level}"
            return position
        
        elif _vowel in VOWELS_SHORT:
            position = f"{ru}-dead-short-{_level}"
            return position
        
    if _consonant == 'z':
        if _coda in live and _vowel in VOWELS_LONG:
            position = f"{ru}-live-long-{_level}"
            return position

        elif _coda in dead and _vowel in VOWELS_SHORT:
            position = f"{ru}-dead-short-{_level}"
            return position

        elif _coda == '' and _vowel in VOWELS_LONG:
            position = f"{ru}-live-long-{_level}"
            return position

        elif _coda == '' and _vowel in VOWELS_SHORT:
            position = f"{ru}-dead-short-{_level}"
            return position

def table(position, _consonant, _vowel, _coda, _level):
#     print(position, _consonant, _coda, _vowel, _level, "@table") #table

    #######################################################
    ###########               MID              ############
    #######################################################
    if position[:-2] == 'mid-live-short' or position[:-2] == 'mid-live-long':
        # print('mid_live')
        lv = {
             "0" : "",
             "1" : " ่",
             "2" : " ้",
             "3" : " ๊",
             "4" : " ๋",
        }
        return [mid[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]

    if position[:-2] == 'mid-dead-short' or position[:-2] == 'mid-dead-long':
        # print('mid_dead')
        lv = {
             "0" : "",
             "1" : "",
             "2" : " ้",
             "3" : " ๊",
             "4" : " ๋",
        }
        return [mid[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
    #######################################################
    ###########             LOW  PAIR          ############
    #######################################################
    if position[:-2] == 'low-pair-live-short' or position[:-2] == 'low-pair-live-long':
        lv = {
             "0" : "",
             "1" : " ่",
             "2" : " ่",
             "3" : " ้",
             "4" : "",
        }
        if _level == "1" or _level == "4":
            return [high[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
        else:
            return [low_pair[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
    
    if position[:-2] == 'low-pair-dead-short':
        lv = {
             "0" : "",
             "1" : "",
             "2" : " ่",
             "3" : "",
             "4" : " ๋",
        }
        if _level =="1":
            return [high[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
        else:
            return [low_pair[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
    
    if position[:-2] == 'low-pair-dead-long':
        lv = {
             "0" : "",
             "1" : "",
             "2" : "",
             "3" : " ้",
             "4" : " ๋",
        }
        if _level =="1":
            return [high[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
        else:
            return [low_pair[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
    #######################################################
    ###########           LOW  SINGLE          ############
    #######################################################
    if position[:-2] == 'low-single-live-short' or position[:-2] == 'low-single-live-long':
        lv = {
             "0" : "",
             "1" : " ่",
             "2" : " ่",
             "3" : " ้",
             "4" : "",
        }
        if _level == "1" or _level == "4":
            #
            # print(_consonant+"-")
            return [high[_consonant+"-"], vowels_all[_vowel], CODAS[_coda], lv[_level]] # lowsing
        else:
            return [low_single[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
        
    if position[:-2] == 'low-single-dead-short':
        lv = {
             "0" : "",
             "1" : "",
             "2" : " ้",
             "3" : "",
             "4" : " ๋",
        }
        if _level == "1" or _level == "4":
            #
            # print(_consonant+"-")
            return [high[_consonant+"-"], vowels_all[_vowel], CODAS[_coda], lv[_level]] # lowsing
        else:
            return [low_single[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]
        
    if position[:-2] == 'low-single-dead-long':
        lv = {
             "0" : "",
             "1" : "",
             "2" : "",
             "3" : "้",
             "4" : " ๋",
        }
        if _level == "1" :
            return [high[_consonant+"-"], vowels_all[_vowel], CODAS[_coda], lv[_level]] # lowsing
        else:
            return [low_single[_consonant], vowels_all[_vowel], CODAS[_coda], lv[_level]]

def bypart(syllable):
    _consonant = syllable[0]
    _vowel     = syllable[1]
    _coda      = syllable[2]
    _level     = syllable[3]

#     print(syllable, "@bypart")

    if _consonant in mid: 
        position = positionOnTable("mid",_consonant, _coda, _vowel, _level)
#         print(position)
        text = table(position, _consonant, _vowel, _coda, _level)
        return text

    if _consonant in low_pair: # high
        position = positionOnTable("low-pair",_consonant , _coda, _vowel, _level)
#         print(position)
        text = table(position, _consonant, _vowel, _coda, _level)
        return text

    if _consonant in low_single: # hn
        position = positionOnTable("low-single",_consonant , _coda, _vowel, _level)
#         print(position)
        text = table(position, _consonant, _vowel, _coda, _level)
        return text
