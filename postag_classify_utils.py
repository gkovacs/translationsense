#!/usr/bin/env python

def pos_to_feature_vector(postag):
  features = [0]*len(alltags)
  features[tag_to_idx[postag]] = 1
  return featuresalltags = ['AD', 'AS', 'BA', 'CC', 'CD', 'CS', 'DEC', 'DEG', 'DER', 'DEV', 'DT', 'ETC', 'FW', 'IJ', 'JJ', 'LB', 'LC', 'M', 'MSP', 'NN', 'NR', 'NT', 'OD', 'ON', 'P', 'PN', 'P', 'SB', 'SP', 'URL', 'VA', 'VC', 'VE', 'VV']
tag_to_idx = {}
for idx,tag in enumerate(alltags):
  tag_to_idx[tag] = idx

def pos_to_feature_vector(postag):
  features = [0]*len(alltags)
  if postag in tag_to_idx:
    features[tag_to_idx[postag]] = 1
  return features

