#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from reference_definitions import *
from corpus_utils import *

from memoized import memoized
import re

from argmax_impl import *

import mlpy

import heapq

'''
DONT USE - for words like 的 this list is ridiculously long, killing classification performance
@memoized
def get_cooccurring_words(word):
  cooccurring_words = []
  cooccurring_word_set = set()
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    for word in get_words_in_chinese_sentence(sentence):
      if word not in cooccurring_word_set:
        cooccurring_words.append(word)
  return cooccurring_words#[:10]
'''
# @memoized
# def get_top_cooccurring_words(word, topn=100, threshold=0.3):
#   cooccurring_word_counts = {}
#   for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
#     sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
#     for word in get_words_in_chinese_sentence(sentence):
#       if word not in cooccurring_word_counts:
#         cooccurring_word_counts[word] = 0
#       cooccurring_word_counts[word] += 1
#   # for whatever reason normalizing by the total number of occurrences (in order to get rid of really common words) decreases the classification accuracy...
#   counts_and_words = [(count/float(get_training_corpus().get_word_count(word)),word) for word,count in  cooccurring_word_counts.iteritems()]
#   #counts_and_words = [(count,word) for word,count in  cooccurring_word_counts.iteritems()]
#   if threshold > 0.0:
#     counts_and_words = [(value,word) for value,word in counts_and_words if value > threshold]
#   if topn > 0:
#     top_count_words = heapq.nlargest(topn, counts_and_words)
#   else:
#     top_count_words = counts_and_words
#   return [word for count,word in top_count_words]
@memoized
def get_top_cooccurring_words_for_meaning(word,sentences,topn=100, threshold=0.3):
  #print "TOP N", topn
  topn = min(800,topn)
  cooccurring_word_counts = {}
  total_cooccurring_word_count = 0
  for w in get_words_in_chinese_sentence(sentences):
    total_cooccurring_word_count += 1
    if w not in cooccurring_word_counts:
      cooccurring_word_counts[w] = 0
    cooccurring_word_counts[w] += 1
  counts_and_words = [(count/float(total_cooccurring_word_count),w) for w,count in  cooccurring_word_counts.iteritems()]
  if threshold > 0.0:
    counts_and_words = [(value,w) for value,w in counts_and_words if value > threshold]
  if topn > 0:
    top_count_words = heapq.nlargest(topn, counts_and_words)
  else:
    top_count_words = counts_and_words
  return [w for count,w in top_count_words]

@memoized
def get_top_cooccurring_words(word, topn=100, threshold=0.3):
  cooccurring_word_counts = {}
  total_cooccurring_word_count = 0
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    for word in get_words_in_chinese_sentence(sentence):
      total_cooccurring_word_count += 1
      if word not in cooccurring_word_counts:
        cooccurring_word_counts[word] = 0
      cooccurring_word_counts[word] += 1
  # for whatever reason normalizing by the total number of occurrences (in order to get rid of really common words) decreases the classification accuracy...
  counts_and_words = [(count/float(total_cooccurring_word_count),word) for word,count in  cooccurring_word_counts.iteritems()]
  #counts_and_words = [(count,word) for word,count in  cooccurring_word_counts.iteritems()]
  if threshold > 0.0:
    counts_and_words = [(value,word) for value,word in counts_and_words if value > threshold]
  if topn > 0:
    top_count_words = heapq.nlargest(topn, counts_and_words)
  else:
    top_count_words = counts_and_words
  return [word for count,word in top_count_words]

@memoized
def get_total_occuring_count(word):
  total = 0
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    total += len(get_words_in_chinese_sentence(sentence))
  return total

