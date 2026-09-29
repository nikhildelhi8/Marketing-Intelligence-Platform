from typing import TypeVar , Generic , Callable 
from mip.exceptions import  NotFoundError , ValidationError  , DuplicateError


T = TypeVar("T")



class InMemoryRepo(Generic[T]) :

    def __init__(self , get_id: Callable[[T] , str]) :

        self.get_id  = get_id 
        self._data : dict[str , T] = {}



    def add(self , entity: T) -> None  :

       entity_id  = self.get_id(entity)

       if not entity_id :
                  raise ValidationError(
                      f" id - '{entity_id}' is not present , check the object "
                  )

       if entity_id in self._data:
           raise DuplicateError(
               f"entity with id - '{entity_id}' is already added"
           )
       
       self._data[entity_id] = entity



    def get(self , entity_id : str ) -> T | None :

        return self._data.get(entity_id)

    

    def get_or_raise(self , entity_id : str) -> T  :

        if entity_id not in self._data :

            raise NotFoundError(f"ID {entity_id} is not a valid id , please check and add the correct id  ")
        
        return self._data[entity_id]
            



    def list(self) -> list[T]  :

        if self._data :
            return list(self._data.values())

        return []


    def update(self , entity: T) -> None:

        entity_id = self.get_id(entity)

        if not entity_id :
              raise ValidationError(
                f" id - '{entity_id}' is not present , check the object "
               )

        if entity_id not in self._data:

              raise NotFoundError(
                    f"Entity with id '{entity_id}' not found "
                )

        self._data[entity_id] = entity


    def delete(self , entity_id: str) -> None :

        if  entity_id not in self._data :

            raise NotFoundError(
                f"Entity with id '{entity_id}' not found "
            )

        del self._data[entity_id]



        




        

    

     



