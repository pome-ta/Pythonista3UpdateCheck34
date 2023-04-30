from objc_util import *

cheeses = ns(['Camembert', 'Feta', 'Gorgonzola'])
print(cheeses)


def compare(_cmd, obj1_ptr, obj2_ptr):
  obj1 = ObjCInstance(obj1_ptr)
  obj2 = ObjCInstance(obj2_ptr)
  # Sort the strings by length:
  return cmp(obj1.length(), obj2.length())


# Note: The first (hidden) argument `_cmd` is the block itself, so there are three arguments instead of two.
compare_block = ObjCBlock(compare,
                          restype=NSInteger,
                          argtypes=[c_void_p, c_void_p, c_void_p])

sorted_cheeses = cheeses.sortedArrayUsingComparator_(compare_block)
print(sorted_cheeses)

