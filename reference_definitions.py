#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from memoized import memoized
import re

import parse_corpora

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

@memoized
def list_chinese_english_sentence_pairs():
  return parse_corpora.get_alignments(30)

@memoized
def list_chinese_sentences():
  return list_chinese_english_sentence_pairs()[0]

def get_sentence_at_idx(sentence_idx):
  return list_chinese_sentences()[sentence_idx]

def get_words_in_chinese_sentence(chinese_sentence):
  return chinese_sentence.split()

@memoized
def list_chinese_words():
  words = []
  word_set = set()
  dictionary = get_dictionary()
  for sentence in list_chinese_sentences():
    for word in get_words_in_chinese_sentence(sentence):
      if word not in word_set and word in dictionary:
        word_set.add(word)
        words.append(word)
  return words

@memoized
def get_chinese_to_english_sentence_mapping():
  chinese_to_english = {}
  chinese_sentences,english_sentences = list_chinese_english_sentence_pairs()
  for chinese_sent,english_sent in zip(chinese_sentences,english_sentences):
    chinese_to_english[chinese_sent] = english_sent
  return chinese_to_english

def get_english_sentence_for_chinese(chinese_sent):
  return get_chinese_to_english_sentence_mapping()[chinese_sent]

def get_reference_definition_idx(word, chinese_sent):
  '''
  -1 if no reference definition idx was found
  otherwise list_definitions_for_word(word)[val] will be the reference definition for the word
  '''
  english_sent = get_english_sentence_for_chinese(chinese_sent)
  english_words_in_sent = set(get_salient_english_words(english_sent))
  definition_scores = []
  for idx,definition in enumerate(list_definitions_for_word(word)):
    english_words_in_definition = get_salient_english_words(definition)
    definition_score = len([word for word in english_words_in_definition if word in english_words_in_sent])
    definition_scores.append((definition_score,idx))
  bestscore,bestidx = max(definition_scores)
  if bestscore == 0:
    return -1
  return bestidx


