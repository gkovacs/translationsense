#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, string, re
import parse_corpora
#from nltk.corpus import stopwords
DICTIONARY_FILE = "./cedict_full.txt"
#stopwords = stopwords.words('english')
stopwords = []
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
        num_choices = len(words_in_each_def)
        matches = [0] * num_choices
        for i in range(num_choices):
                matches[i] = sum([1 for word in words_in_each_def[i] if (word in english_words)])
        num_matching_defs = sum([1 for match in matches if (match>0)])
        
        best_choice = max(range(num_choices), key = lambda x: matches[x])

        if num_matching_defs == 0:
                return (-1, -1)
        elif num_matching_defs == 1:
                return (best_choice, 1)
        else:
                return(best_choice, 0)

def read_all_the_files():
        return parse_corpora.get_alignments(50)

def segment_sent(c_sent):
        return c_sent.split(' ')

def find_common_words(list1,list2):	
	#MUST GET RID OF COMMON WORDS SUCH AS THE, A, ETC
	for word in list1:
		if word not in stopwords:
			if word in list2:
				return True
	return False

def build_chinese_word_sent_dict(read_start, read_end, prev_dict):
    '''
    This will map a single chinese word to 
    a tuple - (sentence_index,english_meaning)
    where sentence_index is the index of the sentence
    in the list of sentences
    '''
    ce_dict = get_dictionary()
    blacklist = set(get_blacklist(ce_dict) + stopwords)
    chinese_word_sent_dict = {}                
    (chinese_sents, english_sents) = read_all_the_files()
    undefined_words = 0
    defined_words = 0
    correct = 0
    incorrect = 0
    words_with_single_def = 0
    words_with_multiple_defs = 0
    instances_with_single_def = 0
    instances_with_multiple_defs = 0
    definition_counts = []
    definition_count_instances = []
    definition_poll = [0] * 50
    match_scores = [0] * 3
    for i in range(read_start, read_end):
    	c_sent = chinese_sents[i]
    	c_sent_words = segment_sent(c_sent)
    	for c_word in c_sent_words:
    		#check if word has a sense
    		sense = False
    		ce_definition = get_english_definitions(c_word, ce_dict)
    		if ce_definition == -1:
    			undefined_words +=1
    			continue
		definition_count_instances.append(len(ce_definition))
		if len(ce_definition) > 1:
			instances_with_multiple_defs += 1
		else:
			instances_with_single_def += 1
		if not c_word in chinese_word_sent_dict:
			definition_counts.append(len(ce_definition))
			if len(ce_definition) > 1:
				words_with_multiple_defs += 1
			else:
				words_with_single_def += 1
		defined_words +=1
		ce_definitions = [x.lower() for x in ce_definition]
		e_corpora_words = [x.lower() for x in segment_sent(english_sents[i])]

		words_in_each_definition = [get_salient_english_words(definition,blacklist) for definition in ce_definitions]
		(sense_index, score) = get_best_definition_index(e_corpora_words, words_in_each_definition)
		try:
			definition_poll[sense_index + 1] += 1
		except IndexError as e:
			print e
			print sense_index
		match_scores[score + 1] += 1

    		if sense_index != -1:
			if baseline_is_correct(c_word, sense_index, prev_dict):
				correct +=1
			else:
				incorrect +=1
    			if c_word in chinese_word_sent_dict:
    				chinese_word_sent_dict[c_word].append((i, sense_index, score))
    			else:
    				chinese_word_sent_dict[c_word] = [(i, sense_index, score)]

    print "number of defined words: %s" % defined_words
    print "number of undefined words: %s" % undefined_words
    print "aggregate occurrence of chosen meanings: %s" % definition_poll
    print "match scoring: %s" % match_scores
    print "correct/incorrect: %s/%s" % (correct,incorrect)
    print "instances multiple/single: %s/%s" % (instances_with_multiple_defs, instances_with_single_def)
    print "words multiple/single: %s/%s" % (words_with_multiple_defs, words_with_single_def)
    print "size of dict: %s" % len(chinese_word_sent_dict)
    print "entries in dict: %s" % sum([len(entry) for entry in chinese_word_sent_dict])
    counts = Counter(definition_counts)
    print "number of definitions for words: %s" % counts.most_common()
    counts = Counter(definition_count_instances)
    print "number of definitions for all instances of words: %s" % counts.most_common()
    return chinese_word_sent_dict

from collections import Counter
def get_most_common_index_dictionary(c_word_sent_dict):
	baseline_dict = {}
	for c_word in c_word_sent_dict:
		counts = Counter([tup[1] for tup in c_word_sent_dict[c_word]])
		(most_common_index, unused) = counts.most_common(1)[0]
		baseline_dict[c_word] = most_common_index
	return baseline_dict

def baseline_is_correct(c_word, index, baseline_dict):
	''' returns True if index is the most common index for that word.
	false otherwise, including if the word isn't found in the index.
	'''
	if c_word in baseline_dict:
		return baseline_dict[c_word] == index
	else:
		return False

def main(args):
	c_sent_dict = build_chinese_word_sent_dict(3500, 5000, {})
	print "REFERENCE DICTIONARY BUILT, MAKING BASELINE..."
	prev_dict = get_most_common_index_dictionary(c_sent_dict)
	print "BASELINE DONE, SCORING NEXT SET.."
	build_chinese_word_sent_dict(3500, 5000, prev_dict)

if __name__ == '__main__':
    main(sys.argv)