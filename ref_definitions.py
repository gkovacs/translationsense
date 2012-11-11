#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, string, re
DICTIONARY_FILE = "./cedict_full.txt"

def get_dictionary():
        with open(DICTIONARY_FILE) as f:
                ce_dict = f.readlines()[30:]
                return [s.decode('utf-8') for s in ce_dict]

def get_blacklist(ce_dict):
        '''
        word_counts = {}
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        for line in ce_dict:
                for meaning in line.split("/")[1:-1]:
                        meaning = regex.sub('', meaning)
                        words_in_meaning = meaning.split(' ')
                        words = [s for s in words_in_meaning if all((ord(c) < 123 and ord(c) > 64) for c in s)]
                        for word in words:
                                if word in word_counts:
                                        word_counts[word] +=1
                                else:
                                        word_counts[word] = 1
        print "vocab size: %s" % len(word_counts)
        blacklist = []
        for word in word_counts:
                if word_counts[word] > 500:
                        blacklist.append(word)
                        print "count of %s: %s" % (word, word_counts[word])
        print blacklist
        '''
        return [u'fig', u'one', u'with', u'variant', u'also', u'into', u'abbr', u'have', u'not', u'get', u'China', u'prefecture', u'level', u'from', u'out', u'for', u'take', u'an', u'as', u'at', u'see', u'be', u'by', u'all', u'the', u'eg', u'surname', u'used', u'go', u'written', u'county', u'is', u'it', u'in', u'and', u'on', u'of', u'or', u'idiom', u'oneself', u'Taiwan', u'sb', u'city', u'to', u'person', u'up', u'Tibetan', u'make', u'Chinese', u'Sichuan', u'Japanese', u'name', u'place', u'district', u'capital', u'old', u'time', u'etc', u'that', u'a', u'sth', u'lit', u'state', u'autonomous', u'over', u'water', u'ones']

def get_english_definitions(word, ce_dict):
        '''
        Returns a list of the possible english meanings of a chinese word.
        if word == '因':
                return ['cause', 'reason', 'because']
        returns -1 if not matches were found
        '''
        uni_word = word.decode('utf-8')
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        for definition in ce_dict:
                index = definition.find(uni_word)
                if index == 0:
                        return [regex.sub('', meaning) for meaning in definition.split("/")[1:-1]]
        return -1

def get_salient_english_words(definition, blacklist):
        '''
        if definition == 'a commission paid to a middleman':
                return ['commission', 'paid', 'middleman']
        '''
        # count up # of occurences of this english word in dictionary definitions
        # if really high, throw out
        return [s for s in definition.split(' ') if s not in blacklist]

def get_best_definition_index(english_words, words_in_each_def):
        '''
        define a match to be that any of the words in the definition are found
        in the bag of english words
        returns -1 if no matches were found
        '''
        for i in range(len(words_in_each_def)):
                for word in words_in_each_def[i]:
                        if word in english_words:
                                return i
        return -1

def read_all_the_files():
        return ([],[])

def segment_chinese(c_sent):
        return c_sent.split(' ')
                                
def main(args):
        ce_dict = get_dictionary()
        blacklist = get_blacklist(ce_dict)
        (chinese_list_of_lists, english_list_of_lists) = read_all_the_files()
        undefined_words = 0
        defined_words = 0
        definition_poll = [0] * 20
        for i in range(len(chinese_list_of_lists)):
                english = english_list_of_lists[i]
                chinese = chinese_list_of_lists[i]
                chinese_words = segment_chinese(chinese)
                english_words = segment_english(english)
                for chinese_word in chinese_words:
                        english_definitions = get_english_definitions(chinese_word)
                        # log
                        if english_definitions == -1:
                                undefined_words +=1
                                continue
                        else:
                                defined_words +=1
                        words_in_each_definition = [get_salient_english_words(definition) for definition in english_definitions]
                        best_definition_index = get_best_definition_index(english_words, words_in_each_definition)
                        # log
                        definition_poll[best_definition_index + 1] += 1

        print "number of defined words: %s" % defined_words
        print "number of undefined words: %s" % undefined_words
        print "aggregate occurrence of chosen meanings: %s" % definition_poll
        return

        '''
        #print get_english_definitions('因', ce_dict)
        definition = get_english_definitions('一中原則', ce_dict)
        for meaning in definition:
                print "def: %s \n %s" % (meaning, get_salient_english_words(meaning, blacklist))

        english = 'Economic development of the last 20 years has brought people surging into the cities to supply industrial manpower.'
        chinese = '中華民國台灣地區，因經濟迅速成長，農村人口大量湧進都市。'
        chinese_words = segment_chinese(chinese)
        english_words = segment_english(english)
        for chinese_word in chinese_words:
                english_definitions = get_english_definitions(chinese_word)
                words_in_each_definition = [get_salient_english_words(definition) for definition in english_definitions]
                best_definition_index = get_best_definition_index(english_words, words_in_each_definition)
        '''

if __name__ == '__main__':
        main(sys.argv)
