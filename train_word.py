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

def build_sentence_vector(sentences):
       words_set = set([])
       for s in sentences:
              words = s.split(' ')
              words_set.update(words)
       words_set.discard('')
       words_ls = list(words_set)
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
def get_classifiers_single_word(vec,word = '\xe5\xaf\xba\xe5\xbb\x9f'):
       with open('train_data.json', 'rb') as fp:
              dictionary = json.load(fp)
              dictionary = dict([(k.encode('utf-8'),v) for k,v in dictionary.items()])
       print "LEN",len(dictionary)
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       
       #print dictionary.keys()
       #classifiers = {}
       #for word in dictionary.keys():
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
       words_vec = build_sentence_vector(sentences)
       for s in info:
              #Create observation vector
              observation_vec = build_observation_vector(words_vec,chinese_sents[s[0]]);
              obs.append(observation_vec)
              #obs[len(obs)-1].append(s[1])
              labels.append(s[1])
              print 'len', len(observation_vec)
       #end = len(obs[0])
       #print end
       #print obs
       #x, y = obs[: :48], obs[: 48]
       # x: (observations x attributes) matrix, y: classes (1: setosa, 2: versicolor, 3: virginica)
       linear_svm = mlpy.LibSvm(kernel_type='linear')
       linear_svm.learn(obs, labels)
       print 'pred:', linear_svm.pred([0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
       #print 'x:', obs
       #print 'y:', labels
       return (linear_svm,obs,labels)
def get_classifiers():
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
              words_vec = build_sentence_vector(sentences)
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