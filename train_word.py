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
def main(args):
       with open('data.json', 'rb') as fp:
              dictionary = json.load(fp)
              dictionary = dict([(k.encode('utf-8'),v) for k,v in dictionary.items()])
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       
       print dictionary.keys()
       #for word in dictionary:
       word = '\xe5\x8f\x83\xe5\x8a\xa0'
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
       print 'pred:', linear_svm.pred([0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
       print 'x:', obs
       print 'y:', labels


if __name__ == '__main__':
    main(sys.argv)


       # [ 5.7,  2.8,  4.1,  1.3,  2. ],
       # [ 6.3,  3.3,  6. ,  2.5,  3. ],
       # [ 5.8,  2.7,  5.1,  1.9,  3. ],
       # [ 7.1,  3. ,  5.9,  2.1,  3. ],
       # [ 6.3,  2.9,  5.6,  1.8,  3. ],
       # [ 6.5,  3. ,  5.8,  2.2,  3. ],
       # [ 7.6,  3. ,  6.6,  2.1,  3. ],
       # [ 4.9,  2.5,  4.5,  1.7,  3. ],
       # [ 7.3,  2.9,  6.3,  1.8,  3. ],
       # [ 6.7,  2.5,  5.8,  1.8,  3. ],
       # [ 7.2,  3.6,  6.1,  2.5,  3. ],
       # [ 6.5,  3.2,  5.1,  2. ,  3. ],
       # [ 6.4,  2.7,  5.3,  1.9,  3. ],
       # [ 6.8,  3. ,  5.5,  2.1,  3. ],
       # [ 5.7,  2.5,  5. ,  2. ,  3. ],
       # [ 5.8,  2.8,  5.1,  2.4,  3. ],
       # [ 6.4,  3.2,  5.3,  2.3,  3. ],
       # [ 6.5,  3. ,  5.5,  1.8,  3. ],
       # [ 7.7,  3.8,  6.7,  2.2,  3. ],
       # [ 7.7,  2.6,  6.9,  2.3,  3. ],
       # [ 6. ,  2.2,  5. ,  1.5,  3. ],
       # [ 6.9,  3.2,  5.7,  2.3,  3. ],
       # [ 5.6,  2.8,  4.9,  2. ,  3. ],
       # [ 7.7,  2.8,  6.7,  2. ,  3. ],
       # [ 6.3,  2.7,  4.9,  1.8,  3. ],
       # [ 6.7,  3.3,  5.7,  2.1,  3. ],
       # [ 7.2,  3.2,  6. ,  1.8,  3. ],
       # [ 6.2,  2.8,  4.8,  1.8,  3. ],
       # [ 6.1,  3. ,  4.9,  1.8,  3. ],
       # [ 6.4,  2.8,  5.6,  2.1,  3. ],
       # [ 7.2,  3. ,  5.8,  1.6,  3. ],
       # [ 7.4,  2.8,  6.1,  1.9,  3. ],
       # [ 7.9,  3.8,  6.4,  2. ,  3. ],
       # [ 6.4,  2.8,  5.6,  2.2,  3. ],
       # [ 6.3,  2.8,  5.1,  1.5,  3. ],
       # [ 6.1,  2.6,  5.6,  1.4,  3. ],
       # [ 7.7,  3. ,  6.1,  2.3,  3. ],
       # [ 6.3,  3.4,  5.6,  2.4,  3. ],
       # [ 6.4,  3.1,  5.5,  1.8,  3. ],
       # [ 6. ,  3. ,  4.8,  1.8,  3. ],
       # [ 6.9,  3.1,  5.4,  2.1,  3. ],
       # [ 6.7,  3.1,  5.6,  2.4,  3. ],
       # [ 6.9,  3.1,  5.1,  2.3,  3. ],
       # [ 5.8,  2.7,  5.1,  1.9,  3. ],
       # [ 6.8,  3.2,  5.9,  2.3,  3. ],
       # [ 6.7,  3.3,  5.7,  2.5,  3. ],
       # [ 6.7,  3. ,  5.2,  2.3,  3. ],
       # [ 6.3,  2.5,  5. ,  1.9,  3. ],
       # [ 6.5,  3. ,  5.2,  2. ,  3. ],
       # [ 6.2,  3.4,  5.4,  2.3,  3. ],
       # [ 5.9,  3. ,  5.1,  1.8,  3. ]])