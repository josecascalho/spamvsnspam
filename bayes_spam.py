import os
from typing import Dict, Any, Union

def read_testfile(_path:str,_file:str) ->list:
    f = open(os.path.join(_path, _file), 'r')
    words_list =[]
    for row in f:
        words = row.split()
    for w in words:
        if len(w) >= 3:
            words_list.append(w)
    return words_list

def test_file(words:int,prob_spam_dict:dict,prob_nonspam_dict:dict,spam_e:int,nonspam_e:int)->[float,float]:
    nonspam_prob = 0.5
    spam_prob = 0.5
    w_in_spam = 0
    w_in_nspam = 0
    for w in words:
        if w in prob_spam_dict.keys():
            spam_prob = spam_prob * prob_spam_dict[w]
            w_in_spam += 1
            # Add a correction to nonspam
            if w not in prob_nonspam_dict.keys():
                nonspam_prob = nonspam_prob*(1/nonspam_e)
                w_in_nspam += 1
        if w in prob_nonspam_dict.keys():
            nonspam_prob = nonspam_prob * prob_nonspam_dict[w]
            w_in_nspam += 1
            # Add a correction to spam
            if w not in prob_spam_dict.keys():
                spam_prob = spam_prob*(1/spam_e)
                w_in_spam += 1

    print("The value for being SPAM is:",spam_prob)
    print("The value being NON SPAM is:",nonspam_prob)
    print("Words in spam:",w_in_spam)
    print("Words not in spam:",w_in_nspam)
    return spam_prob,nonspam_prob

def testfile_dict(_path:str, _file:str) -> Dict[str,Union[int,any]]:
    files = os.listdir(_path)
    _dict ={}
    if _file in files:
            # Test
            # print("Openning file:",_file)
            f=open(os.path.join(_path,_file),'r')
            for row in f:

                words = row.split()
                for w in words:
                    if w in _dict:
                        _dict[w] = _dict[w] + 1
                    else:
                        if len(w) >= 3:
                            _dict[w] = 1
            f.close()
    return _dict

def stat_dict(dict:Dict[str,Union[int,any]],nr_elem:int) ->Dict[str,Union[float,any]]:
    stat_d ={}
    for key, value in dict.items():
        stat_d[key] = value / nr_elem
    return stat_d


def merge_dict(dict1:Dict[str,Union[int,any]],dict2:Dict[str,Union[int,any]]) -> Dict[str,Union[int,any]]:
    dict3 = {}
    for key, value in dict1.items():
        if key in dict2:
            dict3[key] = value + dict2[key]
            # in common (test)
            #print("In common:",key)
        else:
            dict3[key] = value
    return dict3

def spam_dict(_path:str) -> Dict[str,Union[int,any]]:
    files = os.listdir(_path)
    #Test
    #print(files)
    _dict = {}
    for file in files:
        if os.path.isfile(os.path.join(_path,file)):
            #Test
            #print("File:",file)
            f=open(os.path.join(_path,file),'r')
            for row in f:
                #Test
                #print("Row in file: ",row)
                #Split in words
                words = row.split()
                for w in words:
                    if w in _dict:
                        _dict[w] = _dict[w] + 1
                    else:
                        if len(w) >= 3:
                            _dict[w] = 1
            #Test
            #print(spam_d.keys())
            #print(spam_d.values())
            f.close()
    return _dict

def main():

    #Getting data from the train
    _path = './data/spam-train'
    spam_d = spam_dict(_path)
    print("Lê ficheiros da pasta:",_path)
    print("Dicionário SPAM:",spam_d.items())
    _path = './data/nonspam-train'
    nonspam_d = spam_dict(_path)
    all_d = merge_dict(spam_d, nonspam_d)
    # Filtering data (selecting only part of the words
    print("Lê ficheiros da pasta:",_path)
    print("Dicionário não spam:", nonspam_d.items())

    #nonspam_d = dict( (k, v) for k, v in nonspam_d.items() if v >= 100)
    #spam_d = dict( (k, v) for k, v in spam_d.items() if v >= 100)
    # Nr. of elements
    nonspam_e =  sum (nonspam_d.values())
    spam_e =  sum (spam_d.values())


    # Using the naive bayes to decide
    # P(spam | WS) = P( WS | spam) P(spam) / P(WS)
    # P(nonspam | WS) = P(WS | nonspam) P(nonpam ) / P(WS)
    # 1- Probability of P(spam | WS) > P(nonspam | WS) or vice-versa.
    # 2- WS = words in the email to be tested
    # 3- P(WS) doesn't need to be considered
    # 4- P(spam) and P(nospam) are the probability of being a spam or not a spam.
    # We can assume they are equal (trainning spam and nonspam messagens should be in equal number)
    # 5- For each word in WS, using the concept of independency between P(w),
    # P(WS|nonspam)=P(w1|nonspam)*P(w2|nonspam)*...*P(wn|nonspam)
    # P(WS|spam)=P(w1|spam)*P(w2|spam)*...*P(wn|spam)
    # 6- P(w|nonspam) or P(w|spam) is calculated:
    # Dividing number of  w repetitions in spam messages divided by the number of words in all spam messages


    # Preparing naive data:
    # For each word, find its probability in each dictionary
    prob_spam_dict = stat_dict(spam_d, spam_e)
    prob_nonspam_dict = stat_dict(nonspam_d,nonspam_e)
    print(prob_spam_dict.items())
    print(prob_nonspam_dict.items())



    # Get a file spam-test:
    # Try to get it in prob_spam_dict and in prob_nonspam_dict ...
    words = read_testfile('./data/nonspam-test','6-7msg2.txt')
    #Spam & nonspam
    #Printing words in common:
    in_spam = 0
    nin_spam = 0
    #for w in words:
    #    if w in prob_spam_dict.keys():
    #        in_spam = in_spam +1
    #    if w in prob_nonspam_dict.keys():
    #        nin_spam = nin_spam +1
    #print("Not in spam:",nin_spam)
    #print("In spam:",in_spam)
    #print("Words in spam:",spam_e)
    #print("Words in nspam:",nonspam_e)
    # Nro. de mensagens que tenho de cada um dos dois tipos
    spam, nonspam = test_file(words,prob_spam_dict,prob_nonspam_dict,spam_e,nonspam_e)
    if ( spam > nonspam):
        print("The file is spam (spam=",spam,",nonspam=",nonspam,")")
    else:
        print("The file is nonspam (spam=",spam,",nonspam=",nonspam,")")

main()