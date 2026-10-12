from pathlib import Path 
from mip.repositories.in_memory import InMemoryRepo
from mip.repositories.json_file_repo import JsonFileRepo
from mip.domain.models import Business, Campaign , Creator , CampaignStatus , SocialPost
from mip.repositories.factories import (build_campaign_in_json , build_campaign_analytics_in_json , build_business_in_json , build_creator_in_json , build_social_post_in_json)
import json


# reading the data file 


file_path = Path(__file__).parents[4] /"data"

raw_file_path = file_path/"seed"/"seeded_dataset.json"


with open(raw_file_path , 'r') as f:
    seeded_dataset = json.load(f) 



business_repo = build_business_in_json(file_path/"repo/businesses.json")
campaign_repo = build_campaign_in_json(file_path/"repo/campaigns.json")
creators_repo = build_creator_in_json(file_path/"repo/creators.json")
social_post_repo = build_social_post_in_json(file_path/"repo/social_post.json")




business_list = [
    Business.from_dict(raw_business)
    for raw_business in seeded_dataset["businesses"]
]

business_repo.add_many(business_list)




# with open(file_path/"repo/businesses.json", 'r') as f:
#     data = json.load(f)
#     print(data)


campaign_list = [
    Campaign.from_dict(raw_campaign)
    for raw_campaign in seeded_dataset["campaigns"]
]

campaign_repo.add_many(campaign_list)


# with open(file_path/"repo/campaigns.json", 'r') as f:
#     data = json.load(f)
#     print(data)



creator_list = [
    Creator.from_dict(raw_creator)
    for raw_creator in seeded_dataset["creators"]
]


creators_repo.add_many(creator_list)



# with open(file_path/"repo/creators.json", 'r') as f:
#     data = json.load(f)
#     print(data)



social_post_list = [

    SocialPost.from_dict(raw_post)
    for raw_post in seeded_dataset["posts"]
]

social_post_repo.add_many(social_post_list)



