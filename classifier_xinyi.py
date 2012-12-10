from classify_word_utils import *

class XinyiClassifier:
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

