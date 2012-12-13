#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from corpus_utils import *
import json

if __name__ == '__main__':
  all_sentences = get_training_corpus().chinese_sentences + get_test_corpus().chinese_sentences
  for x in all_sentences:
    print x


