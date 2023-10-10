import csv
import re
import random
from .map_vectors import (CONSONANTS, 
                          CLUSTERS, 
                          VOWELS_SHORT, 
                          VOWELS_LONG, 
                          DIPTHONGS, 
                          CODAS)  
from .rules import low, mid, high, live, dead, low_single, low_pair, vowels_all
from .bypart import bypart
# import thaispellcheck

def get_consonant(chars): 
    # Consonant & Cluster
    if chars[:3] in CONSONANTS or chars[:3] in CLUSTERS: 
        _consonant = chars[:3]
        _position = 3
    elif chars[:2] in CONSONANTS or chars[:2] in CLUSTERS: 
        _consonant = chars[:2]
        _position = 2
    elif chars[0] in CONSONANTS: 
        _consonant = chars[0]
        _position = 1
    return _consonant, _position

def get_vowels(chars, position): 
    if chars[position:position+3] in DIPTHONGS:
        _vowel = chars[position:position+3]
        _position = position+3
    elif chars[position:position+2] in VOWELS_LONG:
        _vowel = chars[position:position+2]
        _position = position+2
    elif chars[position:position+1] in VOWELS_SHORT:
        _vowel = chars[position:position+1]
        _position = position+1
    else:
        pass
    return _vowel, _position

def get_coda(chars, position):
#     print(chars, position, "@get_coda")
    try:
        if chars[position:position+3] in CODAS:
            _coda = chars[position:position+3]
        elif chars[position:position+2] in CODAS:
            _coda = chars[position:position+2]
    except:
        _coda=""
    return _coda

def get_level(chars, map=False): 
    if "^" not in chars:
        chars = chars + "^0"

    cd = chars.find("^")
    cd = cd + 1

    if map:
        return chars[cd]
    else:
        return chars[cd]

def find_re(syllable):
    re_vowel_wait = []
    re_vowel = ''
    for vowe in vowels_all:
        v = re.search(vowe, syllable)
        if v is not None:
            x = v.span()
            st, en = x[0], x[1]
            re_vowel_wait.append(syllable[st:en])

    if re_vowel_wait:
        re_vowel = re_vowel_wait[-1]
    
    cd = syllable.find("^")

    if syllable[cd-2 : cd+1] in CODAS:
        coda = syllable[cd -2 : cd+1]
    elif syllable[cd-1 : cd+1] in CODAS:
        coda = syllable[cd -1 : cd+1]
    else:
        coda = 'z^'
    
#     print(syllable, "")
    if syllable[-1] in ['0','1','2','3','4']:
        leve = syllable[-1]
    else:
        leve = '0'

    cons = syllable.replace(re_vowel,"")
    cons = cons.replace(coda,"")
    cons = cons.replace(leve,"")
    cons = cons.replace("^","")

    if not cons:
        cons = "z"

    if cons in CONSONANTS:
        pass
    else:
        cons = random.choice(cons)

#     print(cons, re_vowel, coda, leve, "@count")

    return (cons, re_vowel, coda, leve)

def count_position_chars(chars):
#     print(chars, "@count_position_chars")
    try:
        _consonant, _position_consonant = get_consonant(chars)
        _vowel, _position_vowels = get_vowels(chars, _position_consonant)
        _coda = get_coda(chars, _position_vowels)
        _level = get_level(chars)
#         print("+++++++RULES+++++++")
    except:
        _consonant, _vowel, _coda, _level = find_re(chars)
#         print("+++++++ R E +++++++")
    # _consonant, _vowel, _coda, _level = find_re(chars)
    return _consonant, _vowel, _coda, _level

def format_thai(translated):
#     print(translated, "@translate")
    _consonant = translated[0]
    _vowel = translated[1]
    _coda = translated[2]
    _level = translated[3]

    # short vowels
    if _vowel == 'อะ': 
        if _coda =='':
            text = _consonant + _level + "ะ"
        elif _coda == 'ว': 
            text = "เ"+ _consonant + _level + "า"
        elif _coda == 'ม': 
            text = _consonant + _level + "ำ"
        elif _coda == 'ย': 
            text = "ใ" + _consonant + _level 
        elif _coda != '': 
            text = _consonant  + "ั" + _level + _coda
    
    elif _vowel == 'อิ':
        text = _consonant + "ิ" + _level + _coda

    elif _vowel == 'อุ': 
        text = _consonant + "ุ" + _level + _coda

    elif _vowel == 'เอะ': 
        if _coda != '':
            text = "เ" + _consonant + "็" + _coda
        elif _coda == '': 
            text = "เ" + _consonant + _level + "ะ"
    
    elif _vowel == 'โอะ': 
        if _coda != '':
            text = _consonant + _level + _coda
        elif _coda == '': 
            text = "โ" + _consonant + _level + "ะ"
    
    elif _vowel == 'อึ': 
        text = _consonant + "ึ" + _level + _coda

    elif _vowel == 'เออะ': 
        text = "เ" + _consonant + _level + "อะ"

    elif _vowel == 'เอาะ': 
        if _coda != '':
            text = _consonant + _level + "อ"  + _coda
        elif _coda == '': 
            text = "เ" + _consonant + _level + "าะ"

    elif _vowel == 'แอะ': 
        text = "แ" + _consonant + _level + "ะ"

    #long vowels
    if _vowel == 'อา': 
        text = _consonant + _level + "า" + _coda

    elif _vowel == 'อี':
        text = _consonant + "ี" + _level + _coda

    elif _vowel == 'อู': 
        text = _consonant + "ู" + _level + _coda

    elif _vowel == 'เอ': 
        text = "เ" + _consonant + _level + _coda
    
    elif _vowel == 'โอ': 
        text = "โ" + _consonant + _level + _coda
    
    elif _vowel == 'อื': 
        if _coda == '':
            text = _consonant + "ื" + _level + "อ"
        elif _coda != '':
            text = _consonant + "ื" + _level + _coda

    elif _vowel == 'เออ': 
        if _coda != '':
            text = "เ" + _consonant + "ิ" + _level + _coda
        elif _coda == '':
            text = "เ" + _consonant + _level + "อ"

    elif _vowel == 'ออ': 
        if _coda != '':
            text = _consonant + _level + "อ" + _coda
        elif _coda == '':
            text = _consonant + _level + "อ"
 
    elif _vowel == 'แอ': 
        text = "แ" + _consonant + _level + _coda


    # Dipthongs
    elif _vowel == 'เอียะ': 
        text = "เ" + _consonant + "ี" + _level + "ยะ"
    
    elif _vowel == 'เอีย': 
        text = "เ" + _consonant + "ี" +_level + "ย" + _coda

    elif _vowel == 'เอือะ': 
        text = "เ" + _consonant + _level + "อะ"
    
    elif _vowel == 'เอือ': 
        if _coda == '':
            text = "เ" + _consonant + "ื" + _level + "อ"
        elif _coda !=' ':
            text = "เ" + _consonant + "ื" + _level + "อ" + _coda
    
    elif _vowel == 'อัวะ': 
        text = _consonant + "ั" +_level + "วะ"
    
    elif _vowel == 'อัว': 
        if _coda == '':
            text = _consonant + "ั" + _level + "ว"
            
        elif _coda == 'ว':
            text = "เ" + _consonant + _level + "า"
            
        elif _coda != '':
            text = _consonant + _level + "ว" + _coda
        
    elif _vowel == 'เอา': 
        text = "เ" + _consonant + _level + "า"

    return text

def indentifies_alphabet(sentences):
    sentences = sentences.replace("  "," ").split(" ")
    
    to_decode = []
    
    for word in sentences: 

        syllable_identifies = count_position_chars(word)
#         print(syllable_identifies, "@syllable_identifies") 

        define_levels = bypart(syllable_identifies)
        # print(define_levels ,"@bypart")

        translated = format_thai(define_levels)
        # print(translated)

        to_decode.append(translated.replace(" ",""))
        
    return ' '.join(to_decode)

def saparate_componant(sentences, type_):
    keep = []

    data_split_list = sentences.replace("|"," ")
    data_split_list = data_split_list.replace("^ ","^")
    data_split_list = data_split_list.replace("   "," ")
    data_split_list = data_split_list.replace("  "," ").split(" ")
    
    if type_ == 'level':
        for syllable in data_split_list: 
            syllable_identifies = count_position_chars(syllable)
            if syllable_identifies[-1]:
                re_search = find_re(syllable_identifies[-1])
                level = re_search[-1] 
                keep.append(level)
            else:
                level = syllable[-1]
                keep.append(level)

    elif type_ == 'phone':
        for syllable in data_split_list: 
            try:
                syllable_identifies = count_position_chars(syllable)
                phone = syllable_identifies[0] + " " + syllable_identifies[1] + " " + syllable_identifies[2] 
                keep.append(phone)
            except:
                re_search = find_re(syllable)
                phone = re_search[0] + " " + re_search[1] + " " + re_search[2] 
                keep.append(phone)

    elif type_ == 'both':
        for syllable in data_split_list: 
            try:
                syllable_identifies = count_position_chars(syllable)
                phone = syllable_identifies[0] + " " + syllable_identifies[1] + " " + syllable_identifies[2] + " " + syllable_identifies[3]
                keep.append(phone)
            except:
                re_search = find_re(syllable)
                phone = re_search[0] + " " + re_search[1] + " " + re_search[2] + " " + re_search[3]
                keep.append(phone)
                
    elif type_ == 'delimeter':
        for syllable in data_split_list: 
            try:
                syllable_identifies = count_position_chars(syllable)
                phone = syllable_identifies[0] + "|"  + syllable_identifies[1] + "|" + syllable_identifies[2] + "|" + syllable_identifies[3] + "|"
                keep.append(phone)
            except:
                re_search = find_re(syllable)
                phone = re_search[0] + "|" + re_search[1] + "|" + re_search[2] + "|" + re_search[3] + "|"
                keep.append(phone)

    elif type_ == 'only_phone': 
        for syllable in data_split_list: 
            syllable_identifies = count_position_chars(syllable)
            if syllable_identifies[-1]:
                # phone = " ".join(syllable_identifies[-1])
                phone = syllable_identifies[-1]
                phone = phone.replace("0","")
                phone = phone.replace("1","")
                phone = phone.replace("2","")
                phone = phone.replace("3","")
                phone = phone.replace("4","")
                # print(phone)
            else:
                phone = syllable_identifies[0] + " " + syllable_identifies[1] + " " + syllable_identifies[2] + "^" 
            keep.append(phone)

    elif type_ == 'only_level': 
        for syllable in data_split_list: 
            syllable_identifies = count_position_chars(syllable)
            if syllable_identifies[-1]:
                re_search = find_re(syllable_identifies[-1])
                level = re_search[-1] 
                keep.append(level)
            else:
                level = syllable[-1]
            keep.append(level)
    keep = ' '.join(keep)
    return keep

def P2G(sentence): 
    thai = indentifies_alphabet(sentence)
    return thai




