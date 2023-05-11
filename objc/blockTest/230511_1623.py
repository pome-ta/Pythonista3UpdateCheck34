import ctypes
#import objc_util
from objc_util import ObjCBlock, ObjCInstance, ns, NSInteger

import pprint
import pdbg

cheeses = ns(['Camembert', 'Feta', 'Gorgonzola'])

print(cheeses)


def compare(_cmd, a, b):
  a = ObjCInstance(a).length()
  b = ObjCInstance(b).length()
  if a > b: return 1
  if a < b: return -1
  return 0


# Note: The first (hidden) argument `_cmd` is the block itself, so there are three arguments instead of two.
compare_block = ObjCBlock(
  compare,
  restype=NSInteger,
  argtypes=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p])

sorted_cheeses = cheeses.sortedArrayUsingComparator_(compare_block)
print(sorted_cheeses)
pdbg.state(compare_block)
pprint.pprint(dir(compare_block))

