from typing import Iterator



def lazy_sqaures(n : int) -> Iterator[int] : 

    for i in range(1,n+1):
        print("computing: " , i)
        yield i*i


if __name__ == "__main__" :
    gen = lazy_sqaures(4)

    print("genertor created , no output above this line yet")

    for val in gen:
        print("got: " , val)


# because gen = lazy_squares(4) only generate a generator object , it will only start giving one result at a time once we loop through it.


