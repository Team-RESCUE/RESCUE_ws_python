import numpy as np

starts = np.array([1000, 1000])
ends = np.array([1100, 1350])

diff = np.absolute(np.subtract(ends,starts))
sum = np.add(ends,starts)

compare = (ends>1100).astype(int)
boolin = compare == 1

print(ends[boolin])