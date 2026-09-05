from enum import Enum




class Platform(str , Enum):

    FACEBOOK = 'Facebook'
    INSTAGRAM = 'Instagram'
    LINKEDIN = 'Linkedin'
    TIKTOK = 'Tiktok'
    TWITTER = 'Twitter'
    YOUTUBE = 'Youtube'


class ContentType(str , Enum) :

    ARTICLE = 'article'
    CAROUSEL = 'carousel'
    COMMUNITY_POST = 'community_post'
    DOCUMENT = 'document'
    DUET = 'duet'
    LIVE = 'live'
    PHOTO = 'photo'
    POLL = 'poll'
    POST = 'post'
    RETWEET = 'retweet'
    SHORT = 'short'
    STITCH = 'stitch'
    STORY = 'story'
    THREAD = 'thread'
    TWEET  = 'tweet'
    VIDEO = 'video'




# CREATOR_NICHES : list[str] = ['Business','Education','Entertainment','Fashion','Fitness','Food','Gaming','Health','Lifestyle','Sports','Technology','Travel']


class Category(str , Enum) : 

    BUSINESS = 'business'
    EDUCATION = 'education'
    ENTERTAINMENT = 'entertainment'
    FASHION = 'fashion'
    FITNESS = 'fitness'
    FOOD = 'food'
    GAMING = 'gaming'
    HEALTH = 'health'
    LIFESTYLE = 'lifestyle'
    SPORTS = 'sports'
    TECHNOLOGY = 'technology'
    TRAVEL = 'travel'



# CREATOR_TIER_BANDS : list[tuple[str , int , int]] = [

#     ('Nano' , 500, 10000) , 
#     ('Micro', 10001 , 50000) , 
#     ('Mid-tier' , 50001 , 100000) , 
#     ('Macro' , 100001 , 500000 )
# ]


class CreatorTier(str , Enum) :

    NANO = 'nano'
    MICRO = 'micro'
    MID_TIER = 'mid_tier'
    MACRO = 'macro'


# CAMPAIGN_STATUSES: list[str] = ['draft' , 'active' , 'completed'] 


class CampaignStatus(str, Enum) :

    DRAFT = 'draft'
    ACTIVE = 'active'
    COMPLETED  = 'completed'








