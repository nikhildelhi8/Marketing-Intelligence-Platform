from typing import TypeVar , Generic , Callable 
from pathlib import Path
from mip.exceptions import NotFoundError , DuplicateError , ValidationError , MIPError
import json



T  = TypeVar("T")


class JsonFileRepo(Generic[T]):

    def __init__(self , path : Path , get_id : Callable[[T] , str] , to_dict: Callable[[T] , dict] , from_dict : Callable[[dict] , T]) :

        self.path = path 
        self.get_id = get_id
        self.to_dict = to_dict
        self.from_dict = from_dict
        self._data : dict[str , T] = {}

        if not self.path.exists():
            self.path.parent.mkdir(parents=True , exist_ok=True)

        self._load()


    def _load(self) -> None :

        loaded_json = {}

        if not self.path.exists():
            self._data = {}
            return 

        with open(self.path , 'r') as f :

            try :
                loaded_json = json.load(f)
            
            except  json.JSONDecodeError as e :
                raise NotFoundError(
                    f"path : '{self.path}' does not exist check it getting error : {e} "
                )

        try :
            for item in loaded_json :
                    entity_id  = self.get_id(item)
                    raw        = self.from_dict(item)
                    self._data[entity_id] = raw

        except Exception as e :
            raise MIPError(
                f"got error while converting loaded_json to dataclass object getting {e}"
            )
        



        


            


        




