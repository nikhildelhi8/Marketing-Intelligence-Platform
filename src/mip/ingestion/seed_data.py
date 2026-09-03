'''
seed_data.py

Syntesizes Business and Creator pools via Faker , then wires FK relationships onto real Kaggle rows(from ingestion.csv_loader.loader_influencer_csv) to 
produce the canonical seeded dataset 


Design decisions locked this phase:

-- Creator pool size: 60 creators / 12 categories( niche)
-- Creator tiers: temporary module-level constant here : Phase 4 will promote this to CreatorTier(Enum) once domain/enums.py exists.

-- get_tier() will not return None but will raise the Value Error , as the follower count should lie with the grouping created in accordance with the raw_csv file.

-- Also no Mega tier as we are working in strict accordance with the raw_data that we are using so we only have ( Nano , Micro , Mid-tier  Macro )

-- Row-to-Creator matching : niche + tier band exact match , falling back to niche + adjacent tier , then niche only. Tier is never dropped before niche.

-- Row-to-Campaign matching : niche + active/completed campaign status  , falling to niche + draft , then None on no match 

--AGENCY_NICHES /CREATOR POOL spans 12 niches and 6 creator per niches , the idea is to have maximum coverage of the data.

'''


from faker import Faker
from faker.providers import DynamicProvider
from datetime import date , datetime , timedelta
from pprint import pprint
from pathlib import Path
from mip.ingestion.csv_loader import load_influencer_csv
from mip import PROJECT_ROOT
import json



CSV_PATH = PROJECT_ROOT/ "data" / "raw" / "influencer_marketing.csv"

JSON_OUTPUT_PATH = PROJECT_ROOT/ "data" / "seed" / "seeded_dataset.json" 



# Nano -- (500 -- 10000)
# Micro -- (10000 -- 50000)
# Mid-tier -- (50000 -- 100000)
# Macro -- (100000 -- 500000)


CREATOR_TIER_BANDS : list[tuple[str , int , int]] = [

    ('Nano' , 500, 10000) , 
    ('Micro', 10001 , 50000) , 
    ('Mid-tier' , 50001 , 100000) , 
    ('Macro' , 100001 , 500000 )
]

CREATOR_NICHES : list[str] = ['Business','Education','Entertainment','Fashion','Fitness','Food','Gaming','Health','Lifestyle','Sports','Technology','Travel']

 

fake  = Faker()


def get_tier (follower_count: int) ->  str:

    '''
    Map a raw follower count to a tier label using CREATOR_TIER_BANDS
    '''
    if not isinstance(follower_count , int) or follower_count < 0:
        raise ValueError (f"Follower count must be a non-negative intege , got {follower_count}")

    for tier , min_count , max_count in CREATOR_TIER_BANDS :

        if min_count<=follower_count<=max_count :
            return tier

    raise ValueError (
        f"the follower count -- {follower_count} does not lie in the range of tier bands {CREATOR_TIER_BANDS}"
    )


def build_creator_pool(
        niches: list[str] , 
        creators_per_niche : int , 
        seed : int = 42 , 
    ) -> list[dict] :

    '''
    Generate a fixed pool of synthetic Creator records spread across `niches`,
    with `creators_per_niche` creators per niche.

    Each creator dict should carry (at minimum): a synthetic creator_id,
    Faker-generated name and bio, a niche, a tier, and a follower_count
    sampled from within that tier's band
    '''
    # 3. Create a Dynamic Provider to handle the creator templates
    # This provider pulls random tech/creative actions to build fresh bios

   
    fake.seed_instance(seed)

    creator_actions = [
        "sharing daily insights and tips",
        "exploring the latest trends and future outlooks",
        "building a community of passionate enthusiasts",
        "creating engaging content and deep-dives",
        "breaking down complex ideas into simple steps"
    ]

    creator_provider = DynamicProvider(
        provider_name='creator_action' , 
        elements=creator_actions , 
        generator=fake , 
    )

    fake.add_provider(creator_provider)


    creator_pool = []

    creator_idx = 1
   

    for niche in niches :

        for _ in range(creators_per_niche) :

            # creating id 
            creator_id = f"CR_{creator_idx:03d}"
            creator_idx += 1

            # extracting random creator tier brands 
            creator_tier_brand = fake.random_element(CREATOR_TIER_BANDS)

            tier , min_follower_count , max_follower_count = creator_tier_brand

            # creating random bio message 
            action = fake.creator_action()
            bio = f"{niche} creator passinate about {action}"


            creator_record = {
                                "creator_id" :   creator_id , 
                                "creator_name" : fake.name() , 
                                "creator_bio" :          bio,
                                "creator_niche" :        niche , 
                                "creator_tier" :         tier  , 
                                "creator_follower_count"  :   fake.random_int(min =min_follower_count , max = max_follower_count)
                            }

            creator_pool.append(creator_record)


    return creator_pool


def generate_businesses(n: int , seed: int = 42) -> list[dict] :
    '''
    Generate n synthetic Business records via faker : company name , industry and the budget range.

    Independent of CSV rows and independent of the creator pool -- this pool exists purely so 
    campaign/post rows can later sample a business_id from it.
    '''

    fake.seed_instance(seed)

    
    business_pool = []
    business_idx = 1 

    for _ in range(n) :

        business_id = f"BS_{business_idx:03d}"
        business_idx += 1 

        

        business_record = {

            "business_id"           : business_id, 
            "business_name"         : fake.company() , 
            "business_domain"       : fake.random_element(CREATOR_NICHES) , 
            "business_budget"       : fake.random_int(min=10000 , max=750000 , step = 5000)
        }

        business_pool.append(business_record)

    return business_pool



CAMPAIGN_STATUSES: list[str] = ['draft' , 'active' , 'completed'] 



def build_campaign_pool(
        business_pool : list[dict] , 
        campaigns_per_business_range: tuple[int , int] , 
        seed : int=42 , 
    ) -> list[dict]:

    

    fake.seed_instance(seed)

    campaign_pool = []

    campaign_idx = 1 

    min_camps , max_camps = campaigns_per_business_range

    for business in business_pool :

        # Determine how many campaigns this business runs
        num_campaigns = fake.random_int(min=min_camps , max = max_camps)


        for _ in range(num_campaigns):
            campaign_id = f"CP_{campaign_idx:03d}"
            campaign_idx += 1 

            # dates : start date in 2024-2026 , duration between 14 and 90 days 

            start_date : date = fake.date_between(
                start_date=date(2024,5,5) , end_date=date(2026 , 5 , 5)
            )
            duration_days = fake.random_int(min=14 , max=90) 

            end_date : date = start_date + timedelta(days=duration_days)

    
            campaign_record = {
    
                "campaign_id"            : campaign_id , 
                "campaign_business_id"   : business["business_id"] , 
                "campaign_domain"        : business["business_domain"] , 
                "campaign_budget"        : fake.random_int(min=int(0.1*business["business_budget"]) , max = int(0.5*business["business_budget"])) ,
                "campaign_status"        : fake.random_element(CAMPAIGN_STATUSES) , 
                "campaign_start_date"    : start_date.isoformat() , 
                'campaign_end_date'      : end_date.isoformat() , 
                "campaign_creator_ids"   : [] ,
            }
    
            campaign_pool.append(campaign_record)




    return campaign_pool


def assign_creator_to_row(row: dict , creator_pool: list[dict]) -> dict: 

    '''
    Given one parsed CSV row and the full creator pool , select the creator this row/post should be attached to .

    Matching poilicy -- 
    1) exact match : crator_niche == rows's category and creator_tier == rows's tier

    2) Fallback: same niche , tier one band away (adjacent in CREATOR_TIER_BANDS order) in either direction.

    3) Final fallback : niche match only , any tier.

    4) If step 3 still yields zero candidates: raise , dont return None -- every row must land a creator , and a true zero-candidate case means something is wrong witht eh pool itself , not the row 
    
    '''
    row_category = row.get("Category" , "").strip().lower()
    row_tier = row.get("Influencer_Tier" , "").strip().lower()

    matching_creators_list: list[dict] = [
        
        creator 
        for creator in creator_pool 
        if creator["creator_niche"].strip().lower() == row_category and creator["creator_tier"].strip().lower() == row_tier
    ]

    
    if not matching_creators_list:

        creator_tiers = [ creator_tier for creator_tier , min_follower , max_follower in CREATOR_TIER_BANDS]
        
        adjacent_left_tier = adjacent_right_tier = None
        
        for i , tier in enumerate(creator_tiers) :
             if row_tier == tier.strip().lower():
                 if   i == 0 :
                    adjacent_right_tier = creator_tiers[i+1]
                    break
    
                 elif i == len(creator_tiers) - 1:
                    adjacent_left_tier = creator_tiers[i-1]
                    break
    
                 else:
                     adjacent_left_tier = creator_tiers[i-1]
                     adjacent_right_tier = creator_tiers[i+1]
    
        adjacent_tiers = [t.strip().lower() for t in (adjacent_right_tier , adjacent_left_tier) if t]
        matching_creators_list = [

            creator 

            for creator in creator_pool
            if creator["creator_niche"].strip().lower() == row_category and creator["creator_tier"].strip().lower() in adjacent_tiers
        ]

    

 

    if not matching_creators_list:
        matching_creators_list = [

            creator 

            for creator in creator_pool
            if creator["creator_niche"].strip().lower() == row_category 
        ]

    
    if not matching_creators_list:
        raise ValueError (
            f"there is no matching creator pool available for the csv_post_row , check the creator_pool for {row_category} and {row_tier}"
        )
    


    matching_creator : dict = fake.random_element(elements=matching_creators_list)

    

    return matching_creator



def assign_campaign_to_row(row: dict , campaign_pool : list[dict]) -> str | None :
    '''
    Match a CSV row to campaign by niche + status , with a two-level fallback.

    Level 1 : exact niche match , status in {active , completed}
    Level 2 : exact niche match , status == 'draft' 
    Level 3 : no match -> None (organic post , not an error)

    Unlike assign_creator_to_row , this function never raises -- a row with no campaign match is a valid , expected outcome.

    Returns : 
        campaign_id(str) if matched , else None     
    '''

    row_niche = row["Category"]


    matching_campaign_list = [

        campaign 
        for campaign in campaign_pool 
        # if campaign["campaign_domain"] == row_niche and campaign["campaign_status"] in ["active" , "completed"]

        if campaign.get("campaign_domain") == row_niche and campaign.get("campaign_status") in ["active" , "completed"]
    ]

    if not matching_campaign_list :
        matching_campaign_list = [

            campaign
            for campaign in campaign_pool
            if campaign.get("campaign_domain") == row_niche and campaign.get("campaign_status") == 'draft'
        ]

    if not matching_campaign_list :
        return None


    matching_campagin_id : str  = fake.random_element(elements=matching_campaign_list)["campaign_id"]

    return matching_campagin_id



def seed_dataset(csv_path: Path) -> list[dict] :
    '''

    Orchestrate the full Phase 3 seeding pipeline , build all pools , stream CSV rows , match each row to a creator 
    and campaign (None on failure = organic post) , mutate matched campaigns ' creator lists , and assemble the final joined records.

    Fails fast : any creator-match failure aborts the entire run and propogates the exception. No partial output is written on failure 

    Returns: 
        list[dict] -- one fully join ed record per CSV row.
    
    '''

    # Build phase 

    creator_pool = build_creator_pool ( CREATOR_NICHES , creators_per_niche=6 , seed = 42 )

    business_pool = generate_businesses(8 , seed=42)

    campaign_pool = build_campaign_pool(business_pool , (3,7) , seed=42)

    


    # Index phase 

    campaign_pool_by_id = {c["campaign_id"]: c for c in campaign_pool}


    # Ingest + Match  + Mutate + Assemble , per row 


    assembled_records : list[dict] = [] 

    for row in load_influencer_csv(csv_path):

        matched_creator = assign_creator_to_row(row , creator_pool)


        match_campaign_id = assign_campaign_to_row(row , campaign_pool)

        # pprint(match_campaign_id)
        
        # pprint(campaign_pool_by_id[match_campaign_id])

        # pprint(matched_creator)

        if match_campaign_id is not None:

            campaign = campaign_pool_by_id[match_campaign_id]
            if matched_creator["creator_id"] not in campaign["campaign_creator_ids"]:
                campaign["campaign_creator_ids"].append(matched_creator["creator_id"])

            business_id = campaign["campaign_business_id"]

        else:
            business_id = None


        assembled_record = {

            **row , 
            "creator_id" : matched_creator["creator_id"] , 
            "campaign_id" : match_campaign_id , 
            "business_id" : business_id
        }

        assembled_records.append(assembled_record)

    return {

        "businesses"       : business_pool , 
        "campaigns"        : campaign_pool  , 
        "creators"         : creator_pool , 
        "posts"            : assembled_records , 

    }



def _json_default(obj) :

    '''
    Fallback serializer passed to json.dumps default=' parameter. Called only for objects json.dump doesn't know hoe to 
    serilaize natevly (eg datetime)  Anything unexpected reaching here should be investigated, not silently stringigiled forever.
    '''

    if isinstance(obj , datetime) :
        return obj.isoformat()

    else:
        raise TypeError(
            f"Object of type {type(obj)} is not JSON serializable"
        )



def persist_seeded_dataset(data: dict , output_path: Path) -> None: 

    output_path.parent.mkdir(parents=True , exist_ok=True )
    with open(output_path , 'w' , encoding='utf-8') as f:
        json.dump(data , f , indent = 2 , default=_json_default )

    return f"data saved as json at {output_path}"



def check_referential_integrity(data: dict) -> None :

    '''
    Verify zero dangling foreign keys across the seeded dataset.

    Checks:
      - every post's creator_id exists in data["creators"]
      - every post's non-None business_id exists in data["businesses"]
      - every post's non-None campaign_id exists in data["campaigns"]
      - every id inside each campaign's campaign_creator_ids exists in data["creators"]

    None values for business_id/campaign_id are valid (organic posts) —
    NOT treated as violations.

    Raises:
        ValueError, with the specific offending id and which post/campaign
        it came from, on the first violation found.
    
    '''

    creators_pool_id  = { creator["creator_id"] : creator  for creator in data["creators"] }

    campaign_pool_id = { campaign["campaign_id"] : campaign for campaign in data["campaigns"]}

    business_pool_id = {  business["business_id"] : business for business in data["businesses"]}

    for post in data["posts"] : 

      if post["creator_id"] not in creators_pool_id :
          raise ValueError(
              f"{post['creator_id']} is not present in creator pool"
          )

      if post["campaign_id"]: 
          if post["campaign_id"] not in campaign_pool_id :
              raise ValueError(
                  f"{post['campaign_id']} does not exist in the campaingn"
              )

      if post["business_id"]:
          if post["business_id"] not in business_pool_id:
            raise ValueError (
                f"{post['business_id']} is not present in business pool"
            )

    for campaign in data["campaigns"]:

        if not campaign["campaign_creator_ids"] :
            continue

        for campaign_creator_id in campaign["campaign_creator_ids"] :
            if campaign_creator_id not in creators_pool_id :
                raise ValueError (
                    f"{campaign_creator_id} is not present in creator pool"
                )

    return f"integrity check passed: {len(data['posts'])} posts , {len(data['campaigns'])} campaigns checked"
          




    




if __name__ == "__main__" : 

    result = seed_dataset(CSV_PATH)

    print(persist_seeded_dataset(result , JSON_OUTPUT_PATH))

    print(check_referential_integrity(result))

    

#     raw_row = {'Post_ID': 'POST_04552', 'Timestamp': datetime(2024, 1, 1, 1, 42), 'Platform': 'Instagram', 'Content_Type': 'Carousel', 'Category': 'Business', 'Likes': 8287, 'Comments': 247, 'Shares': 51, 'Views': 29502, 'Saves': 20, 'Follower_Count': 223080, 'Engagement_Rate': 3.85, 'Hour_of_Day': 1, 'Day_of_Week': 'Monday', 'Hashtag_Count': 16, 'Content_Length': 985, 'Sentiment': 'Positive', 'Influencer_Tier': 'Macro', 'Has_Media': True, 'Is_Verified': False}
#     creator_pool =  build_creator_pool(CREATOR_NICHES , 6 , 42 )
#     business_pool = generate_businesses(5 , seed=42)
#     campaign_pool   = build_campaign_pool(business_pool , (4 , 8) , seed =42)

# #    pprint(business_pool)
#     pprint(campaign_pool)

#     result = assign_creator_to_row(raw_row , creator_pool)
#     result1 = assign_campaign_to_row(raw_row , campaign_pool)
#     pprint(result1)








           

        

    





    








