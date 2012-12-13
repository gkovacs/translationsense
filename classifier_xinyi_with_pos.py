from classify_word_utils import *
from corpus_utils import *

from postag_classify_utils import *

class XinyiWithPOSClassifier:
  def __init__(self, word,fv_size_scale, thresh):
    self.word = word
    self.observations = self.get_num_observations()
    print "NUM OBS:", self.observations
    self.feature_words = self.get_feature_words((int)(round(self.observations*fv_size_scale)),thresh)
    self.num_definitions_available = len(list_definitions_for_word(word))
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
    self.observations = observations
    if len(labels) == 0:
      raise Exception("need at least 1 reference definition in training data for word " + word)
    self.classifier = mlpy.LibSvm(kernel_type='linear')
    self.classifier.learn(observations, labels)
  def get_num_observations(self):
    observations = 0
    for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(self.word))):
      sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
      most_common_reference_definition = get_training_corpus().get_reference_definition_idx(self.word, sentence)
      if most_common_reference_definition == -1:
        continue
      observations += 1
    return observations
  def get_feature_words(self,fv_size_scale,thresh):
    meaning_segregated_features = self.get_top_features_by_meaning(fv_size_scale,thresh)
    unique_features = []
    for meaning in meaning_segregated_features.keys():
      #print "MEANING:", meaning
      target = meaning_segregated_features[meaning]
      rest = []
      for other_meaning in meaning_segregated_features.keys():
        if other_meaning != meaning:
          rest += meaning_segregated_features[other_meaning]
      unique = set(target) - set(rest)
      unique_features += unique
    return unique_features
    #print "LENGTH OF COMBINED", len(meaning_segregated_features)
    # combination_features = []
    # for f in meaning_segregated_features.values():
    #   combination_features += f
    # return combination_features
  def get_top_features_by_meaning(self,fv_size_scale,thresh):
    meaning_sentence_dict = {}
    meanings = 0
    for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(self.word))):
      sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
      most_common_reference_definition = get_training_corpus().get_reference_definition_idx(self.word, sentence)
      if most_common_reference_definition == -1:
        continue
      if most_common_reference_definition in meaning_sentence_dict:
        meaning_sentence_dict[most_common_reference_definition] += sentence
      else:
        meanings += 1
        meaning_sentence_dict[most_common_reference_definition] = sentence
    #print "sentence_dict", meaning_sentence_dict
    meaning_top_features_dict = {}
    length = 0
    for meaning in meaning_sentence_dict.keys():
      sentences = meaning_sentence_dict[meaning]
      meaning_top_features_dict[meaning] = get_top_cooccurring_words_for_meaning(self.word,sentences,fv_size_scale,thresh)
      #print "meaning", meaning
      #print "features", meaning_top_features_dict[meaning]
      length += len(meaning_top_features_dict[meaning])
    #print "LENGTH TOTAL", length
    return meaning_top_features_dict
  def extract_features(self, sentence):
    words_in_sentence = set(get_words_in_chinese_sentence(sentence))
    features = [0]*len(self.feature_words)
    for i in range(len(self.feature_words)):
      feature_word = self.feature_words[i]
      if feature_word in words_in_sentence:
        features[i] = 1
      else:
        features[i] = 0
    return features
  def get_pos_tag(self, sentence):
    tag = None
    for curword,curtag in get_pos_tags_in_chinese_sentence(sentence):
      if curword == self.word:
        tag = curtag
        break
    return tag
  def get_observation_vectors(self):
    return self.observations
  def get_feature_vector(self):
    return self.feature_words
  def get_definition_idx(self, sentence):
    features = self.extract_features(sentence)
    print "features",features
    prediction = self.classifier.pred(features)
    prediction = int(round(prediction))
    if prediction >= self.num_definitions_available:
      prediction = self.num_definitions_available - 1
    if prediction < 0:
      prediction = 0
    return prediction

