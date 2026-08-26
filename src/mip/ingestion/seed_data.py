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
'''


from faker import Faker
from faker.providers import DynamicProvider
from datetime import date , datetime



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



CAMPAIGN_STATUSES: list[str] = ['draft' , 'active' , 'completed' , 'cancelled'] 



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
    1) exact match : crator_niche == rows's category and creator_tier == rows's tier(derived via get_tier on the rows follwer count).

    2) Fallback: same niche , tier one band away (adjacent in CREATOR_TIER_BANDS order) in either direction.

    3) Final fallback : niche match only , any tier.

    4) If step 3 still yields zero candidates: raise , dont return None -- every row must land a creator , and a true zero-candidate case means something is wrong witht eh pool itself , not the row 
    
    '''
    row_category = row.get("Category" , "").strip().lower()
    row_tier = row.get("Influencer_Tier" , "").strip().lower()

    matching_creators_list: list[dict] = [

        creator 
        for creator in creator_pool 
        if creator.get("creator_niche" , creator.get("niche" , "")).strip().lower() == row_category and creator.get("creator_tier" , creator.get("tier" , "")).strip().lower() == row_tier
    ]

    


    matching_creator : dict = fake.random_element(matching_creators_list)

    

    return matching_creator





if __name__ == "__main__" : 

    raw_row = {'Post_ID': 'POST_04552', 'Timestamp': datetime(2024, 1, 1, 1, 42), 'Platform': 'Instagram', 'Content_Type': 'Carousel', 'Category': 'Business', 'Likes': 8287, 'Comments': 247, 'Shares': 51, 'Views': 29502, 'Saves': 20, 'Follower_Count': 223080, 'Engagement_Rate': 3.85, 'Hour_of_Day': 1, 'Day_of_Week': 'Monday', 'Hashtag_Count': 16, 'Content_Length': 985, 'Sentiment': 'Positive', 'Influencer_Tier': 'Macro', 'Has_Media': True, 'Is_Verified': False}
    creator_pool =  build_creator_pool(CREATOR_NICHES , 6 , 42 )
#    business_pool = generate_businesses(5 , seed=42)
#    campaign_pool   = build_campaign_pool(business_pool , (4 , 8) , seed =42)
#    print(business_pool)
#    print(campaign_pool)

    result = assign_creator_to_row(raw_row , creator_pool)
    print(result)







           

        

    





    








