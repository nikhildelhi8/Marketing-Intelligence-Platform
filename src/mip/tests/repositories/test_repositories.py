# Goal: One shared test body, run against both InMemoryRepo and JsonFileRepo, using the pytest.fixture(params=[...]) pattern from the concept explanation earlier.

# What to build:

# A small test-only dataclass (or reuse one real entity, e.g. Campaign) with a known get_id/to_dict/from_dict — keeps the test suite decoupled from having to fully construct valid Campaign objects with all their real fields.
# A conftest.py fixture parametrized over ["in_memory", "json_file"] that returns a fresh repo instance per test run — for the json_file branch, use pytest's built-in tmp_path fixture so each test gets an isolated, auto-cleaned temp file (never touching real data/).
# Test functions covering, at minimum:
# add() then get() returns the same entity.
# add() twice with the same id raises DuplicateError.
# add() with a falsy/missing id raises ValidationError.
# get() on a missing id returns None.
# get_or_raise() on a missing id raises NotFoundError; on a present id returns the entity.
# list() returns all added entities; returns [] when empty.
# update() on an existing id overwrites; on a missing id raises NotFoundError.
# delete() removes the entity; on a missing id raises NotFoundError.
# Run pytest -v tests/unit/test_repositories.py and confirm every test name appears twice in the output (once per repo type) — that doubling is the visible proof the parametrization is working.



from mip.exceptions import DuplicateError, NotFoundError, ValidationError
import pytest 

from mip.repositories.factories import build_campaign_in_json , build_campaign_in_memory
from mip.domain.models import Campaign 
from mip.domain.enums import Category , CampaignStatus

@pytest.fixture(params=["in_memory" , "json_file"])

def campaign_repo(request , tmp_path) :

    if request.param == "in_memory":
        return build_campaign_in_memory()
    else :
        return build_campaign_in_json(tmp_path/"campaigns.json")


def test_add_and_get(campaign_repo) :
    
   campaign = Campaign(
        campaign_id="C001",
        campaign_business_id="B001",
        campaign_domain=Category.EDUCATION,
        campaign_budget=50000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2026-09-01",
        campaign_end_date="2026-12-31",
        campaign_creator_ids=["CR001", "CR002"]
    )   
   campaign_repo.add(campaign)
   assert campaign_repo.get("C001") == campaign



def test_duplicate_add_raise(campaign_repo):

    campaign = Campaign(
    campaign_id="C001",
    campaign_business_id="B001",
    campaign_domain=Category.EDUCATION,
    campaign_budget=50000,
    campaign_status=CampaignStatus.ACTIVE,
    campaign_start_date="2026-09-01",
    campaign_end_date="2026-12-31",
    campaign_creator_ids=["CR001", "CR002"]
    )  

    campaign_repo.add(campaign)

    with pytest.raises(DuplicateError) :
        campaign_repo.add(campaign)   


def test_add_falsy_values(campaign_repo): 

    campaign = Campaign(
        campaign_id = "",
        campaign_business_id="B001",
        campaign_domain=Category.EDUCATION,
        campaign_budget=50000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2026-09-01",
        campaign_end_date="2026-12-31",
        campaign_creator_ids=["CR001", "CR002"]
    )  

    

    with pytest.raises(ValidationError):
        campaign_repo.add(campaign)
    

def test_get_falsy_values(campaign_repo): 

    campaign = Campaign(
        campaign_id = "100",
        campaign_business_id="B001",
        campaign_domain=Category.EDUCATION,
        campaign_budget=50000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2026-09-01",
        campaign_end_date="2026-12-31",
        campaign_creator_ids=["CR001", "CR002"]
    )   

    assert campaign_repo.get("1") == None



def test_get_or_raise_falsy_values(campaign_repo): 

    campaign = Campaign(
        campaign_id = "100",
        campaign_business_id="B001",
        campaign_domain=Category.EDUCATION,
        campaign_budget=50000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2026-09-01",
        campaign_end_date="2026-12-31",
        campaign_creator_ids=["CR001", "CR002"]
    )  

    campaign_repo.add(campaign)

    with pytest.raises(NotFoundError):
        campaign_repo.get_or_raise("1")



def test_get_list(campaign_repo) : 

    campaign = Campaign(
        campaign_id = "100",
        campaign_business_id="B001",
        campaign_domain=Category.EDUCATION,
        campaign_budget=50000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2026-09-01",
        campaign_end_date="2026-12-31",
        campaign_creator_ids=["CR001", "CR002"]
    )
    campaign2 = Campaign(
            campaign_id = "101",
            campaign_business_id="B001",
            campaign_domain=Category.EDUCATION,
            campaign_budget=50000,
            campaign_status=CampaignStatus.ACTIVE,
            campaign_start_date="2026-09-01",
            campaign_end_date="2026-12-31",
            campaign_creator_ids=["CR001", "CR002"]
    )

    campaign_repo.add(campaign)
    campaign_repo.add(campaign2)

    campaigns = [
        Campaign(
            campaign_id="100",
            campaign_business_id="B001",
            campaign_domain=Category.EDUCATION,
            campaign_budget=50000,
            campaign_status=CampaignStatus.ACTIVE,
            campaign_start_date="2026-09-01",
            campaign_end_date="2026-12-31",
            campaign_creator_ids=["CR001", "CR002"],
        ),

        Campaign(
            campaign_id="101",
            campaign_business_id="B001",
            campaign_domain=Category.EDUCATION,
            campaign_budget=50000,
            campaign_status=CampaignStatus.ACTIVE,
            campaign_start_date="2026-09-01",
            campaign_end_date="2026-12-31",
            campaign_creator_ids=["CR001", "CR002"],
        ),
    ]

    assert campaign_repo.list() == campaigns







def test_delete_entity(campaign_repo) :

    campaign = Campaign(
            campaign_id = "100",
            campaign_business_id="B001",
            campaign_domain=Category.EDUCATION,
            campaign_budget=50000,
            campaign_status=CampaignStatus.ACTIVE,
            campaign_start_date="2026-09-01",
            campaign_end_date="2026-12-31",
            campaign_creator_ids=["CR001", "CR002"]
        )
    campaign2 = Campaign(
                campaign_id = "101",
                campaign_business_id="B001",
                campaign_domain=Category.EDUCATION,
                campaign_budget=50000,
                campaign_status=CampaignStatus.ACTIVE,
                campaign_start_date="2026-09-01",
                campaign_end_date="2026-12-31",
                campaign_creator_ids=["CR001", "CR002"]
        )
    
    campaign_repo.add(campaign)
    campaign_repo.add(campaign2)
    
    campaign_updated = Campaign(
                    campaign_id = "101",
                    campaign_business_id="B001",
                    campaign_domain=Category.EDUCATION,
                    campaign_budget=60000,
                    campaign_status=CampaignStatus.ACTIVE,
                    campaign_start_date="2026-09-01",
                    campaign_end_date="2026-12-31",
                    campaign_creator_ids=["CR001", "CR002"]
            )

    campaign_repo.delete("101") 

    with pytest.raises(NotFoundError):
        campaign_repo.get_or_raise("101")



def test_update_entity(campaign_repo) :

    campaign = Campaign(
            campaign_id = "100",
            campaign_business_id="B001",
            campaign_domain=Category.EDUCATION,
            campaign_budget=50000,
            campaign_status=CampaignStatus.ACTIVE,
            campaign_start_date="2026-09-01",
            campaign_end_date="2026-12-31",
            campaign_creator_ids=["CR001", "CR002"]
        )
    campaign2 = Campaign(
                campaign_id = "101",
                campaign_business_id="B001",
                campaign_domain=Category.EDUCATION,
                campaign_budget=50000,
                campaign_status=CampaignStatus.ACTIVE,
                campaign_start_date="2026-09-01",
                campaign_end_date="2026-12-31",
                campaign_creator_ids=["CR001", "CR002"]
        )
    
    campaign_repo.add(campaign)
    campaign_repo.add(campaign2)
    
    campaign_updated = Campaign(
                    campaign_id = "101",
                    campaign_business_id="B001",
                    campaign_domain=Category.EDUCATION,
                    campaign_budget=60000,
                    campaign_status=CampaignStatus.ACTIVE,
                    campaign_start_date="2026-09-01",
                    campaign_end_date="2026-12-31",
                    campaign_creator_ids=["CR001", "CR002"]
            )

    campaign_updated_wrong = Campaign(
                        campaign_id = "102",
                        campaign_business_id="B001",
                        campaign_domain=Category.EDUCATION,
                        campaign_budget=60000,
                        campaign_status=CampaignStatus.ACTIVE,
                        campaign_start_date="2026-09-01",
                        campaign_end_date="2026-12-31",
                        campaign_creator_ids=["CR001", "CR002"]
                )

    campaign_repo.update(campaign_updated) 

    assert campaign_repo.get("101") == campaign_updated

    with pytest.raises(NotFoundError):
        campaign_repo.update(campaign_updated_wrong)