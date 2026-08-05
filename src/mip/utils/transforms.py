'''
Reusable higher-order transform helpers used by ingestion and reporting.

Unike formatting.py , these functions dont validate / parse untrusted strings -- they operate
on already-trusted iterables and are pure(no side effects , no logging) by design
'''


from typing import Any , Callable , Iterable , Iterator , TypeVar

T = TypeVar("T")


def chunked(iterable : Iterable[T] , size: int) -> Iterator[list[T]] :

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


    current_chunk = []

    for item in iterable :
        current_chunk.append(item)
        if len(current_chunk) == size:
            yield current_chunk
            current_chunk = []

    if current_chunk :
        yield current_chunk





