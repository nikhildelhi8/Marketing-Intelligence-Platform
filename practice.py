from typing import Callable
from functools import reduce
import timeit


# Drill 1 
def apply_pipeline(value , *fns: Callable):

    if len(fns) == 0 : 
        return value

    return reduce(lambda value , fn : fn(value) , fns , value)


result = apply_pipeline(2 , lambda x : x+3 , lambda x: x*2)


apply_pipeline("hello")

print(result)



# Drill 3 Part a 




def handle_create(payload: dict) -> str:
    return f"created {payload}"

def handle_delete(payload: dict) -> str:
    return f"deleted {payload}"


COMMAND_HANDLERS: dict[str , Callable[[dict] , str]] = {

    "create" : handle_create , 
    "delete" : handle_delete 
}

def dispatch(command: str , payload: dict) -> str:

    handler = COMMAND_HANDLERS.get(command)

    if handler is None:
        raise ValueError(f"Unknown Command: {command}")

    return handler(payload)




# result = dispatch("create" , {"name": "nikhil"})
# result2 = dispatch("unknown" , {"name" : "nikhil"})
# print(result)


# drill 3 part b 


def benchmark_list_vs_generator(n: int = 1000000) -> None :


   list_timiing =  timeit.timeit(lambda : sum([x**2 for x in range(n)]) , number=5)
   gen_timing   =  timeit.timeit(lambda : sum(x**2 for x in range(n)) , number = 5)


   print(f"average list timing {list_timiing/5}")
   print(f"average gen_timing : {gen_timing/5}")




benchmark_list_vs_generator()



creator1 = {"niche": "fashion" , "engagement" : 3.2}
creator2 = {"niche": "tech" , "engagement" : 3.2}


def build_filter(**criteria) -> Callable[[dict] , bool] :

    def predicate(record:dict) -> bool:

        # for kr , vr in criteria.items() :
        #     if kr in record.keys() :
                
        #         if record.get(kr) == vr:
        #             return True 
        #         else :
        #             return False 
        #     else :
        #         return False

        return all(  record.get(kr) == vr  for kr , vr in criteria.items() if kr in record.keys() )
    return predicate

                
is_match = build_filter(niche="fashion")
print(is_match(creator1))   # -> True
print(is_match(creator2))   # -> False

is_match2 = build_filter(niche="fashion", engagement=3.2)
print(is_match2(creator1) ) # -> True  (both match)             
                 



            


        

