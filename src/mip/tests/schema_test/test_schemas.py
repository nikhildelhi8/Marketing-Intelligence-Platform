# test_schemas.py

# A known-valid row for each schema (BusinessSchema, CampaignSchema, CreatorSchema, SocialPostSchema) constructs without error, and each enum field is actually an instance of its Enum class after validation (not still a string).
# A row with a bad enum value (e.g. "Category": "NotARealCategory") fails validation.
# A row with a negative creator_follower_count fails — this exercises your one custom field_validator.
# Alias mapping works: construct from a dict keyed by the CSV-style alias ("Post_ID", not post_id) and confirm it succeeds; construct from the Python attribute name instead and confirm whether it fails (this tells you whether populate_by_name is configured, which matters for anyone constructing these schemas outside the CSV path later).


import pytest 
from mip.schemas.ingestion_schemas import BusinessSchema , CampaignSchema , SocialPostSchema , CreatorSchema
from mip.domain.enums import Category , CampaignStatus , CreatorTier , ContentType , Platform

from pydantic import ValidationError as PydanticValidationError






def test_valid_business_schema(seeded_dataset):

    business_record = seeded_dataset["businesses"][3]

    business_record_validation = BusinessSchema.model_validate(business_record)

    assert isinstance(business_record_validation , BusinessSchema)

    assert isinstance(business_record_validation.business_domain , Category)


def test_valid_campaign_schema(seeded_dataset):

    campaign_record = seeded_dataset["campaigns"][4]

    campaign_record_validation = CampaignSchema.model_validate(campaign_record)

    assert isinstance(campaign_record_validation , CampaignSchema)
    assert isinstance(campaign_record_validation.campaign_domain , Category)
    assert isinstance(campaign_record_validation.campaign_status , CampaignStatus)


def test_valid_creator_schema(seeded_dataset) :

    creator_record = seeded_dataset["creators"][4]

    creator_record_validation = CreatorSchema.model_validate(creator_record)

    assert isinstance(creator_record_validation , CreatorSchema)
    assert isinstance(creator_record_validation.creator_niche , Category)
    assert isinstance(creator_record_validation.creator_tier , CreatorTier)


def test_valid_social_post_schema(seeded_dataset) :

    social_post_record = seeded_dataset["posts"][20]

    socialpost_record_validation = SocialPostSchema.model_validate(social_post_record)

    assert isinstance(socialpost_record_validation , SocialPostSchema)
    assert isinstance(socialpost_record_validation.platform , Platform)
    assert isinstance(socialpost_record_validation.content_type , ContentType)
    assert isinstance(socialpost_record_validation.category , Category)




def test_row_with_bad_enum():

    data = {
      "business_id": "BS_004",
      "business_name": "Gonzalez, Santos and Gardner",
      "business_domain": "NotCorrectDomain",
      "business_budget": 580000
    }

    with pytest.raises(PydanticValidationError) :
        validated = BusinessSchema.model_validate(data)



def test_negative_creator_follower_count():

    data = {
      "creator_id": "CR_069",
      "creator_name": "Mary Nguyen",
      "creator_bio": "Travel creator passinate about building a community of passionate enthusiasts",
      "creator_niche": "Travel",
      "creator_tier": "Nano",
      "creator_follower_count": -5344
    }


    with pytest.raises(ValueError):
        validated = CreatorSchema.model_validate(data)





def test_alias_mapping_socialpost(seeded_dataset):

    social_post_data = seeded_dataset["posts"][61]


    validated = SocialPostSchema.model_validate(social_post_data)

    assert validated.post_id == social_post_data.get("Post_ID")








    


   
