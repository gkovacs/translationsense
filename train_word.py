import sys, string, re
import ref_definitions2
import numpy as np
import mlpy
import matplotlib.pyplot as plt 
import json
# Input: Training data (sentences) corresponding to a chinese word
# Returns:
# 1) The trained linear svm associated with the word
# 2) The feature vector used to train the svm
def build_occurence_dict(read_start,read_end):
       occurence_dict = {}
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       for i in range(read_start, read_end):
              c_sent = chinese_sents[i]
              c_sent_words = c_sent.split(' ')
              for c_word in c_sent_words:
                     if(c_word in occurence_dict):
                            occurence_dict[c_word] += 1
                     else:
                            occurence_dict[c_word] = 1
       with open('occurence_data.json', 'wb') as fp:
              json.dump(occurence_dict,fp)
       return occurence_dict

def get_total_cooccurence(word,sentences):
       #print "WORD", word
       #print "sentences", sentences
       words = []
       for s in sentences:
              sent_words = s.split(' ')
              sent_words.remove('')
              words = words + sent_words
       cooccurence_data = {}
       for w in words:
              #print "w", w
              #print "word", word
              if w != word:
                     if w in cooccurence_data:
                            cooccurence_data[w] += 1
                     else:
                            cooccurence_data[w] = 1
       return cooccurence_data
def get_important_features(word,sentences):
       cooccurence_data = get_total_cooccurence(word,sentences)
       with open('occurence_data.json', 'rb') as fp:
              occurence_data = json.load(fp)
       features = {}
       for word in cooccurence_data:
              #print "cooccur", cooccurence_data[word]
              #print "all", occurence_data[word]
              features[word] = float(cooccurence_data[word])/occurence_data[word]
              #print "value", features[word]
       return features
def get_top_features(thresh,word,sentences):
       features = get_important_features(word,sentences)
       sorted_features = sorted(features, key=features.get)
       sorted_features.reverse()

       # stop_pos = 0
       # for i in range(len(sorted_features)):
       #        f = sorted_features[i]
       #        if(features[f] < thresh):
       #               stop_pos = i
       #               break
       # n = max(10,stop_pos)
       n = thresh
       if(n > len(features)):
              n = len(features)

       #print "features", features
       #print "sorted", sorted_features[len(features)-n:len(features)]
       #print "edge value:", features[sorted_features[n-1]]
       #print "N", n
       return sorted_features[:n]
# def build_sentence_vector(word,sentences):
#        words_set = set([])
#        for s in sentences:
#               words = s.split(' ')
#               words_set.update(words)
#        words_set.discard('')
#        words_ls = list(words_set)
#        return words_ls

#Builds simplest feature vector - presence/absence of a word in the sentence.
def build_observation_vector(words_vec,sentence):
       vector = []
       for word in words_vec:
              if word in sentence:
                     vector.append(1)
              else:
                     vector.append(0)
       return vector
def get_classifiers(n):
       with open('train_data.json', 'rb') as fp:
              dictionary = json.load(fp)
              dictionary = dict([(k.encode('utf-8'),v) for k,v in dictionary.items()])
       print "LEN",len(dictionary)
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       
       #print dictionary.keys()
       classifiers = {}
       for word in dictionary.keys():
              #print "word", word
       #word = '\xe5\x8f\x83\xe5\x8a\xa0'
       #xs, y is last element
              obs = []
              labels = []
              #Collect all sentences containing this word into a feature vector
              info = dictionary[word]
              sentences = []
              for s in info:
                     sentences.append(chinese_sents[s[0]])
              words_vec = get_top_features(n,word,sentences)
              for s in info:
                     #Create observation vector
                     observation_vec = build_observation_vector(words_vec,chinese_sents[s[0]]);
                     obs.append(observation_vec)
                     #obs[len(obs)-1].append(s[1])
                     labels.append(s[1])
       #end = len(obs[0])
       #print end
       #print obs
       #x, y = obs[: :48], obs[: 48]
       # x: (observations x attributes) matrix, y: classes (1: setosa, 2: versicolor, 3: virginica)
              linear_svm = mlpy.LibSvm(kernel_type='linear')
              linear_svm.learn(obs, labels)
              classifiers[word] = (linear_svm,words_vec)
       #print 'pred:', linear_svm.pred([0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
       #print 'x:', obs
       #print 'y:', labels
       return classifiers

if __name__ == '__main__':
    main(sys.argv)