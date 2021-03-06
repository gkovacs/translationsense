#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from reference_definitions import *

from memoized import memoized
import re

import parse_corpora

import heapq

from argmax_impl import *

class ParallelCorpus:
  def __init__(self, chinese_sentences, english_sentences):
    assert len(chinese_sentences) == len(english_sentences)
    self.chinese_sentences = chinese_sentences
    self.english_sentences = english_sentences

  def get_sentence_at_idx(self, sentence_idx):
    return self.chinese_sentences[sentence_idx]

  @memoized
  def list_chinese_words(self):
    words = []
    word_set = set()
    dictionary = get_dictionary()
    for sentence in self.chinese_sentences:
      for word in get_words_in_chinese_sentence(sentence):
        if word not in word_set and word in dictionary:
          word_set.add(word)
          words.append(word)
    return words

  @memoized
  def get_chinese_to_english_sentence_mapping(self):
    chinese_to_english = {}
    for chinese_sent,english_sent in zip(self.chinese_sentences, self.english_sentences):
      chinese_to_english[chinese_sent] = english_sent
    return chinese_to_english

  def get_english_sentence_for_chinese(self, chinese_sent):
    return self.get_chinese_to_english_sentence_mapping()[chinese_sent]
  
  @memoized
  def get_words_to_sentence_idxes_it_occurs_in(self):
    # dictionary of word => set of sentence idxes it occurs in
    words_to_sentence_idxes_it_occurs_in = {}
    for sentence_idx,sentence in enumerate(self.chinese_sentences):
      words = get_words_in_chinese_sentence(sentence)
      for word in words:
        if word not in words_to_sentence_idxes_it_occurs_in:
          words_to_sentence_idxes_it_occurs_in[word] = set()
        words_to_sentence_idxes_it_occurs_in[word].add(sentence_idx)
    return words_to_sentence_idxes_it_occurs_in

  def sentence_idxes_word_occurs_in(self, word):
    idx_set = self.get_words_to_sentence_idxes_it_occurs_in()
    if word not in idx_set:
      return frozenset()
    return idx_set[word]

  def sentence_idxes_both_words_occur_in(self,word1,word2):
    return self.sentence_idxes_word_occurs_in(word1) & self.sentence_idxes_word_occurs_in(word2) # & is the set intersection operator
  
  def sentence_idxes_either_word_occurs_in(self,word1,word2):
    return self.sentence_idxes_word_occurs_in(word1) | self.sentence_idxes_word_occurs_in(word2) # | is the set union operator
  
  @memoized
  def word_counts_in_corpus(self):
    word_counts = {}
    for sentence in self.chinese_sentences:
      for word in get_words_in_chinese_sentence(sentence):
        if word not in word_counts:
          word_counts[word] = 0
        word_counts[word] += 1
    return word_counts
  

  @memoized
  def get_top_words(self,n):
    d = self.word_counts_in_corpus()
    d = [(value,word) for word,value in d.iteritems()]
    return heapq.nlargest(n, d)


  def get_word_count(self, word):
    if word in self.word_counts_in_corpus():
      return self.word_counts_in_corpus()[word]
    return 0

  @memoized
  def english_word_counts_in_corpus(self):
    word_counts = {}
    for sentence in self.english_sentences:
      for word in get_salient_english_words(sentence):
        if word not in word_counts:
          word_counts[word] = 0
        word_counts[word] += 1
    return word_counts

  def get_english_word_count(self, word):
    if word in self.english_word_counts_in_corpus():
      return self.english_word_counts_in_corpus()[word]
    return 0

  @memoized
  def get_reference_definition_idx_counts(self, word):
    definition_idx_to_count = {}
    for sentence_idx in self.sentence_idxes_word_occurs_in(word):
      sentence = self.get_sentence_at_idx(sentence_idx)
      definition_idx = self.get_reference_definition_idx(word, sentence)
      if definition_idx not in definition_idx_to_count:
        definition_idx_to_count[definition_idx] = 0
      definition_idx_to_count[definition_idx] += 1
    return definition_idx_to_count

  @memoized
  def get_reference_definition_idx_counts_excluding_neg1(self, word):
    definition_idx_to_count = dict(self.get_reference_definition_idx_counts(word))
    if -1 in definition_idx_to_count:
      del definition_idx_to_count[-1]
    return definition_idx_to_count

  def get_most_common_reference_definition_idx(self, word):
    definition_idx_to_count = self.get_reference_definition_idx_counts(word)
    if len(definition_idx_to_count) == 0:
      return -1
    return argmax(definition_idx_to_count)
  
  def get_most_common_reference_definition_idx_excluding_neg1(self, word):
    definition_idx_to_count = self.get_reference_definition_idx_counts_excluding_neg1(word)
    if len(definition_idx_to_count) == 0:
      return -1
    return argmax(definition_idx_to_count)

  def get_reference_definition_idx(self, word, chinese_sent):
    '''
    -1 if no reference definition idx was found
    otherwise list_definitions_for_word(word)[val] will be the reference definition for the word
    '''
    english_sent = self.get_english_sentence_for_chinese(chinese_sent)
    english_words_in_sent = set(get_salient_english_words(english_sent))
    definition_scores = []
    if word not in get_dictionary():
      return -1
    try:
      definitions = list_definitions_for_word(word)
    except:
      return -1
    for idx,definition in enumerate(definitions):
      english_words_in_definition = get_salient_english_words(definition)
      definition_score = sum([inverse_freq_score(word) for word in english_words_in_definition if word in english_words_in_sent])
      #definition_score = sum([1.0 for word in english_words_in_definition if word in english_words_in_sent])
      definition_scores.append((definition_score,-idx))
    bestscore,negbestidx = max(definition_scores)
    bestidx = -negbestidx
    if bestscore == 0:
      return -1
    return bestidx

def inverse_freq_score(w):
  wc = get_training_corpus().get_english_word_count(w)
  if wc == 0:
    return 0
  return 1.0/wc

@memoized
def get_training_data():
  #return parse_corpora.get_alignments(320, 0) # 0 through 49
  return parse_corpora.get_alignments(100, 0)

@memoized
def get_test_data():
  #return parse_corpora.get_alignments(24, 321) # 50 through 60
  return parse_corpora.get_alignments(10, 99) # 0 through 49

@memoized
def get_training_corpus():
  chinese_sentences,english_sentences = get_training_data()
  return ParallelCorpus(chinese_sentences, english_sentences)

@memoized
def get_test_corpus():
  chinese_sentences,english_sentences = get_test_data()
  return ParallelCorpus(chinese_sentences, english_sentences)

'''
@memoized
def get_combined_corpus():
  chinese_sentences_train,english_sentences_train = get_training_data()
  chinese_sentences_test,english_sentences_test = get_test_data()
  return ParallelCorpus(chinese_sentences_train + chinese_sentences_test, english_sentences_train + english_sentences_test)
'''
