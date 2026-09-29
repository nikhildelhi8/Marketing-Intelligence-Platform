from pathlib import Path
from mip.domain.models import CampaignAnalytics
from mip.repositories.json_file_repo import JsonFileRepo
from mip.repositories.in_memory import InMemoryRepo



def build_campaign_analytics_in_memory() -> InMemoryRepo[CampaignAnalytics] :

    return InMemoryRepo(get_id = lambda c: c.campaign_id)


def build_campaign_analytics_in_json(path: Path) -> JsonFileRepo[CampaignAnalytics] :

    return JsonFileRepo(

        path = path , 
        get_id    =   lambda c : c.campaign_id , 
        to_dict   =   lambda c : c.to_dict() , 
        from_dict =   lambda raw: CampaignAnalytics.from_dict(raw), 
    )




