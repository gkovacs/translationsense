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

@memoized
def getClassifier(classifierType, word):
  return classifierType(word)

class MaxCountClassifier:
  def __init__(self, word):
    self.most_common_idx = get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word)
    if self.most_common_idx == -1:
      raise Exception("need at least 1 reference definition in training data for word " + word)
  def get_definition_idx(self, sentence):
    return self.most_common_idx

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

@memoized
def get_top_cooccurring_words(word, topn=5):
  cooccurring_word_counts = {}
  for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
    for word in get_words_in_chinese_sentence(sentence):
      if word not in cooccurring_word_counts:
        cooccurring_word_counts[word] = 0
      cooccurring_word_counts[word] += 1
  # for whatever reason normalizing by the total number of occurrences (in order to get rid of really common words) decreases the classification accuracy...
  #counts_and_words = [(count/float(get_training_corpus().get_word_count(word)),word) for word,count in  cooccurring_word_counts.iteritems()]
  counts_and_words = [(count,word) for word,count in  cooccurring_word_counts.iteritems()]
  top_count_words = heapq.nlargest(topn, counts_and_words)
  return [word for count,word in top_count_words]

class OccurrenceClassifier:
  def __init__(self, word):
    self.feature_words = get_top_cooccurring_words(word)
    labels = []
    observations = []
    for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
      features = self.extract_features(sentence)
      most_common_reference_definition = get_training_corpus().get_reference_definition_idx(word, sentence)
      if most_common_reference_definition == -1:
        continue
      labels.append(most_common_reference_definition)
      observations.append(features)
    if len(labels) == 0:
      raise Exception("need at least 1 reference definition in training data for word " + word)
    self.classifier = mlpy.LibSvm(kernel_type='poly')
    self.classifier.learn(observations, labels)
  def extract_features(self, sentence):
    words_in_sentence = set(get_words_in_chinese_sentence(sentence))
    features = []
    for feature_word in self.feature_words:
      if feature_word in words_in_sentence:
        features.append(1)
      else:
        features.append(0)
    return features
  def get_definition_idx(self, sentence):
    features = self.extract_features(sentence)
    return self.classifier.pred(features)

class FractionOccurrenceClassifier:
  def __init__(self, word):
    self.feature_words = get_top_cooccurring_words(word)
    labels = []
    observations = []
    for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
      features = self.extract_features(sentence)
      most_common_reference_definition = get_training_corpus().get_reference_definition_idx(word, sentence)
      if most_common_reference_definition == -1:
        continue
      labels.append(most_common_reference_definition)
      observations.append(features)
    if len(labels) == 0:
      raise Exception("need at least 1 reference definition in training data for word " + word)
    self.classifier = mlpy.LibSvm(kernel_type='poly')
    self.classifier.learn(observations, labels)
  def extract_features(self, sentence):
    sentence_word_counts = {}
    words_in_sentence = get_words_in_chinese_sentence(sentence)
    for word in words_in_sentence:
      if word not in sentence_word_counts:
        sentence_word_counts[word] = 0
      sentence_word_counts[word] += 1
    features = []
    for feature_word in self.feature_words:
      if feature_word in sentence_word_counts:
        features.append(sentence_word_counts[feature_word] / float(len(words_in_sentence)))
      else:
        features.append(0)
    return features
  def get_definition_idx(self, sentence):
    features = self.extract_features(sentence)
    return self.classifier.pred(features)

def main():
  num_word_instances = 0
  num_word_instances_correctly_classified = 0
  for word in get_training_corpus().list_chinese_words():
    print word
    if get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word) == -1: # no reference definitions available for this word in the training data
      continue
    classifier = getClassifier(MaxCountClassifier, word) # can be changed to a different classifier type
    for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
      reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
      if reference_definition_idx == -1: # no reference definition available for this word instance
        continue
      classified_definition_idx = classifier.get_definition_idx(sentence)
      num_word_instances += 1
      if classified_definition_idx == reference_definition_idx:
        num_word_instances_correctly_classified += 1
  print 'Total number of word instances:', num_word_instances
  print 'Number of word instances correctly classified:', num_word_instances_correctly_classified

if __name__ == '__main__':
  main()

