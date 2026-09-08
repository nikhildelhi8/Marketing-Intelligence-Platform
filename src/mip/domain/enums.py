from enum import Enum




class Platform(str , Enum):

    FACEBOOK = 'Facebook'
    INSTAGRAM = 'Instagram'
    LINKEDIN = 'Linkedin'
    TIKTOK = 'Tiktok'
    TWITTER = 'Twitter'
    YOUTUBE = 'YouTube'


class ContentType(str , Enum) :

    ARTICLE = 'Article'
    CAROUSEL = 'Carousel'
    COMMUNITY_POST = 'Community_post'
    DOCUMENT = 'Document'
    DUET = 'Duet'
    LIVE = 'Live'
    PHOTO = 'Photo'
    POLL = 'Poll'
    POST = 'Post'
    RETWEET = 'Retweet'
    SHORT = 'Short'
    STITCH = 'Stitch'
    STORY = 'Story'
    THREAD = 'Thread'
    TWEET  = 'Tweet'
    VIDEO = 'Video'




# CREATOR_NICHES : list[str] = ['Business','Education','Entertainment','Fashion','Fitness','Food','Gaming','Health','Lifestyle','Sports','Technology','Travel']


class Category(str , Enum) : 

    BUSINESS = 'Business'
    EDUCATION = 'Education'
    ENTERTAINMENT = 'Entertainment'
    FASHION = 'Fashion'
    FITNESS = 'Fitness'
    FOOD = 'Food'
    GAMING = 'Gaming'
    HEALTH = 'Health'
    LIFESTYLE = 'Lifestyle'
    SPORTS = 'Sports'
    TECHNOLOGY = 'Technology'
    TRAVEL = 'Travel'



# CREATOR_TIER_BANDS : list[tuple[str , int , int]] = [

#     ('Nano' , 500, 10000) , 
#     ('Micro', 10001 , 50000) , 
#     ('Mid-tier' , 50001 , 100000) , 
#     ('Macro' , 100001 , 500000 )
# ]


class CreatorTier(str , Enum) :

    NANO = 'Nano'
    MICRO = 'Micro'
    MID_TIER = 'Mid-tier'
    MACRO = 'Macro'


# CAMPAIGN_STATUSES: list[str] = ['draft' , 'active' , 'completed'] 


class CampaignStatus(str, Enum) :

    DRAFT = 'draft'
    ACTIVE = 'active'
    COMPLETED  = 'completed'








