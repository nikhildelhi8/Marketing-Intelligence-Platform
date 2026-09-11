from pydantic import BaseModel , field_validator
from mip.domain.enums import Platform , ContentType , CampaignStatus , Category , CreatorTier
from mip.exceptions import ValidationError , RepositoryError , NotFoundError , MIPError


#  {
#       "business_id": "BS_001",
#       "business_name": "Rodriguez, Figueroa and Sanchez",
#       "business_domain": "Entertainment",
#       "business_budget": 140000
# }


data = {
      "business_id": "BS_002",
      "business_name": "Yang, Gardner and Garza",
      "business_domain": "Business",
      "business_budget": -87
    }

class BusinessSchema(BaseModel):

    business_id : str 
    business_name : str 
    business_domain : Category
    business_budget : int 


    @field_validator("business_budget")
    @classmethod
    def budget_non_negative(cls , business_budget):

        if business_budget<=0 :
            raise ValidationError(f"business_budget cannot be negative number currently {business_budget}")

        return business_budget




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
    campaign_budget : int 
    campaign_status : CampaignStatus 
    campaign_start_date : str 
    campaign_end_date : str 
    campaign_creator_ids : list[str]

    @field_validator("campaign_budget")
    @classmethod
    def non_negative_campaign_budget(cls , campaign_budget):

        if campaign_budget <= 0 :
            raise ValidationError(f"campaign_budget cannot be a negative value , currently {campaign_budget}")
        
        return campaign_budget




#  {
#       "creator_id": "CR_001",
#       "creator_name": "Danielle Taylor",
#       "creator_bio": "Business creator passinate about sharing daily insights and tips",
#       "creator_niche": "Business",
#       "creator_tier": "Nano",
#       "creator_follower_count": 2179
# }


class CreatorShema(BaseModel) :

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

    post_id : str
    timestamp : str 
    platform : Platform
    content_type : ContentType 
    category : Category
    likes : int 
    comments : int 
    shares : int 
    views : int 
    saves : int 
    follower_count : int 
    engagemenet_rate : float 
    hour_of_day : int 
    day_of_week : str 
    hashtag_count : int 
    content_length : int 
    sentiment : str 
    influencer_tier : CreatorTier 
    has_media : int 
    is_verified: bool 
    creator_id : str 
    campaign_id : str | None 
    business_id : str | None


    








   

    

