import pytest 

from mip.ingestion.seed_data import seed_dataset  , check_referential_integrity
from mip import PROJECT_ROOT



file_path_test = PROJECT_ROOT/'data'/'raw'/'influencer_marketing_pytest.csv'

file_path = PROJECT_ROOT/'data'/'raw'/'influencer_marketing.csv'






def test_pipeline_seed_dataset():

    result , pydantic_result = seed_dataset(file_path_test) 

    campaign_list = result["campaigns"]

    for item in campaign_list :

        assert item.get("campaign_creator_ids") == []


def test_refrential_integrity():

    result , pydantic_result = seed_dataset(file_path)

    with pytest.raises(ValueError) :
        check_referential_integrity(result)






