from typing import Protocol

from mip.domain.models import Campaign, CampaignAnalytics, SocialPost


class CampaignRepository(Protocol):
    def get_or_raise(self, entity_id: str) -> Campaign: ...


class SocialPostRepository(Protocol):
    def list(self) -> list[SocialPost]: ...


class CampaignAnalyticsRepository(Protocol):
    def add(self, entity: CampaignAnalytics) -> None: ...

    def get(self, entity_id: str) -> CampaignAnalytics | None: ...

    def update(self, entity: CampaignAnalytics) -> None: ...


class AnalyticsService:
    def __init__(
        self,
        campaign_repo: CampaignRepository,
        social_post_repo: SocialPostRepository,
        analytics_repo: CampaignAnalyticsRepository,
    ) -> None:
        self._campaign_repo = campaign_repo
        self._social_post_repo = social_post_repo
        self._analytics_repo = analytics_repo

    def calculate_campaign_analytics(self, campaign_id: str) -> CampaignAnalytics:
        
        self._campaign_repo.get_or_raise(campaign_id)
        campaign_posts = [
            post
            for post in self._social_post_repo.list()
            if post.campaign_id == campaign_id
        ]

        post_count = len(campaign_posts)
        analytics = CampaignAnalytics(
            campaign_id=campaign_id,
            total_posts_attached_to_campaign=post_count,
            total_views=sum(post.views for post in campaign_posts),
            total_likes=sum(post.likes for post in campaign_posts),
            total_comments=sum(post.comments for post in campaign_posts),
            total_shares=sum(post.shares for post in campaign_posts),
            total_saves=sum(post.saves for post in campaign_posts),
            avg_engagement_rate=(
                sum(post.engagement_rate for post in campaign_posts) / post_count
                if post_count
                else 0.0
            ),
        )

        existing_analytics = self._analytics_repo.get(campaign_id)
        if existing_analytics is None:
            self._analytics_repo.add(analytics)
        else:
            self._analytics_repo.update(analytics)

        return analytics