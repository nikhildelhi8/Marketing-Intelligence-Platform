from mip.domain.models import Business
from mip.repositories.factories import build_business_in_memory
from mip.services.business_service import BusinessService
from mip.exceptions import NotFoundError

import pytest


business_repo = build_business_in_memory()

business_repo.add(
    Business(

        business_id = "B-01" , 
        business_name = "Khadi Bhandar" , 
        business_domain = "Fashion" , 
        business_budget = 300000
    )
)

business_service  = BusinessService(business_repo)

def test_business_repo(): 

    with pytest.raises(NotFoundError) :

        business_service.delete_business("B-02")

    business_service.delete_business("B-01")

    with pytest.raises(NotFoundError) :
        business_service.delete_business("B-01")

    



    






