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

def get_classifier_for_word(word):
  

num_word_instances = 0
num_word_instances_correctly_classified = 0
for word in get_training_corpus().list_chinese_words():
  best_definition_idx = get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word)
  if best_definition_idx == -1:
    continue
  definition_idx_to_count = get_test_corpus().get_reference_definition_idx_counts_excluding_neg1(word)
  if len(definition_idx_to_count) == 0:
    continue
  print word
  correct = 0
  if best_definition_idx in definition_idx_to_count:
    correct = definition_idx_to_count[best_definition_idx]
  total = sum(definition_idx_to_count.values())
  num_word_instances += total
  num_word_instances_correctly_classified += correct
print num_word_instances
print num_word_instances_correctly_classified


