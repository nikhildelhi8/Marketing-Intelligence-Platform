import pytest

from mip.domain.enums import CampaignStatus, Category, ContentType, CreatorTier, Platform
from mip.domain.models import Campaign, CampaignAnalytics, SocialPost
from mip.exceptions import NotFoundError
from mip.repositories.factories import build_campaign_analytics_in_json
from mip.repositories.in_memory import InMemoryRepo
from mip.services.analytics_service import AnalyticsService


def make_campaign(campaign_id: str = "CP_01") -> Campaign:
    return Campaign(
        campaign_id=campaign_id,
        campaign_business_id="BS_01",
        campaign_domain=Category.FASHION,
        campaign_budget=20_000,
        campaign_status=CampaignStatus.ACTIVE,
        campaign_start_date="2030-01-01",
        campaign_end_date="2030-02-01",
    )


def make_post(
    post_id: str,
    campaign_id: str | None,
    *,
    views: int,
    likes: int,
    comments: int,
    shares: int,
    saves: int,
    engagement_rate: float,
) -> SocialPost:
    return SocialPost(
        post_id=post_id,
        timestamp="2025-01-01T10:00:00",
        platform=Platform.INSTAGRAM,
        content_type=ContentType.PHOTO,
        category=Category.FASHION,
        likes=likes,
        comments=comments,
        shares=shares,
        views=views,
        saves=saves,
        follower_count=100,
        engagement_rate=engagement_rate,
        hour_of_day=10,
        day_of_week="Wednesday",
        hashtag_count=1,
        content_length=100,
        sentiment="Positive",
        influencer_tier=CreatorTier.MICRO,
        has_media=True,
        is_verified=False,
        creator_id="CR_01",
        campaign_id=campaign_id,
        business_id="BS_01",
    )


@pytest.fixture
def analytics_context():
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    analytics_repo = InMemoryRepo(get_id=lambda result: result.campaign_id)
    campaign_repo.add(make_campaign())
    service = AnalyticsService(campaign_repo, post_repo, analytics_repo)
    return service, post_repo, analytics_repo


def test_calculate_and_store_campaign_analytics(analytics_context) -> None:
    service, post_repo, analytics_repo = analytics_context
    post_repo.add(
        make_post(
            "POST_01",
            "CP_01",
            views=100,
            likes=10,
            comments=2,
            shares=3,
            saves=4,
            engagement_rate=1.5,
        )
    )
    post_repo.add(
        make_post(
            "POST_02",
            "CP_01",
            views=300,
            likes=20,
            comments=6,
            shares=7,
            saves=8,
            engagement_rate=2.5,
        )
    )
    post_repo.add(
        make_post(
            "POST_OTHER",
            "CP_OTHER",
            views=999,
            likes=999,
            comments=999,
            shares=999,
            saves=999,
            engagement_rate=99.0,
        )
    )

    result = service.calculate_campaign_analytics("CP_01")

    assert result == CampaignAnalytics(
        campaign_id="CP_01",
        total_posts_attached_to_campaign=2,
        total_views=400,
        total_likes=30,
        total_comments=8,
        total_shares=10,
        total_saves=12,
        avg_engagement_rate=2.0,
    )
    assert analytics_repo.get("CP_01") == result


def test_calculate_analytics_with_no_posts_returns_zero_metrics(
    analytics_context,
) -> None:
    service, _, analytics_repo = analytics_context

    result = service.calculate_campaign_analytics("CP_01")

    assert result.total_posts_attached_to_campaign == 0
    assert result.total_views == 0
    assert result.avg_engagement_rate == 0.0
    assert analytics_repo.get("CP_01") == result


def test_recalculating_updates_existing_analytics(analytics_context) -> None:
    service, post_repo, analytics_repo = analytics_context
    analytics_repo.add(
        CampaignAnalytics(
            campaign_id="CP_01",
            total_posts_attached_to_campaign=0,
            total_views=0,
            total_likes=0,
            total_comments=0,
            total_shares=0,
            total_saves=0,
            avg_engagement_rate=0.0,
        )
    )
    post_repo.add(
        make_post(
            "POST_01",
            "CP_01",
            views=10,
            likes=2,
            comments=1,
            shares=1,
            saves=1,
            engagement_rate=2.0,
        )
    )

    result = service.calculate_campaign_analytics("CP_01")

    assert result.total_views == 10
    assert analytics_repo.get("CP_01") == result
    assert len(analytics_repo.list()) == 1


def test_calculating_analytics_for_unknown_campaign_raises(
    analytics_context,
) -> None:
    service, _, analytics_repo = analytics_context

    with pytest.raises(NotFoundError):
        service.calculate_campaign_analytics("missing")

    assert analytics_repo.list() == []


def test_json_analytics_repository_loads_serialized_record(tmp_path) -> None:
    path = tmp_path / "campaign_analytics.json"
    repository = build_campaign_analytics_in_json(path)
    expected = CampaignAnalytics(
        campaign_id="CP_01",
        total_posts_attached_to_campaign=2,
        total_views=400,
        total_likes=30,
        total_comments=8,
        total_shares=10,
        total_saves=12,
        avg_engagement_rate=2.0,
    )
    repository.add(expected)

    reloaded_repository = build_campaign_analytics_in_json(path)

    assert reloaded_repository.get("CP_01") == expected
