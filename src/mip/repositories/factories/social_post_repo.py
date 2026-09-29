from pathlib import Path
from mip.domain.models import SocialPost
from mip.repositories.json_file_repo import JsonFileRepo
from mip.repositories.in_memory import InMemoryRepo



def build_social_post_in_memory() -> InMemoryRepo[SocialPost] :

    return InMemoryRepo(get_id = lambda c: c.post_id)


def build_social_post_in_json(path: Path) -> JsonFileRepo[SocialPost] :

    return JsonFileRepo(

        path = path , 
        get_id    =   lambda c : c.post_id , 
        to_dict   =   lambda c : c.to_dict() , 
        from_dict =   lambda raw: SocialPost.from_dict(raw), 
    )




