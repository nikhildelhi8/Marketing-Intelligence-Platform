from dataclasses import dataclass , field  , asdict
from mip.domain.enums import Platform , ContentType , Category , CreatorTier , CampaignStatus
from mip import PROJECT_ROOT
import json
from pprint import pprint




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

    def __post_init__(self):

        if self.business_budget < 0 :
            raise ValueError(
                f"Budget cannot be less than 0 , current value is {self.business_budget}"
            )
   
    @classmethod
    def from_dict(cls , data: dict) -> "Business" :

        return cls (
            business_id = data["business_id"] , 
            business_name = data["business_name"] , 
            business_domain = Category(data["business_domain"]) , 
            business_budget = data["business_budget"]
        )

    
    def to_dict(self)-> dict :

        return {
            "business_id" : self.business_id , 
            "business_name" : self.business_name , 
            "business_domain" : self.business_domain.value , 
            "business_budget" : self.business_budget
        }


# {
#       "campaign_id": "CP_001",
#       "campaign_business_id": "BS_001",
#       "campaign_domain": "Entertainment",
#       "campaign_budget": 30049,
#       "CampaignStatus": "draft",
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
    campaign_status  : CampaignStatus
    campaign_start_date : str 
    campaign_end_date : str 
    campaign_creator_ids : list[str] = field(default_factory=list)

    def __post_init__(self) :

        if self.campaign_start_date > self.campaign_end_date :
            raise ValueError(f" campaign start date {self.campaign_start_date} cannot be after the campaign end dates {self.campaign_end_date}")


    @classmethod
    def from_dict(cls , data:dict) -> "Campaign" :

        return cls (

            campaign_id = data["campaign_id"] , 
            campaign_business_id = data["campaign_business_id"] , 
            campaign_domain = Category(data["campaign_domain"]) , 
            campaign_budget = data["campaign_budget"] , 
            campaign_status = CampaignStatus(data["campaign_status"]) , 
            campaign_start_date = data["campaign_start_date"] , 
            campaign_end_date = data["campaign_end_date"] , 
            campaign_creator_ids = data["campaign_creator_ids"]
        )

    def to_dict(self) -> dict :
        return {

            "campaign_id"  : self.campaign_id , 
            "campaign_business_id" : self.campaign_business_id , 
            "campaign_domain" : self.campaign_domain.value , 
            "campaign_budget" : self.campaign_budget  , 
            "campaign_status" : self.campaign_status.value , 
            "campaign_start_date" : self.campaign_start_date , 
            "campaign_end_date" : self.campaign_end_date , 
            "campaign_creator_ids" : self.campaign_creator_ids

        }





# {
#       "creator_id": "CR_012",
#       "creator_name": "Patty Perez",
#       "creator_bio": "Education creator passinate about building a community of passionate enthusiasts",
#       "creator_niche": "Education",
#       "CreatorTier": "Micro",
#       "creator_follower_count": 12104
# }


@dataclass(frozen=True)
class Creator:

    creator_id : str 
    creator_name : str 
    creator_bio : str 
    creator_niche : Category
    creator_tier : CreatorTier
    creator_follower_count : int 

    def __post_init__(self) :
        if self.creator_follower_count < 0 :
            raise ValueError(
                f"Creator follower Count cannot be less than 0 , currently it is {self.creator_follower_count}"
            )

    @classmethod
    def from_dict(cls , data: dict) -> "Creator" :

        return cls (

            creator_id = data["creator_id"] , 
            creator_name = data["creator_name"] , 
            creator_bio = data["creator_bio"] , 
            creator_niche = Category(data["creator_niche"]) , 
            creator_tier = CreatorTier(data["creator_tier"]) , 
            creator_follower_count = data["creator_follower_count"]
        )

    def to_dict(self) -> dict : 

        return {
            "creator_id" : self.creator_id , 
            "creator_name" : self.creator_name , 
            "creator_bio" : self.creator_bio , 
            "creator_niche" : self.creator_niche.value , 
            "creator_tier" : self.creator_tier.value , 
            "creator_follower_count" : self.creator_follower_count
        }


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
    content_type: ContentType
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
    influencer_tier : CreatorTier
    has_media : bool 
    is_verified : bool
    creator_id : str 
    campaign_id : str| None
    business_id : str| None

    def __post_init__(self) :

        post_data = asdict(self)

        negative_post_data = {k : v for k , v in post_data.items() if isinstance(v , (int , float)) and v < 0}

        if negative_post_data:
            raise ValueError(
                f"Post data cannot contain negative value , check the data again for -- {negative_post_data}"
            )


    @classmethod
    def from_dict(cls , data : dict) -> "SocialPost" :

        return cls (

            post_id = data["post_id"] , 
            timestamp = data["timestamp"] , 
            platform = Platform(data["platform"] ), 
            content_type = ContentType(data["content_type"]) , 
            category = Category(data["category"]) , 
            likes = data["likes"] , 
            comments = data["comments"] , 
            shares = data["shares"] , 
            views = data["views"] , 
            saves = data["saves"] , 
            follower_count = data["follower_count"] , 
            engagement_rate = data["engagement_rate"] , 
            hour_of_day = data["hour_of_day"] , 
            day_of_week = data["day_of_week"] , 
            hashtag_count = data["hashtag_count"] , 
            content_length = data["content_length"] , 
            sentiment = data["sentiment"] , 
            influencer_tier = CreatorTier(data["influencer_tier"]) , 
            has_media = data["has_media"]   , 
            is_verified = data["is_verified"] , 
            creator_id = data["creator_id"]  , 
            campaign_id = data["campaign_id"]  , 
            business_id = data["business_id"]
        )

    def to_dict(self) -> dict:
        return {
            "post_id": self.post_id,
            "timestamp": self.timestamp,
            "platform": self.platform.value,
            "content_type": self.content_type.value,
            "category": self.category.value,
            "likes": self.likes,
            "comments": self.comments,
            "shares": self.shares,
            "views": self.views,
            "saves": self.saves,
            "follower_count": self.follower_count,
            "engagement_rate": self.engagement_rate,
            "hour_of_day": self.hour_of_day,
            "day_of_week": self.day_of_week,
            "hashtag_count": self.hashtag_count,
            "content_length": self.content_length,
            "sentiment": self.sentiment,
            "influencer_tier": self.influencer_tier.value,
            "has_media": self.has_media,
            "is_verified": self.is_verified,
            "creator_id": self.creator_id,
            "campaign_id": self.campaign_id,
            "business_id": self.business_id,
        }


        

    



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

        metric_data = asdict(self)

        negative_metrics = {k : v for k , v in metric_data.items() if isinstance(v , (int , float)) and v < 0}

        if negative_metrics:
            raise ValueError(
                        f" Metrics cannot contain negative value , check the data again -- {negative_metrics}"
                    )

    def to_dict(self) -> dict:
        return {
            "campaign_id": self.campaign_id,
            "total_posts_attached_to_campaign": self.total_posts_attached_to_campaign,
            "total_views": self.total_views,
            "total_likes": self.total_likes,
            "total_comments": self.total_comments,
            "total_shares": self.total_shares,
            "total_saves": self.total_saves,
            "avg_engagement_rate": self.avg_engagement_rate,
        }








 










    
            

        














