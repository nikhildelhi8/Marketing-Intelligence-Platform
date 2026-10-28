from datetime import datetime

from pydantic import BaseModel

from mip.domain.enums import (
    Category,
    CampaignStatus,
    CreatorTier,
    Platform,
    ContentType,
)
from mip.schemas.shared_validators import PositiveBudget , PositiveFollowerCount



class CreateBusinessDTO(BaseModel):

    business_name : str 
    business_domain : Category 
    business_budget : PositiveBudget


class CreateCampaignDTO(BaseModel) :
    campaign_business_id: str
    campaign_domain: Category
    campaign_budget: PositiveBudget
    campaign_status: CampaignStatus
    campaign_start_date: str
    campaign_end_date: str
    campaign_creator_ids: list[str]


class CreateCreatorDTO(BaseModel):
    creator_name: str
    creator_bio: str
    creator_niche: Category
    creator_tier: CreatorTier
    creator_follower_count: PositiveFollowerCount

class CreateSocialPostDTO(BaseModel):
    timestamp: datetime | None
    platform: Platform
    content_type: ContentType
    category: Category
    likes: int
    comments: int
    shares: int
    views: int
    saves: int
    follower_count: int
    engagement_rate: float
    hour_of_day: int
    day_of_week: str
    hashtag_count: int
    content_length: int
    sentiment: str
    influencer_tier: CreatorTier
    has_media: bool
    is_verified: bool



    