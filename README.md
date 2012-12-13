### About

This is our 6.864 Final Project code. It performs translation-sense disambiguation for Chinese-English translation - that is, you can give it a Chinese sentence, ask a particular word you want the translation for, and it'll use the surrounding context to infer the correct translation. The reference translations are from the CC-CEDICT file, which you can observe in the file cedict_full.txt

### Team Members
Geza Kovacs
Joy Chen
Xinyi Zhang

### Prerequisites
Chinese-English News Parallel Corpus, which you can obtain from the LDC.

Chinese_seg should contain the segmented Chinese (segmented by Stanford Word Segmenter) .sgm files, English should contain the English .sgm files, alignment should contain the alignment .sgm files. All should be converted to utf-8 encoding beforehand.

### Usage

classifier\_*.py are the various translation-sense classifiers we implemented. classifier\_list.py provides an abstraction layer over these - a call to getClassifier(classifierType, word) will give you a classifier for the Chinese word you provide.

Once you have a Classifier instance, the get\_definition\_idx(sentence) method will then allow you to get the best definition index in the context of the Chinese sentence (which should be pre-segmented, ie words delimited by spaces). To see what the definition text itself is, you can use the function list\_definitions\_for\_word from the file reference\_definitions.py




