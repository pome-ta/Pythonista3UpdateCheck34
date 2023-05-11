import objc_util

cheeses = objc_util.ns(['Camembert', 'Feta', 'Gorgonzola'])

print(cheeses)


def compare(_cmd, a, b):
  a = objc_util.ObjCInstance(a).length()
  b = objc_util.ObjCInstance(b).length()
  if a > b: return 1
  if a < b: return -1
  return 0


# Note: The first (hidden) argument `_cmd` is the block itself, so there are three arguments instead of two.
compare_block = objc_util.ObjCBlock(
  compare,
  restype=objc_util.NSInteger,
  argtypes=[objc_util.c_void_p, objc_util.c_void_p, objc_util.c_void_p])

sorted_cheeses = cheeses.sortedArrayUsingComparator_(compare_block)
print(sorted_cheeses)

