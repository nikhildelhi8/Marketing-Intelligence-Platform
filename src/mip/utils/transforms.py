'''
Reusable higher-order transform helpers used by ingestion and reporting.

Unike formatting.py , these functions dont validate / parse untrusted strings -- they operate
on already-trusted iterables and are pure(no side effects , no logging) by design
'''


from typing import  Callable , Iterable , Iterator , TypeVar
import logging
from functools import reduce

logger = logging.getLogger(__name__)


T = TypeVar("T")


def chunked(iterable : Iterable[T] , size: int) : 

    if size<=0 : 
        logger.warning("Warning: Size is zero or negative!")
        raise ValueError("Chunking size is zero or negative")

    return _chunked_impl(iterable , size)

def _chunked_impl(iterable : Iterable[T] , size: int) -> Iterator[list[T]] :

    '''
    Split 'iterable' into consecutive chunks of at most 'size' items each.

    Args:
        iterable: Any iterable of items.
        size: Maximum number of items per chunk. Must be a positive integer.

    Yields:
        Lists of up to 'size' items , preserving original order.

    Example:
        list(chunked([1,2,3,4,5] , 2)) == [[1,2],[3,4],[5]]
    
    '''

    if size<=0 : 
        logger.warning("Warning: Size is zero or negative!")
        raise ValueError("Chunking size is zero or negative")
        

    current_chunk = []

    for item in iterable :
        current_chunk.append(item)
        if len(current_chunk) == size:
            yield current_chunk
            current_chunk = []

    if current_chunk :
        yield current_chunk




def flatten(nested: Iterable[Iterable[T]]) -> Iterator[T]:

    '''
    Flatten one level of nested iterables into a single flat sequence

    Args:
        nested: An iterable of iterables (eg a list of lists)

    Yields:
        Individual items from each inner iterable , in order.

    Example:
        list(flatten([[1,2] , [3] , [4,5]])) == [1,2,3,4,5]

    '''
    for item in nested :

        if isinstance(item , Iterable) and not isinstance(item , (str , bytes)) :
            yield from item
        else :
            yield item





def apply_pipeline(value: T , *fns: Callable[[T] , T]) -> T :
    '''
    Apply a sequence of single-argument functions to 'value' , left to right.

    Args:
        value: The initial input.

        *fns: Function applied in order; each receives the previous functions output.

    Returns:
        The final value after all functions have been applied

    Example:
        apply_pipeline(3 , lambda x:x+1 , lambda x: x*2) == 8

    '''
    updated_value = value # i wanted to created a variable based on the type of the value , i will got the value by type(value) but after that the empty value initialization is different for each value type

    

    # for fn in fns :
    #     updated_value = fn(updated_value)


    # return updated_value


    return reduce(lambda v, fn: fn(v), fns, value)
    


        

    



