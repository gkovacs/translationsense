from classifier_maxcount import *
from classifier_occurrence import *
from classifier_fraction import *
from classifier_clustered import *
from classifier_xinyi import *

@memoized
def getClassifier(classifierType, word):
  return classifierType(word)

def getClassifierByName(name):
  name = name.lower()
  if 'max' in name:
    return MaxCountClassifier
  elif 'fraction' in name:
    return FractionOccurrenceClassifier
  elif 'occurrence' in name:
    return OccurrenceClassifier
  elif 'cluster' in name:
    return ClusteredOccurrenceClassifier
  elif 'xinyi' in name:
    return XinyiClassifier
  else:
    raise Exception('No such classifier: ' + name)


