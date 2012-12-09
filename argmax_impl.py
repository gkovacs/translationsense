from itertools import *
from operator import *

def argmax(items):
  if type(items) == type([]):
    return argmax_index(items)
  if type(items) == type({}):
    return argmax_pairs(items.items())
  return argmax_pairs(items)

# given an iterable of pairs return the key corresponding to the greatest value
def argmax_pairs(pairs):
    return max(pairs, key=itemgetter(1))[0]

# given an iterable of values return the index of the greatest value
def argmax_index(values):
    return argmax(izip(count(), values))

# given an iterable of keys and a function f, return the key with largest f(key)
def argmax_f(keys, f):
    return argmax((k, f(k)) for k in keys)

