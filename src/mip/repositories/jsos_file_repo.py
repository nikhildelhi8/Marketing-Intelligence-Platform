from typing import TypeVar , Generic , Callable 
from pathlib import Path
from mip.exceptions import NotFoundError , DuplicateError , ValidationError , MIPError , RepositoryError
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

        self.__load()


    def __load(self) -> None

        loaded_json = {}
        failed_parsed_record = []

        if not self.path.exists():
            self._data = {}
            return 

        with open(self.path , 'r') as f :

            try :
                loaded_json = json.load(f)
            
            except  json.JSONDecodeError as e :
                raise RepositoryError(
                    f"path : '{self.path}' does not exist check it getting error : {e} "
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

       


    def __flush(self , path: Path) -> None :

        failed_json_parsed_record = []
        json_safe_dict = {}

        for entity_id , entity in self._data.items():

            try:
                json_safe_dict = self.to_dict(entity)

            except Exception as e :

                logger.warning(f"Json parsing failed for {entity_id}")
                failed_json_parsed_record.append({entity_id : entity})
                continue

        if len(failed_json_parsed_record) > 0 :
            logger.warning()

       # atomic writing to temp file and then replacing it with original file 

        fd , tmp_path = tempfile.mkstemp(dir=path.parent)

        try:
            with os.fdopen(fd , 'w') as f:
                json.dump(json_safe_dict , f)
            os.replace(tmp_path , path)

        except Exception as e :
            raise RepositoryError(
                f" writing to file is having some issues getting {e}"
            )
        finally :
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        

        

        





        
              
            
                

        
        
        



        


            


        




