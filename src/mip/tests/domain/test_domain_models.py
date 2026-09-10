import pytest 
from mip.domain.models import Business , Campaign , Creator , SocialPost , CampaignAnalytics
from mip.domain.enums import Category , CampaignStatus , ContentType , CreatorTier




# Construction path

def test_business_creation_valid():

    data = {

        "business_id" : "BS_999" , 
        "business_name" : "Test co" , 
        "business_domain" : "Entertainment"  , 
        "business_budget" : 5000 , 
    }

    business = Business.from_dict(data)

    assert business.business_id == "BS_999"
    assert business.business_domain == Category.ENTERTAINMENT
    assert business.business_budget == 5000


# invarient rejection 

def test_business_rejecting_object():

    data = {
        "business_id" : "BS_999" , 
        "business_name" : "Test co" , 
        "business_domain" : "Entertainment"  , 
        "business_budget" : -700 
    }

    with pytest.raises(ValueError):
        business = Business.from_dict(data)


# from_dict test 



def test_business_from_dict_real_record(seeded_dataset):
    record = seeded_dataset["businesses"][3]
    business = Business.from_dict(record)

    assert business.business_id == record["business_id"]
    assert business.business_name == record["business_name"]
    assert business.business_domain == Category(record["business_domain"])
    assert business.business_budget == record["business_budget"]



# to_dict round_trip 

def test_business_round_trip(seeded_dataset):
    record = seeded_dataset["businesses"][3]
    result = Business.from_dict(record).to_dict()

    assert result == record




def test_all_businesses_load(seeded_dataset):
    records = seeded_dataset["businesses"]  # verify this key casing yourself
    for i, record in enumerate(records):
        try:
            Business.from_dict(record)
        except Exception as e:
            pytest.fail(f"Business record at index {i} failed: {e}\nRecord: {record}")
        
    





