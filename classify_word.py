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
  # feature_vector_pare_down_size = 100
  # freq_threshold = 0.3
  # number_of_stop_words = 50
  # non_maj_thresh = 0.3
  # ref_data_req = 50

  #baseline
  # feature_vector_pare_down_size = 10000
  # freq_threshold = 0.0
  # number_of_stop_words = 0
  # non_maj_thresh = 0.0
  # ref_data_req = 1 


  # fv_values = [30, 50, 100, 500, 1000] 
  # f_values = [0.01, 0.1, 0.3, 0.5]
  # sw_values = [10, 50, 100, 200]
  # nm_values = [0.1, 0.3]
  # rd_values = [10, 50, 100]

  #best values from round 1 testing:
  #fv =  100 < 500 > 1000
  #f =  < 0.5
  #sw = 10 < 50 < 100
  #nm = < 0.3
  #rd = 500

  #baseline new params
  feature_vector_scale_size = 1
  freq_threshold = 0.0
  number_of_stop_words = 0
  non_maj_thresh = 0.0
  ref_data_req = 1 
  fv_values = [2,3,4,5,6] 
  f_values = [0.0]
  sw_values = [10, 50, 100, 200]
  nm_values = [0.2,0.4,0.45,0.5]
  rd_values = [10,20,40,60,100]

  #f_value of 1.0 beats the max_classifier

  #c = OccurrenceClassifier
  m_thresh = [3,4,5] 
  words = ['研究所']
  classifiers = [MaxCountClassifier, OccurrenceClassifier]
<<<<<<< HEAD
  # for m in m_thesh:
  #   for c in classifiers:
  #     print "CLASSIFIER:", c
  #     run_test_single_word('研究所',c,m,0.0,100,0.0,1)

  ratio = [0.33,0.36,0.4,0.43]
=======
  for c in classifiers:
     print "CLASSIFIER:", c
     run_test_single_word('研究所',c,1,0.0,100,0.0,1)
  '''
  ratio = [1,2,3]
>>>>>>> 2edad54d8da447c9a6137a8a9ec4d6c72ebae88f
  for r in ratio:
  #   print "MAJ THRESH" , r
    for c in classifiers:
<<<<<<< HEAD
    #     print "CLASSIFIER:", c
      run_test(c,4.3,0,50,0.4,10)
=======
      print "CLASSIFIER:", c
      run_test(c,r,0,50,0.35,10)
  '''
>>>>>>> 2edad54d8da447c9a6137a8a9ec4d6c72ebae88f
  # print "-----------------------------------------------------"
  #   run_test(c,feature_vector_scale_size,
  #     freq_threshold,
  #     number_of_stop_words,
  #     non_maj_thresh,
  #     ref_data_req)

  #   print " ********************** FV to obs ratio"
  #   for fv in fv_values:
  #     run_test(c,fv,
  #       freq_threshold,
  #       number_of_stop_words,
  #       non_maj_thresh,
  #       ref_data_req)
    
  #   print " ********************** Stop Words"
  #   for sw in sw_values:
  #     run_test(c,feature_vector_scale_size,
  #       freq_threshold,
  #       sw,
  #       non_maj_thresh,
  #       ref_data_req)
    
  #   print " ********************** Non Maj"
  #   for nm in nm_values:
  #     run_test(c,feature_vector_scale_size,
  #       freq_threshold,
  #       number_of_stop_words,
  #       nm,
  #       ref_data_req)

  #   print " ********************** Ref Data"
  #   for rd in rd_values:
  #     run_test(c,feature_vector_scale_size,
  #       freq_threshold,
  #       number_of_stop_words,
  #       non_maj_thresh,
  #       rd)
def run_test_single_word(word, classifier, fv_size_scale,thresh,num_stop,non_maj_thresh,ref_data_req):
  # arg 1: classifier name
  top_word_freq =  get_training_corpus().get_top_words(num_stop)
  top_word_list = [word for f,word in top_word_freq]

  classifierType = classifier
  print classifierType
  print "feature vector size %s" % fv_size_scale
  print "freq thresh %s" % thresh
  print "number of stop words to eliminate %s" % num_stop
  print "none majority threshold %s" % non_maj_thresh
  print "required number of observations in training %s" % ref_data_req
  num_word_instances = 0
  skipped_words = 0
  num_word_instances_correctly_classified = 0
  # if not word_has_enough_reference_definitions(word,ref_data_req):
  #   skipped_words += 1
  #   continue
  # if not word_has_enough_nonmajority_definitions(word,non_maj_thresh):
  #   skipped_words += 1
  #   continue
  # if word in top_word_list:
  #   skipped_words += 1
  #   continue
  word = '研究所'
  print word
  for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
    sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
    reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
    if reference_definition_idx == -1: # no reference definition available for this word instance
      continue
    classifier = getClassifier(classifierType, word,fv_size_scale,thresh) # can be changed to a different classifier type
    classified_definition_idx = classifier.get_definition_idx(sentence)
    #print classified_definition_idx, reference_definition_idx
    num_word_instances += 1
    print "pred:",classified_definition_idx
    print "ref:", reference_definition_idx
    if classified_definition_idx == reference_definition_idx:
      num_word_instances_correctly_classified += 1
    #else:
      # print 'correct:', list_definitions_for_word(word)[reference_definition_idx]
      # print 'incorrect:', list_definitions_for_word(word)[classified_definition_idx]
      # print 'sentence:', sentence
      # print 'translation:', get_test_corpus().get_english_sentence_for_chinese(sentence)
      # print ''
  default_features = classifier.get_feature_vector()
  meaning_segregated_features = classifier.get_top_features_by_meaning(fv_size_scale,thresh)
  # print 'feature_vector', default_features
  # print 'feature vector len', len(default_features)
  # print 'observations', classifier.get_observation_vectors()
  # print 'features segregated by meaning', meaning_segregated_features
  # for meaning in meaning_segregated_features.keys():
  #   print "MEANING:", meaning
  #   target = meaning_segregated_features[meaning]
  #   rest = []
  #   for other_meaning in meaning_segregated_features.keys():
  #     if other_meaning != meaning:
  #       rest += meaning_segregated_features[other_meaning]
  #   unique = set(target) - set(rest)
  #   print "UNIQUE", unique
  #   print "SIZE OF UNIQUE", len(unique) 


  # combination_features = []
  # for f in meaning_segregated_features.values():
  #   combination_features += f
  # print 'features combination_features', len(combination_features)
  # missing_features_in_default = list(set(default_features) - set(combination_features))
  # print 'missing features in default', missing_features_in_default
  # print 'number of missing in default', len(missing_features_in_default)
  print 'Num observations', classifier.get_num_observations()
  print 'Number of skipped words:', skipped_words
  print 'Total number of word instances:', num_word_instances
  print 'Number of word instances correctly classified:', num_word_instances_correctly_classified
  print "accuracy: %s" % (num_word_instances_correctly_classified / float(num_word_instances))
def run_test(classifier, fv_size_scale,thresh,num_stop,non_maj_thresh,ref_data_req):
  # arg 1: classifier name
  top_word_freq =  get_training_corpus().get_top_words(num_stop)
  top_word_list = [word for f,word in top_word_freq]

  classifierType = classifier
  print classifierType
  print "feature vector size %s" % fv_size_scale
  print "freq thresh %s" % thresh
  print "number of stop words to eliminate %s" % num_stop
  print "none majority threshold %s" % non_maj_thresh
  print "required number of observations in training %s" % ref_data_req
  num_word_instances = 0
  skipped_words = 0
  num_word_instances_correctly_classified = 0
  for word in get_training_corpus().list_chinese_words():
    if not word_has_enough_reference_definitions(word,ref_data_req):
      skipped_words += 1
      continue
    if not word_has_enough_nonmajority_definitions(word,non_maj_thresh):
      skipped_words += 1
      continue
    if word in top_word_list:
      skipped_words += 1
      continue
    #print word
    for sentence_idx in sorted(list(get_test_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_test_corpus().get_sentence_at_idx(sentence_idx)
      reference_definition_idx = get_test_corpus().get_reference_definition_idx(word, sentence)
      if reference_definition_idx == -1: # no reference definition available for this word instance
        continue
      classifier = getClassifier(classifierType, word,fv_size_scale,thresh) # can be changed to a different classifier type
      classified_definition_idx = classifier.get_definition_idx(sentence)
      #print classified_definition_idx, reference_definition_idx
      num_word_instances += 1
      if classified_definition_idx == reference_definition_idx:
        num_word_instances_correctly_classified += 1
      #else:
        #print word
        #print 'correct:', list_definitions_for_word(word)[reference_definition_idx]
        #print 'incorrect:', list_definitions_for_word(word)[classified_definition_idx]
        #print 'sentence:', sentence
        #print 'translation:', get_test_corpus().get_english_sentence_for_chinese(sentence)
        #print ''
  print 'Number of skipped words:', skipped_words
  print 'Total number of word instances:', num_word_instances
  print 'Number of word instances correctly classified:', num_word_instances_correctly_classified
  print "accuracy: %s" % (num_word_instances_correctly_classified / float(num_word_instances))

if __name__ == '__main__':
  main(sys.argv)

