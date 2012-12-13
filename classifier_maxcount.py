from classify_word_utils import *

class MaxCountClassifier:
  def __init__(self, word,fv_size_scale,thresh):
    self.most_common_idx = get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word)
    if self.most_common_idx == -1:
      raise Exception("need at least 1 reference definition in training data for word " + word)
  def get_definition_idx(self, sentence):
    return self.most_common_idx
  def get_feature_words(self,fv_size_scale,thresh):
   	return []
  def get_top_features_by_meaning(self,fv_size_scale,thresh):
  	return {0:['']}
  def get_observation_vectors(self):
    return []
  def get_feature_vector(self):
    return []


