import train_word as train
import ref_definitions2 as ref
import json

with open('chinese_sents.json', 'rb') as fp:
      chinese_sents = json.load(fp)
def get_linear_svms():
    return train.get_classifiers()
def get_c_words():
    with open('train_data.json', 'rb') as fp:
        train_dict = json.load(fp)
        train_dict = dict([(k.encode('utf-8'),v) for k,v in train_dict.items()])
    classifiable_words = train_dict.keys()
    return classifiable_words
def get_test_words(read_start, read_end):
    with open('train_data.json', 'rb') as fp:
        train_dict = json.load(fp)
        train_dict = dict([(k.encode('utf-8'),v) for k,v in train_dict.items()])
    classifiable_words = train_dict.keys()

    test_words = {}
    for i in range(read_start, read_end):
        c_sent = chinese_sents[i]
        c_sent_words = c_sent.split(' ')
        c_sent_words = list(set(c_sent_words))
        for c_word in c_sent_words:
            #check if word can be classified
            utf = c_word.encode('utf-8')
            if (utf in classifiable_words):
                if utf in test_words.keys():
                    test_words[utf].append(i)
                else:
                    test_words[utf] = [i]
    return test_words
def build_sentence_vector(sentences):
       words_set = set([])
       for s in sentences:
              words = s.split(' ')
              words_set.update(words)
       words_set.discard('')
       words_ls = list(words_set)
       return words_ls
def build_observation_vector(words_vec,sentence):
       vector = []
       for word in words_vec:
              if word in sentence:
                     vector.append(1)
              else:
                     vector.append(0)
       return vector
def classify_test_words():
    classifiers = train.get_classifiers()
    test_words = get_test_words(3500,5000)
    classified_words = {}
    for word in test_words:
        #print "WORD", word
        for sent_i in test_words[word]:
            classifier = classifiers[word][0]
            feature_vec = classifiers[word][1]
            sent_vec = build_sentence_vector([chinese_sents[sent_i]])
            test_feature_vec = build_observation_vector(feature_vec,sent_vec)
            # print "feature_vec", feature_vec
            # print "sent_vec", sent_vec
            # print "obs_vec", test_feature_vec
            pred = classifier.pred(test_feature_vec)
            if(word in classified_words):
                classified_words[word].append([sent_i,pred])
            else:
                classified_words[word] = [[sent_i,pred]]
    #print "classified words", classified_words
    return classified_words
def get_ref():
    with open('test_ref_dict.json', 'rb') as fp:
        ref_dict = json.load(fp)
        ref_dict = dict([(k.encode('utf-8'),v) for k,v in ref_dict.items()])
    return ref_dict
def evaluate():
    #ref_dict is build_chinese_word_sent_dict(3500,5000,{})
    with open('test_ref_dict.json', 'rb') as fp:
        ref_dict = json.load(fp)
        ref_dict = dict([(k.encode('utf-8'),v) for k,v in ref_dict.items()])
    correct_pred_count = 0
    correct_predictions = {}
    pred_count = 0
    classified_words = classify_test_words()
    for word in classified_words:
        for test_pred in classified_words[word]:
            sent_i = test_pred[0]
            prediction = test_pred[1]
            if (word in ref_dict):
                ref_meanings = ref_dict[word]
                for meaning in ref_meanings:
                    if meaning[0] == sent_i:
                        if meaning[1] == prediction:
                            correct_pred_count += 1
                            correct_predictions[word] = classified_words[word]
                        pred_count += 1
                    
    print "total # of correct predictions: %s" % correct_pred_count
    print "total # of prediction attempts: %s" % pred_count


