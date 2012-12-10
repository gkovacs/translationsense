#!/usr/bin/env python
# -*- coding: utf-8 -*-

from microsofttranslator import Translator
# if this fails, do:
# sudo easy_install microsofttranslator

from ref_definitions2 import read_all_the_files

translator = Translator('finalproj', 'LZTVKNyxQEjmIUbMWp1HhkN4x9XkIbnT6fHhaJfLFmo=')

#print translator.translate('你好'.decode('utf8'), 'en', 'zh-CHT')

(chinese_sentences,english_sentences) = read_all_the_files()
of = open('bing_translations.txt', 'w')
for chinese_sent in chinese_sentences:
  chinese_sent = ''.join([x for x in chinese_sent if x != ' '])
  print >> of, chinese_sent
  print >> of, translator.translate(chinese_sent.decode('utf8'), 'en', 'zh-CHT').encode('utf-8')
  print >> of, '=========='

