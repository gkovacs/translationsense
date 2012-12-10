import sys, string, re
import ref_definitions2
import numpy as np
import mlpy
import ref_definitions2 as ref
import matplotlib.pyplot as plt 
import json
reload(sys)
sys.setdefaultencoding("utf-8")



'''
Build commonly used files:
num_test = the number of training sentences to use
num_training = the number of test senteces to use
n = number of alignment files we are using
'''
def build_all_the_files(num_training,num_test,n):
       chinese_sents,english_sents = ref.read_all_the_files(n)
       with open('chinese_sents.json', 'wb') as fp:
              json.dump(chinese_sents,fp)
       build_occurence_dict(0,num_training)
       test_ref = ref.build_chinese_word_sent_dict(num_training, num_test+num_training,{},n)
       with open('test_ref_dict.json', 'wb') as fp:
              json.dump(test_ref,fp)
       train_data = ref.build_chinese_word_sent_dict(0,num_training,{},n)
       with open('train_data.json', 'wb') as fp:
              json.dump(train_data,fp)
       build_cooccurrence_dict()
'''
Build a dictionary. k => word, v => total # of occurences among the sentences spanned by read_start, read_end
'''
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
              json.dump(occurence_dict,fp,)
       return occurence_dict
'''
Called by build_all_the_files, builds dictionary, k => k_word, v => dictionary of words w that cooccur with the k_word in all the sentences containing the k_word in the test_corpus. The words in the dictionary are restricted to the intersection of words we have reference definitions for in the training and test data sets. 
'''
def build_cooccurrence_dict():
       with open('train_data.json', 'rb') as fp:
              dictionary = json.load(fp)
              dictionary = dict([(k.encode('utf-8'),v) for k,v in dictionary.items()])
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       with open('test_ref_dict.json', 'rb') as fp:
              ref_dict = json.load(fp)
              ref_dict = dict([(k.encode('utf-8'),v) for k,v in ref_dict.items()])
       words_train = dictionary.keys()
       words_ref = ref_dict.keys()
       can_eval_words = list(set(words_train) & set(words_ref))

       d = {}
       for word in can_eval_words:
              sentences = []
              info = dictionary[word]
              for s in info:
                     sentences.append(chinese_sents[s[0]])
              d[word] = get_total_cooccurence(word,sentences)
       with open('cooccurence_data.json', 'wb') as fp:
              json.dump(d,fp,ensure_ascii = False,encoding = 'utf-8')
'''
Called by build_cooccurrence_dict.
Given a t_word and a list of sentences containing the t_word , returns a dictionary of cooccuring words mapped to the number of the coocurrences with t_word 

'''
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
'''
Called by get_top_features.
Given cooccurence data and t_word, returns the list of features (cooccuring words) sorted in order of importance (# of cooccurences/total # of occurences -in training)
'''
def get_important_features(word,cooccur_data):
       #cooccurence_data = get_total_cooccurence(word,sentences)
       with open('occurence_data.json', 'rb') as fp:
              occurence_data = json.load(fp)
       features = {}
       for w in cooccur_data:
              #print "cooccur", cooccurence_data[word]
              #print "all", occurence_data[word]
              features[w] = float(cooccur_data[w])/occurence_data[w]
              #print "value", features[word]
       return features
'''
Gets the features with importance value over thresh.
'''
def get_top_features(thresh,word,cooccur_data):
       features = get_important_features(word,cooccur_data)
       sorted_features = sorted(features, key=features.get)
       sorted_features.reverse()

       stop_pos = 0
       for i in range(len(sorted_features)):
              f = sorted_features[i]
              if(features[f] < thresh):
                     stop_pos = i
                     break
       n = max(10,stop_pos)
       #n = thresh
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
'''
Given the feature vector and the input observed sentence, builds the feature vector for the sentence.
'''
def build_observation_vector(words_vec,sentence):
       vector = []
       for word in words_vec:
              if word in sentence:
                     vector.append(1)
              else:
                     vector.append(0)
       return vector
'''
Returns the classifiers for evaluable words(intersection of training and test words which we have reference definitions for). The result is dictionary k => t_word, v => (the classifier, the feature vector used)
'''
def get_classifiers(n):
       with open('train_data.json', 'rb') as fp:
              dictionary = json.load(fp)
              dictionary = dict([(k.encode('utf-8'),v) for k,v in dictionary.items()])
       print "LEN",len(dictionary)
       with open('chinese_sents.json', 'rb') as fp:
              chinese_sents = json.load(fp)
       with open('test_ref_dict.json', 'rb') as fp:
              ref_dict = json.load(fp)
              ref_dict = dict([(k.encode('utf-8'),v) for k,v in ref_dict.items()])
       with open('cooccurence_data.json', 'rb') as fp:
              cooccur_data = json.load(fp)
              cooccur_data = dict([(k.encode('utf-8'),v) for k,v in cooccur_data.items()])
       #print dictionary.keys()
       classifiers = {}
       words_train = dictionary.keys()
       words_ref = ref_dict.keys()
       can_eval_words = list(set(words_train) & set(words_ref))
       for word in can_eval_words:
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
              words_vec = get_top_features(n,word,cooccur_data[word])
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