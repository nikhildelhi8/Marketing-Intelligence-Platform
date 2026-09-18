from pydantic import BaseModel , field_validator , ValidationError as PydanticValidationError  , Field
from mip.domain.enums import Platform , ContentType , CampaignStatus , Category , CreatorTier
from mip.schemas.shared_validators import PositiveBudget







#  {
#       "business_id": "BS_001",
#       "business_name": "Rodriguez, Figueroa and Sanchez",
#       "business_domain": "Entertainment",
#       "business_budget": 140000
# }


class BusinessSchema(BaseModel):

    business_id : str 
    business_name : str 
    business_domain : Category
    business_budget : PositiveBudget 


# {
#       "campaign_id": "CP_002",
#       "campaign_business_id": "BS_001",
#       "campaign_domain": "Entertainment",
#       "campaign_budget": 58348,
#       "campaign_status": "completed",
#       "campaign_start_date": "2024-08-14",
#       "campaign_end_date": "2024-09-10",
#       "campaign_creator_ids": [
#         "CR_016",
#         "CR_017",
#         "CR_015",
#         "CR_018",
#         "CR_013",
#         "CR_014"
#       ]
# }

class CampaignSchema(BaseModel):


    campaign_id : str 
    campaign_business_id : str    
    campaign_domain : Category
    campaign_budget : PositiveBudget 
    campaign_status : CampaignStatus 
    campaign_start_date : str 
    campaign_end_date : str 
    campaign_creator_ids : list[str]




#  {
#       "creator_id": "CR_001",
#       "creator_name": "Danielle Taylor",
#       "creator_bio": "Business creator passinate about sharing daily insights and tips",
#       "creator_niche": "Business",
#       "creator_tier": "Nano",
#       "creator_follower_count": 2179
# }


class CreatorSchema(BaseModel) :

    creator_id : str 
    creator_name : str 
    creator_bio : str 
    creator_niche : Category
    creator_tier : CreatorTier
    creator_follower_count : int 


    @field_validator("creator_follower_count")
    @classmethod
    def non_negative_follower_count(cls , creator_follower_count ):

        if creator_follower_count<0 :
            raise ValueError(f"Creator follower count cannot be less than 0 , currently : {creator_follower_count}")

        return creator_follower_count

    

# {
#       "Post_ID": "POST_02171",
#       "Timestamp": "2024-01-01T05:05:00",
#       "Platform": "LinkedIn",
#       "Content_Type": "Document",
#       "Category": "Health",
#       "Likes": 1711,
#       "Comments": 27,
#       "Shares": 247,
#       "Views": 24538,
#       "Saves": 139,
#       "Follower_Count": 312647,
#       "Engagement_Rate": 0.63,
#       "Hour_of_Day": 5,
#       "Day_of_Week": "Monday",
#       "Hashtag_Count": 9,
#       "Content_Length": 627,
#       "Sentiment": "Negative",
#       "Influencer_Tier": "Macro",
#       "Has_Media": false,
#       "Is_Verified": true,
#       "creator_id": "CR_046",
#       "campaign_id": null,
#       "business_id": null
# }

class SocialPostSchema(BaseModel) :

    post_id : str = Field(alias = "Post_ID")
    timestamp : str = Field(alias = "Timestamp")
    platform : Platform =  Field(alias= "Platform")
    content_type : ContentType = Field(alias = "Content_Type") 
    category : Category = Field(alias = "Category")
    likes : int = Field(alias  = "Likes")
    comments : int  = Field(alias = "Comments")
    shares : int  = Field(alias = "Shares")
    views : int  = Field(alias = "Views")
    saves : int  = Field(alias = "Saves")
    follower_count : int  = Field(alias = "Follower_Count")
    engagement_rate : float  = Field(alias = "Engagement_Rate")
    hour_of_day : int  = Field(alias = "Hour_of_Day")
    day_of_week : str = Field(alias = "Day_of_Week")
    hashtag_count : int = Field(alias = "Hashtag_Count")
    content_length : int = Field(alias = "Content_Length")
    sentiment : str  = Field(alias = "Sentiment")
    influencer_tier : CreatorTier = Field(alias = "Influencer_Tier") 
    has_media : bool = Field(alias = "Has_Media") 
    is_verified: bool = Field(alias = "Is_Verified")
    creator_id : str 
    campaign_id : str | None 
    business_id : str | None












   

    

