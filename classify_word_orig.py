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

from classifier_list import *

import math

def word_has_enough_reference_definitions(word, n=50):
  num_ref_definitions = 0
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    reference_definition_idx = get_training_corpus().get_reference_definition_idx(word, sentence)
    if reference_definition_idx == -1: # no reference definition available for this word instance
      continue
    num_ref_definitions += 1
  if num_ref_definitions > n:
    return True
  return False

def word_has_enough_nonmajority_definitions(word, threshold=0.3):
  num_nonmajority_definitions = 0
  num_ref_definitions = 0
  majority_definition_idx = get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word)
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    reference_definition_idx = get_training_corpus().get_reference_definition_idx(word, sentence)
    if reference_definition_idx == -1: # no reference definition available for this word instance
      continue
    num_ref_definitions += 1
    if reference_definition_idx != majority_definition_idx:
      num_nonmajority_definitions += 1
  if num_nonmajority_definitions > threshold*num_ref_definitions:
    return True
  return False

def main(args):
  # arg 1: classifier name
  classifierType = MaxCountClassifier
  if len(args) > 1:
    classifierType = getClassifierByName(args[1])
  print classifierType
  num_word_instances = 0
  skipped_words = 0
  num_word_instances_correctly_classified = 0
  for word in get_training_corpus().list_chinese_words():
    if not word_has_enough_reference_definitions(word):
      skipped_words += 1
      continue
    if not word_has_enough_nonmajority_definitions(word):
      skipped_words += 1
      continue
    print word
    for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
      reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
      if reference_definition_idx == -1: # no reference definition available for this word instance
        continue
      classifier = getClassifier(classifierType, word) # can be changed to a different classifier type
      classified_definition_idx = classifier.get_definition_idx(sentence)
      #print classified_definition_idx, reference_definition_idx
      num_word_instances += 1
      if classified_definition_idx == reference_definition_idx:
        num_word_instances_correctly_classified += 1
      else:
        print word
        print 'correct:', list_definitions_for_word(word)[reference_definition_idx]
        print 'incorrect:', list_definitions_for_word(word)[classified_definition_idx]
        print 'sentence:', sentence
        print 'translation:', get_test_corpus().get_english_sentence_for_chinese(sentence)
        print ''
  print 'Number of skipped words:', skipped_words
  print 'Total number of word instances:', num_word_instances
  print 'Number of word instances correctly classified:', num_word_instances_correctly_classified

if __name__ == '__main__':
  main(sys.argv)

