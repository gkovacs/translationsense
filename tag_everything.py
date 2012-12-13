#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from corpus_utils import *
import json

def group_by_thousands(l):
  tmpl = []
  output = []
  for i,e in enumerate(l):
    if i % 100 == 0 and len(tmpl) > 0:
      output.append(tmpl)
      tmpl = []
    tmpl.append(e)
  if len(tmpl) > 0:
    output.append(tmpl)
  return output

if __name__ == '__main__':
  all_sentences = get_training_corpus().chinese_sentences + get_test_corpus().chinese_sentences
  sentences_grouped_by_thousands = group_by_thousands(all_sentences)
  #dictionary = {}
  output = []
  for i,sentences in enumerate(sentences_grouped_by_thousands):
    print i, len(sentences_grouped_by_thousands)
    sentences_nowhitespace = [''.join(sentence.split()) for sentence in sentences]
    for tagged_sentence,sentence_nowhitespace in zip(get_pos_tags_in_chinese_sentence_bulk(sentences), sentences_nowhitespace):
      output.append((sentence_nowhitespace, tagged_sentence))
      #dictionary[sentence_nowhitespace] = tagged_sentence
  #json.dump(dictionary, open('tagged_chinese_sentences_nowhitespace_bythousand_utf8.json', 'w'), ensure_ascii=False)
  json.dump(output, open('tagged_chinese_sentences_nowhitespace_byhundred_list_utf8.json', 'w'), ensure_ascii=False)

