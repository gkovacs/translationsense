from classify_word_utils import *

class MaxCountClassifier:
  def __init__(self, word):
    self.most_common_idx = get_training_corpus().get_most_common_reference_definition_idx_excluding_neg1(word)
    if self.most_common_idx == -1:
      raise Exception("need at least 1 reference definition in training data for word " + word)
  def get_definition_idx(self, sentence):
    return self.most_common_idx

