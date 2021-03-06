#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from memoized import memoized
import re

#from redis_memo import redismemo

import parse_corpora

#import stanford

import json

DICTIONARY_FILE = "./cedict_full.txt"
@memoized
def get_dictionary_lines():
  with open(DICTIONARY_FILE) as f:
    return f.readlines()[30:]

@memoized
def get_dictionary():
  ce_dict_hash = {}
  for x in get_dictionary_lines():
    if x.strip() == '':
      continue
    trad_word = x.split(' ')[0]
    simp_word = x.split(' ')[1]
    if simp_word != trad_word and simp_word not in ce_dict_hash:
      ce_dict_hash[simp_word] = x
    ce_dict_hash[trad_word] = x
  return ce_dict_hash

def uniquify(list_of_words):
  set_of_words = set()
  output = []
  for word in list_of_words:
    if word not in set_of_words:
      set_of_words.add(word)
      output.append(word)
  return output

def lookup_word(chinese_word):
  return get_dictionary()[chinese_word]

def list_definitions_for_word(word):
  definition = lookup_word(word)
  definition = definition[definition.index(']')+1:]
  definitions = [x.strip() for x in definition.split('/')]
  return [x for x in definitions if x != '']

@memoized
def get_english_blacklist():
  blacklist = [u'fig', u'one', u'with', u'variant', u'also', u'into', u'abbr', u'have', u'not', u'get', u'China', u'prefecture', u'level', u'from', u'out', u'for', u'take', u'an', u'as', u'at', u'see', u'be', u'by', u'all', u'the', u'eg', u'surname', u'used', u'go', u'written', u'county', u'is', u'it', u'in', u'and', u'on', u'of', u'or', u'idiom', u'oneself', u'Taiwan', u'sb', u'city', u'to', u'person', u'up', u'Tibetan', u'make', u'Chinese', u'Sichuan', u'Japanese', u'name', u'place', u'district', u'capital', u'old', u'time', u'etc', u'that', u'a', u'sth', u'lit', u'state', u'autonomous', u'over', u'water', u'ones']
  stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
  return set(blacklist + stopwords)

@memoized
def get_salient_english_words(text):
  words = re.findall(r'\w+', text) # warning, doesn't do the correct thing on Tōkyō (splits into [T, ky]), should use nltk tokenize instead
  return [word for word in words if word not in get_english_blacklist()]

def segment_chinese_sentence(chinese_sentence):
  #return re.findall(r'\S+', chinese_sentence)
  return [word for word in chinese_sentence.split() if word != '']

@memoized
def get_words_in_chinese_sentence(chinese_sentence):
  #return chinese_sentence.split()
  #words = re.findall(r'\S+', chinese_sentence)
  words = segment_chinese_sentence(chinese_sentence)
  return [word for word in words if word in get_dictionary()]

@memoized
def get_chinese_pos_tagger():
  return stanford.StanfordTagger(lang='zh')

@memoized
def get_english_pos_tagger():
  return stanford.StanfordTagger(lang='en')

def getTag(tagged_word):
  return tagged_word[tagged_word.rindex('#')+1:]

def getWord(tagged_word):
  return tagged_word[:tagged_word.rindex('#')]

# list of word,tag tuples
@memoized
def get_pos_tags_in_chinese_sentence(sentence):
  sentence_nowhitespace = ''.join(sentence.split()).decode('utf-8')
  if sentence_nowhitespace in get_precomputed_chinese_sentence_to_pos_tags():
    tags_for_sentence = get_precomputed_chinese_sentence_to_pos_tags()[sentence_nowhitespace.decode('utf-8')]
    return [(word.decode('utf-8'),tag.decode('utf-8')) for word,tag in tags_for_sentence]
    #return [(getWord(word),tag) for word,tag in tags_for_sentence]
  raise Exception('not found in dictionary:' + sentence)
  words = segment_chinese_sentence(sentence)
  tags = get_chinese_pos_tagger().tag(words)
  return [(getWord(word[0]), getTag(word[0])) for word in tags]

@memoized
def get_precomputed_chinese_sentence_to_pos_tags():
  return json.load(open('tagged_chinese_sentences_full.json'))

def get_pos_tags_in_chinese_sentence_bulk(sentences):
  segmented_sentences = [segment_chinese_sentence(sentence) for sentence in sentences]
  tags_by_sentence = get_chinese_pos_tagger().batch_tag(segmented_sentences)
  return [[(getWord(word[0]), getTag(word[0])) for word in tags] for tags in tags_by_sentence]

# list of word,tag tuples
@memoized
def get_pos_tags_in_english_sentence(sentence):
  words = re.findall(r'\w+', sentence)
  tags = get_english_pos_tagger().tag(words)
  return tags

