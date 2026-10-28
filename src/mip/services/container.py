
from pathlib import Path

from mip.repositories.factories import (
    build_business_in_json,
    build_campaign_analytics_in_json,
    build_campaign_in_json,
    build_creator_in_json,
    build_social_post_in_json,
)
from mip.services.analytics_service import AnalyticsService
from mip.services.business_service import BusinessService
from mip.services.campaign_service import CampaignService
from mip.services.creator_service import CreatorService

repository_file_path = Path(__file__).parents[3] / "data" / "repo"


class ContainerServices:
    def __init__(self) -> None:
        self._business_repo = build_business_in_json(
            repository_file_path / "businesses.json"
        )
        self._campaign_repo = build_campaign_in_json(
            repository_file_path / "campaigns.json"
        )
        self._creator_repo = build_creator_in_json(
            repository_file_path / "creators.json"
        )
        self._campaign_analytics_repo = build_campaign_analytics_in_json(
            repository_file_path / "campaign_analytics.json"
        )
        self._social_post_repo = build_social_post_in_json(
            repository_file_path / "social_post.json"
        )

        self.business_service = BusinessService(
            self._business_repo,
            self._campaign_repo,
        )
        self.campaign_service = CampaignService(
            self._business_repo,
            self._campaign_repo,
            self._creator_repo,
            self._social_post_repo,
        )
        self.creator_service = CreatorService(
            self._creator_repo,
            self._campaign_repo,
            self._social_post_repo,
        )
        self.analytics_service = AnalyticsService(
            self._campaign_repo,
            self._social_post_repo,
            self._campaign_analytics_repo,
        )

