#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from reference_definitions import *

from memoized import memoized
import re

from argmax_impl import *

@memoized
def get_words_to_sentence_idxes_it_occurs_in():
  # dictionary of word => set of sentence idxes it occurs in
  words_to_sentence_idxes_it_occurs_in = {}
  for sentence_idx,sentence in enumerate(list_chinese_sentences()):
    words = get_words_in_chinese_sentence(sentence)
    for word in words:
      if word not in words_to_sentence_idxes_it_occurs_in:
        words_to_sentence_idxes_it_occurs_in[word] = set()
      words_to_sentence_idxes_it_occurs_in[word].add(sentence_idx)
  return words_to_sentence_idxes_it_occurs_in

def sentence_idxes_word_occurs_in(word):
  return get_words_to_sentence_idxes_it_occurs_in()[word]

def sentence_idxes_both_words_occur_in(word1,word2):
  return sentence_idxes_word_occurs_in(word1) & sentence_idxes_word_occurs_in(word2) # & is the set intersection operator

@memoized
def get_reference_definition_idx_counts(word):
  definition_idx_to_count = {}
  for sentence_idx in sorted(list(sentence_idxes_word_occurs_in(word))):
    sentence = get_sentence_at_idx(sentence_idx)
    definition_idx = get_reference_definition_idx(word, sentence)
    if definition_idx not in definition_idx_to_count:
      definition_idx_to_count[definition_idx] = 0
    definition_idx_to_count[definition_idx] += 1
  return definition_idx_to_count

def most_common_reference_definition_idx(word):
  definition_idx_to_count = get_reference_definition_idx_counts(word)
  return argmax(definition_idx_to_count)

for word in list_chinese_words():
  definition_idx_to_count = get_reference_definition_idx_counts(word)
  if -1 in definition_idx_to_count and len(definition_idx_to_count) == 1:
    continue # no reference definitions for this word
  print word, definition_idx_to_count
  

