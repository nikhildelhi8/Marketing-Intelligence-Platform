from typing import TypeVar , Generic , Callable 
from pathlib import Path
from mip.exceptions import NotFoundError , DuplicateError , ValidationError , RepositoryError
import json
import os , tempfile

import logging


logger = logging.getLogger(__name__)



T  = TypeVar("T")


class JsonFileRepo(Generic[T]):

    def __init__(self , path : Path , get_id : Callable[[T] , str] , to_dict: Callable[[T] , dict] , from_dict : Callable[[dict] , T]) :

        self.path = path 
        self.get_id = get_id
        self.to_dict = to_dict
        self.from_dict = from_dict
        self._data : dict[str , T] = {}

        self.path.parent.mkdir(parents=True , exist_ok=True)

        self._load()


    def _load(self) -> None :


        if not self.path.exists():
            self._data = {}
            return 

        with open(self.path , 'r') as f :

            try :
                loaded_json = json.load(f)
            
            except  json.JSONDecodeError as e :
                raise RepositoryError(
                    f"Content aren't valid JSON , getting error -: {e} "
                )

        
        # for entity_id , item in loaded_json.items() :

        #     try : 
        #         validatedObject = self.from_dict(item)
        #         self._data[entity_id] = validatedObject

        #     except Exception as e  :
        #         raise RepositoryError(
        #             f"got error while converting {entity_id} dict  to dataclass object getting {e}"
        #         )

        failed_parsed_record = []
        
        for entity_id , item in loaded_json.items() :

            try:     
                validatedObject = self.from_dict(item)

            except Exception as e :
                logger.warning(f"parsing failed for {entity_id}")
                failed_parsed_record.append({entity_id: item})
                continue

            self._data[entity_id] = validatedObject

        if len(failed_parsed_record) > 0 : 

            logger.warning(f"Encountered issue while parsing json data to {T} objects '\n' Failed entries -- {failed_parsed_record}" )

       


    def _flush(self) -> None :

        json_safe_dict = {}

        for entity_id , entity in self._data.items():

            try:
                json_safe_dict[entity_id] = self.to_dict(entity)

            except Exception as e :

                raise RepositoryError(f"Failed to serialize entity {entity_id} : {e}")


       # atomic writing to temp file and then replacing it with original file 

        fd , tmp_path = tempfile.mkstemp(dir=self.path.parent)

        try:
            with os.fdopen(fd , 'w') as f:
                json.dump(json_safe_dict , f)
            os.replace(tmp_path , self.path)

        except Exception as e :
            raise RepositoryError(
                f" writing to file is having some issues getting {e}"
            )
        finally :
            if os.path.exists(tmp_path):
                os.remove(tmp_path)



    def add(self , entity: T) -> None:

        entity_id = self.get_id(entity)

        if not entity_id:
            raise ValidationError(
                f"id - '{entity_id}' is not present , check the object"
            )

        if entity_id in self._data:

            raise DuplicateError(
                f"Entity with id - '{entity_id}' is already added"
            )

        self._data[entity_id] = entity

        self._flush()



    def get(self , entity_id : str) -> T | None :
        
        return self._data.get(entity_id)

    
    def get_or_raise(self , entity_id: str) -> T :

        if entity_id not in self._data :

            raise NotFoundError(f"ID {entity_id} is not a valid id , please check the id- {entity_id} passed")

        return self._data[entity_id]
        

    def list(self) -> list[T] :

        return list(self._data.values())



    def update(self , entity : T) -> None :

        entity_id = self.get_id(entity)

        if not entity_id :
            raise ValidationError(
                f" id - {entity_id} is not present , check the object"
            )

        if entity_id not in self._data :

            raise NotFoundError(
                f"Entity with id : {entity_id} is not found"
            )

        self._data[entity_id] = entity

        self._flush()



    def delete(self , entity_id : str) -> None :

        if entity_id not in self._data :

            raise NotFoundError(
                f"Entity with id '{entity_id}' not found"
            )

        del self._data[entity_id]

        self._flush()




        

        





        
              
            
                

        
        
        



        


            


        




