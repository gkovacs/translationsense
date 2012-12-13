#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json

if __name__ == '__main__':
  d = json.load(open('tagged_chinese_sentences.json'))
  tags = []
  for sentence,tagged in d.iteritems():
    for word,tag in tagged:
      tags.append(tag)
  print sorted(list(set(tags)))
