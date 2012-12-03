import sys, string, re
import ref_definitions2
import numpy as np
import mlpy
import matplotlib.pyplot as plt 

# Input: Training data (sentences) corresponding to a chinese word
# Returns:
# 1) The trained linear svm associated with the word
# 2) The feature vector used to train the svm 

def build_sentence_vector(sentences):
	words_set = set([])
	for s in sentences:
		words = s.split(' ')
		words_set.update(words)
	words_set.discard('')
	words_ls = []
	words_ls.addAll(words_set)
	return words_ls

#Builds simplest feature vector - presence/absence of a word in the sentence.
def build_observation_vector(words_vec,sentence):
	vector = []
	for word in words_vec:
		if word in sentence:
			vector.append(1)
		else:
			vector.append(0)
	return vector
def main(args):
	dictionary = ref_definitions2.main()
	(chinese_sents,english_sents) =  read_all_the_files()

	#xs, ys
	observations = []
	labels = []

	for word in dictionary:
		#Collect all sentences containing this word into a feature vector
		info = dictionary[word]
		sentences = []
		for s in info:
			sentences.append(chinese_sents[s[0]])
		words_vec = build_sentence_vector(sentences)
		for s in info:
			#Create observation vector
			observation_vec = build_observation_vector(words_vec,chinese_sents[s[0]]);
			observations.append(observation_vec)
			labels.append(s[1])
	


if __name__ == '__main__':
    main(sys.argv)


