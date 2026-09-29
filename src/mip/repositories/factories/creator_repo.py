from pathlib import Path
from mip.domain.models import Creator
from mip.repositories.json_file_repo import JsonFileRepo
from mip.repositories.in_memory import InMemoryRepo



def build_creator_in_memory() -> InMemoryRepo[Creator] :

    return InMemoryRepo(get_id = lambda c: c.creator_id)


def build_creator_in_json(path: Path) -> JsonFileRepo[Creator] :

    return JsonFileRepo(

        path = path , 
        get_id    =   lambda c : c.creator_id , 
        to_dict   =   lambda c : c.to_dict() , 
        from_dict =   lambda raw: Creator.from_dict(raw), 
    )




