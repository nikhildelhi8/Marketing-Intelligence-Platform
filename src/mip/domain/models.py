from dataclasses import dataclass , field
from mip.domain.enums import Platform , Content_type , Category , Creator_Tier , Campaign_Status



# {
#       "business_id": "BS_001",
#       "business_name": "Rodriguez, Figueroa and Sanchez",
#       "business_domain": "Entertainment",
#       "business_budget": 140000
# }



@dataclass(frozen=True)
class Business:

    business_id : str 
    business_name : str 
    business_domain : Category 
    business_budget : int


# {
#       "campaign_id": "CP_001",
#       "campaign_business_id": "BS_001",
#       "campaign_domain": "Entertainment",
#       "campaign_budget": 30049,
#       "campaign_status": "draft",
#       "campaign_start_date": "2024-05-23",
#       "campaign_end_date": "2024-07-11",
#       "campaign_creator_ids": []
# }


@dataclass
class Campaign:
    campaign_id : str 
    campaign_business_id : str 
    campaign_domain : Category
    campaign_budget : int 
    campaign_status  : Campaign_Status
    campaign_start_date : str 
    campaign_end_date : str 
    campaign_creator_ids : list[str] = field(default_factory=list)

    def __post_init__(self) :

        if self.campaign_start_date > self.campaign_end_date :
            raise ValueError(f" campaign start date {self.campaign_start_date} cannot be after the campaign end dates {self.campaign_end_date}")







# {
#       "creator_id": "CR_012",
#       "creator_name": "Patty Perez",
#       "creator_bio": "Education creator passinate about building a community of passionate enthusiasts",
#       "creator_niche": "Education",
#       "creator_tier": "Micro",
#       "creator_follower_count": 12104
# }


@dataclass(frozen=True)
class Creator:

    creator_id : str 
    creator_name : str 
    creator_bio : str 
    creator_niche : Category
    creator_tier : Creator_Tier
    creator_follower_count : int 


# {
#       "Post_ID": "POST_02656",
#       "Timestamp": "2024-01-02T03:01:00",
#       "Platform": "Twitter",
#       "Content_Type": "Poll",
#       "Category": "Lifestyle",
#       "Likes": 1558,
#       "Comments": 71,
#       "Shares": 676,
#       "Views": 45929,
#       "Saves": 92,
#       "Follower_Count": 259275,
#       "Engagement_Rate": 0.89,
#       "Hour_of_Day": 3,
#       "Day_of_Week": "Tuesday",
#       "Hashtag_Count": 25,
#       "Content_Length": 1406,
#       "Sentiment": "Negative",
#       "Influencer_Tier": "Macro",
#       "Has_Media": true,
#       "Is_Verified": false,
#       "creator_id": "CR_054",
#       "campaign_id": null,
#       "business_id": null
# }


@dataclass(frozen=True)
class SocialPost :

    post_id : str 
    timestamp : str 
    platform : Platform
    content_type: Content_type
    category : Category
    likes  : int 
    comments : int 
    shares : int 
    views : int 
    saves : int 
    follower_count : int 
    engagement_rate : float 
    hour_of_day : int 
    day_of_week : str 
    hashtag_count : int 
    content_length : int 
    sentiment : str 
    influencer_tier : Creator_Tier
    has_media : bool 
    is_verified : bool
    creator_id : str 
    campaign_id : str| None
    business_id : str| None



@dataclass(frozen=True)

class CampaignAnalytics :

    campaign_id : str 
    total_posts_attached_to_campaign: int 
    total_views: int 
    total_likes : int 
    total_comments : int 
    total_shares : int 
    total_saves : int 
    avg_engagement_rate : float 

    def __post_init__(self) :

        field_lists = [ self.total_saves , self.total_shares , self.total_comments , self.total_likes , self.total_views , self.total_posts_attached_to_campaign]

        negative_fields = [ field for field in field_lists if field < 0.0 ]

        if negative_fields :
            raise ValueError (
                f"Negative data found for {negative_fields}"
            )










