from typing import Callable
import timeit 
from functools import reduce


def apply_pipeline(value , *fns: Callable) : 

    if len(fns) ==0 :
        return value 

    return reduce(lambda value , fn: fn(value)  , fns , value)




result = apply_pipeline(2, lambda x: x + 3, lambda x: x * 2)
# Step 1: 2 + 3 = 5
# Step 2: 5 * 2 = 10
# -> 10

result1 = apply_pipeline("hello")  # no fns passed
# -> "hello"  (unchanged)

print(result , result1)





class Creator :
    def __init__(self , niche , engagement ):
        self.niche = niche ,
        self.engagement = engagement



