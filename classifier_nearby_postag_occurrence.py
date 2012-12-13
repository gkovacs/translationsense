from classify_word_utils import *

alltags = ['AD', 'AS', 'BA', 'CC', 'CD', 'CS', 'DEC', 'DEG', 'DER', 'DEV', 'DT', 'ETC', 'FW', 'IJ', 'JJ', 'LB', 'LC', 'M', 'MSP', 'NN', 'NR', 'NT', 'OD', 'ON', 'P', 'PN', 'P', 'SB', 'SP', 'URL', 'VA', 'VC', 'VE', 'VV']
tag_to_idx = {}
for idx,tag in enumerate(alltags):
  tag_to_idx[tag] = idx

def pos_to_feature_vector(postag):
  features = [0]*len(alltags)
  features[tag_to_idx[postag]] = 1
  return features

class NearbyPOSTagOccurrenceClassifier:
  def __init__(self, word, fv_size_scale, thresh):
    self.num_definitions_available = len(list_definitions_for_word(word))
    self.word = word
    labels = []
    observations = []
    for sentence_idx in sorted(list(get_training_corpus().sentence_idxes_word_occurs_in(word))):
      sentence = get_training_corpus().get_sentence_at_idx(sentence_idx)
      most_common_reference_definition = get_training_corpus().get_reference_definition_idx(word, sentence)
      if most_common_reference_definition == -1:
        continue
      features = self.extract_features(sentence)
      labels.append(most_common_reference_definition)
      observations.append(features)
    if len(labels) == 0 or len(observations) == 0:
      raise Exception("need at least 1 reference definition in training data for word " + word)
    self.classifier = mlpy.LibSvm(kernel_type='poly')
    self.classifier.learn(observations, labels)
  def extract_features(self, sentence):
    features = [0]*len(alltags)
    wordidx = 0
    idx = 0
    for curword,curtag in get_pos_tags_in_chinese_sentence(sentence):
      if curword == self.word:
        wordidx = idx
      idx += 1
    surrounding_words_and_tags = get_pos_tags_in_chinese_sentence(sentence)[wordidx-1:wordidx+2]
    for curword,curtag in surrounding_words_and_tags:
      features[tag_to_idx[curtag]] = 1
    return features
  def get_definition_idx(self, sentence):
    features = self.extract_features(sentence)
    if not features:
      print sentence
      exit(0)
    prediction = self.classifier.pred(features)
    prediction = int(round(prediction))
    if prediction >= self.num_definitions_available:
      prediction = self.num_definitions_available - 1
    if prediction < 0:
      prediction = 0
    return prediction

