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

def main(args):
  # arg 1: classifier name
  # arg 2: number of reference definitions needed
  num_reference_definitions_needed = 10
  classifierType = MaxCountClassifier
  if len(args) > 1:
    classifierType = getClassifierByName(args[1])
  print classifierType
  if len(args) > 2:
    num_reference_definitions_needed = int(args[2])
  num_word_instances = 0
  skipped_words = 0
  num_word_instances_correctly_classified = 0
  for word in get_training_corpus().list_chinese_words():
    if get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word) == -1: # no reference definitions available for this word in the training data
      continue
    num_reference_definitions = 0
    for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
      reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
      if reference_definition_idx == -1: # no reference definition available for this word instance
        continue
      num_reference_definitions += 1
    if num_reference_definitions < num_reference_definitions_needed:
      skipped_words += 1
      continue
    classifier = getClassifier(classifierType, word) # can be changed to a different classifier type
    print word
    for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
      reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
      if reference_definition_idx == -1: # no reference definition available for this word instance
        continue
      classified_definition_idx = classifier.get_definition_idx(sentence)
      num_word_instances += 1
      if classified_definition_idx == reference_definition_idx:
        num_word_instances_correctly_classified += 1
  print 'Number of skipped words:', skipped_words
  print 'Total number of word instances:', num_word_instances
  print 'Number of word instances correctly classified:', num_word_instances_correctly_classified

if __name__ == '__main__':
  main(sys.argv)

