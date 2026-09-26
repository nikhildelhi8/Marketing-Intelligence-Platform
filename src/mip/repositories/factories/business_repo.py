from pathlib import Path
from mip.domain.models import Business
from mip.repositories.json_file_repo import JsonFileRepo
from mip.repositories.in_memory import InMemoryRepo



def build_business_in_memory() -> InMemoryRepo[Business] :

    return InMemoryRepo(get_id = lambda c: c.business_id)


def build_business_in_json(path: Path) -> JsonFileRepo[Business] :

    return JsonFileRepo(

        path = path , 
        get_id    =   lambda c : c.business_id , 
        to_dict   =   lambda c : c.to_dict() , 
        from_dict =   lambda raw: Business.from_dict(raw), 
    )




