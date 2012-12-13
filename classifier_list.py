from classifier_maxcount import *
from classifier_occurrence import *
from classifier_fraction import *
from classifier_clustered import *
from classifier_xinyi import *
from classifier_postag import *
from classifier_postag_occurrence import *
from classifier_nearby_postag_occurrence import *

@memoized
def getClassifier(classifierType, word,fv_size_scale=1.0,thresh=0.0):
  return classifierType(word,fv_size_scale,thresh)

def getClassifierByName(name):
  name = name.lower()
  if 'max' in name:
    return MaxCountClassifier
  elif 'fraction' in name:
    return FractionOccurrenceClassifier
  elif 'posoccurrence' in name:
    return POSTagOccurrenceClassifier
  elif 'occurrence' in name:
    return OccurrenceClassifier
  elif 'cluster' in name:
    return ClusteredOccurrenceClassifier
  elif 'nearbypos' in name:
    return NearbyPOSTagOccurrenceClassifier
  elif 'pos' in name:
    return POSTagClassifier
  elif 'xinyi' in name:
    return XinyiClassifier
  else:
    raise Exception('No such classifier: ' + name)


