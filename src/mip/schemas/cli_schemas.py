from pydantic import BaseModel
from mip.domain.enums import Category
from mip.schemas.shared_validators import PositiveBudget



class CreateCampaignInput(BaseModel) :

    campaign_domain : Category
    campaign_budget : PositiveBudget 
    campaign_business_id : str 


   