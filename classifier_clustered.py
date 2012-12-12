from classify_word_utils import *

@memoized
def word_similarity(word1, word2):
  both_occurred = get_training_corpus().sentence_idxes_both_words_occur_in(word1, word2)
  either_occurred = get_training_corpus().sentence_idxes_either_word_occurs_in(word1, word2)
  return len(both_occurred) / len(either_occurred)

class ClusteredOccurrenceClassifier:
  def __init__(self, word):
    self.feature_words = get_top_cooccurring_words(word, 5, 0.3)
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
    if len(labels) == 0:
      raise Exception("need at least 1 reference definition in training data for word " + word)
    self.classifier = mlpy.LibSvm(kernel_type='poly')
    self.classifier.learn(observations, labels)
  def extract_features(self, sentence):
    features = []
    words_in_sentence = uniquify(get_words_in_chinese_sentence(sentence))
    for feature_word in self.feature_words:
      similarity_score_sum = sum([word_similarity(word, feature_word) for word in words_in_sentence])
      feature_score = similarity_score_sum / len(words_in_sentence)
      features.append(feature_score)
    return features
  def get_definition_idx(self, sentence):
    features = self.extract_features(sentence)
    prediction = self.classifier.pred(features)
    prediction = int(round(prediction))
    if prediction >= self.num_definitions_available:
      prediction = self.num_definitions_available - 1
    if prediction < 0:
      prediction = 0
    return prediction

if __name__ == '__main__':
  pass
