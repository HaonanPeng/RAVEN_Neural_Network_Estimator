import numpy as np 

a = [1,2,3,4,5]
b = [1,3,4]

a = [x for x in a if x not in b]
print(a)