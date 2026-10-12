from uuid import uuid4

from mip.domain.models import Business
from mip.domain.enums import CampaignStatus
from mip.exceptions import BusinessRuleError, DuplicateError , NotFoundError
from mip.schemas.dto import CreateBusinessDTO
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mip.repositories.in_memory import InMemoryRepo

class BusinessService :

    def __init__(self , business_repo : InMemoryRepo , campaign_repo: InMemoryRepo) -> None :

        self._business_repo = business_repo
        self._campaign_repo = campaign_repo



    def create_business(
            self , 
            request: CreateBusinessDTO ,    
    ) -> Business :

        business_id = f"BS_{uuid4().hex[:8]}"

        business = Business(
            business_id= business_id , 
            business_name=request.business_name ,
            business_domain = request.business_domain ,
            business_budget= request.business_budget
        )

        self._business_repo.add(business)

        return business



    def delete_business( self , business_id : str) -> None :

        self._business_repo.get_or_raise(business_id)


        has_active_campaign = any(
            campaign.business_id == business_id and campaign.status is CampaignStatus.ACTIVE
            for campaign in self._campaign_repo.list()
        )

        if has_active_campaign:
            raise BusinessRuleError(f"{business_id} has active campaigns listed , cannot delete it")

        self._business_repo.delete(business_id)



    def get_business(self , business_id : str) -> Business :



        try:
           business =  self._business_repo.get_or_raise(business_id) 
           return business

        except Exception as e :
           e 

        

        
    

        


    

 









