from typing import Iterable, Set, AbstractSet, Dict, Mapping, Tuple, List, TypeVar
from itertools import chain, combinations
from pprint import pformat

T = TypeVar('T')

def generate_powerset(s: AbstractSet[T]) -> Iterable[Set[T]]:
  return map(set, chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def jaccard_index(a: Set[T], b: Set[T]) -> float:
  return len(a.intersection(b)) / len(a.union(b))


def weighted_jaccard_index(a: Set[str], b: Set[str], weights: Mapping[str, float]):
  union = a.union(b)

  x = list(map(lambda v: weights[v] if v in a else 0, union))
  y = list(map(lambda v: weights[v] if v in b else 0, union))

  c = sum(list(map(lambda i: min(x[i], y[i]), range(len(x)))))
  d = sum(list(map(lambda i: max(x[i], y[i]), range(len(x)))))
  return  c / d

def weights_with_default(s: AbstractSet[str], weights: Mapping[str, float]) -> Dict[str, float]:
  result = {}
  for key in s:
    result[key] =  weights[key] if key in weights else 1
  return result

def sorted_jaccard_indices(a: Set[str], b: Iterable[Set[str]]) -> Iterable[Tuple[Set[str], float]]:
  indices = map(lambda s: (s, jaccard_index(a, s)), b)
  return sorted(indices, key=lambda entry: entry[1], reverse=True)
  
def sorted_weighted_jaccard_indices(a: Set[str], b: Iterable[Set[str]], weights: Mapping[str, float]) -> Iterable[Tuple[Set[str], float]]:
  indices = map(lambda s: (s, weighted_jaccard_index(a, s, weights)), b)
  return sorted(indices, key=lambda entry: entry[1], reverse=True)

def set_to_sorted_string(a: AbstractSet[str]) -> str:
  return f'{{{", ".join(sorted(a))}}}'

def index_to_string(index: Tuple[Set[str], float]) -> str:
  return f'{index[1]:.3f} {set_to_sorted_string(index[0])}'

def print_indices(search: Set[str], words: Set[str], weights: Mapping[str, float]):
  filledWeights = weights_with_default(words, weights)

  print(f'Search: {set_to_sorted_string(search)}')
  print(f'Words: {set_to_sorted_string(words)}')
  print(f'Weights: {pformat(filledWeights)}')


  powerset = list(generate_powerset(words))

  width = 3
  print('')
  print('jaccard indices')
  
  for i, entry in enumerate(sorted_jaccard_indices(search, powerset)):
    print(f'{i+1:{width}} {index_to_string(entry)}')

  print('')
  print('weighted jaccard indices')
  for i, entry in enumerate(sorted_weighted_jaccard_indices(search, powerset, filledWeights)):
    print(f'{i+1:{width}} {index_to_string(entry)}')

# Set weights (default: 1)
weights = {
  'a': 2
}
# Set of all words
words = {'a', 'b', 'c', 'd', 'e'}
# Search term
search = {'a','b','c'}

print_indices(search, words, weights)
