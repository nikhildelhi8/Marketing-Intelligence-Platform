from datetime import datetime, timedelta

import pytest

from mip.domain.enums import CampaignStatus, Category, ContentType, CreatorTier, Platform
from mip.domain.models import Business, Creator, SocialPost
from mip.exceptions import BusinessRuleError, NotFoundError
from mip.repositories.in_memory import InMemoryRepo
from mip.schemas.dto import CreateCampaignDTO
from mip.services.campaign_service import CampaignService


@pytest.fixture
def campaign_context():
    business_repo = InMemoryRepo(get_id=lambda business: business.business_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    business_repo.add(
        Business(
            business_id="BS_01",
            business_name="Example",
            business_domain=Category.FASHION,
            business_budget=100_000,
        )
    )
    creator_repo.add(
        Creator(
            creator_id="CR_01",
            creator_name="Creator",
            creator_bio="Bio",
            creator_niche=Category.FASHION,
            creator_tier=CreatorTier.MICRO,
            creator_follower_count=12_000,
        )
    )
    service = CampaignService(business_repo, campaign_repo, creator_repo, post_repo)
    return service, campaign_repo, post_repo


def make_request(**overrides) -> CreateCampaignDTO:
    start = datetime.now().astimezone().date() + timedelta(days=3)
    values = {
        "campaign_business_id": "BS_01",
        "campaign_domain": Category.FASHION,
        "campaign_budget": 20_000,
        "campaign_status": CampaignStatus.DRAFT,
        "campaign_start_date": start.isoformat(),
        "campaign_end_date": (start + timedelta(days=14)).isoformat(),
        "campaign_creator_ids": ["CR_01"],
    }
    values.update(overrides)
    return CreateCampaignDTO(**values)


def make_post(campaign_id: str) -> SocialPost:
    return SocialPost(
        post_id="POST_01",
        timestamp="2025-01-01T10:00:00",
        platform=Platform.INSTAGRAM,
        content_type=ContentType.PHOTO,
        category=Category.FASHION,
        likes=1,
        comments=1,
        shares=1,
        views=1,
        saves=1,
        follower_count=1,
        engagement_rate=1.0,
        hour_of_day=10,
        day_of_week="Wednesday",
        hashtag_count=1,
        content_length=1,
        sentiment="Positive",
        influencer_tier=CreatorTier.MICRO,
        has_media=True,
        is_verified=False,
        creator_id="CR_01",
        campaign_id=campaign_id,
        business_id="BS_01",
    )


def test_create_campaign_uses_validated_references_and_dates(campaign_context) -> None:
    service, campaign_repo, _ = campaign_context

    created = service.create_campaign(make_request())

    assert created.campaign_id.startswith("CP_")
    assert created.campaign_business_id == "BS_01"
    assert created.campaign_creator_ids == ["CR_01"]
    assert campaign_repo.get(created.campaign_id) == created


@pytest.mark.parametrize(
    "overrides",
    [
        {"campaign_business_id": "missing"},
        {"campaign_status": CampaignStatus.ACTIVE},
        {"campaign_start_date": "not-a-date"},
        {
            "campaign_start_date": (
                datetime.now().astimezone().date() - timedelta(days=1)
            ).isoformat(),
        },
        {
            "campaign_end_date": (
                datetime.now().astimezone().date() + timedelta(days=3)
            ).isoformat(),
        },
        {"campaign_creator_ids": ["missing"]},
    ],
)
def test_create_campaign_rejects_invalid_input(campaign_context, overrides) -> None:
    service, campaign_repo, _ = campaign_context

    with pytest.raises(BusinessRuleError):
        service.create_campaign(make_request(**overrides))

    assert campaign_repo.list() == []


def test_get_campaign_status_filter_and_missing_id(campaign_context) -> None:
    service, _, _ = campaign_context
    campaign = service.create_campaign(make_request())

    assert service.get_campaign(campaign.campaign_id) == campaign
    assert service.get_campaign_list_per_status(" DRAFT ") == [campaign]
    with pytest.raises(NotFoundError):
        service.get_campaign("missing")


def test_delete_campaign_rejects_posts_that_reference_it(campaign_context) -> None:
    service, campaign_repo, post_repo = campaign_context
    campaign = service.create_campaign(make_request())
    post_repo.add(make_post(campaign.campaign_id))

    with pytest.raises(BusinessRuleError, match="posts reference"):
        service.delete_campaign(campaign.campaign_id)

    assert campaign_repo.get(campaign.campaign_id) == campaign


def test_delete_unreferenced_campaign_succeeds(campaign_context) -> None:
    service, campaign_repo, _ = campaign_context
    campaign = service.create_campaign(make_request())

    service.delete_campaign(campaign.campaign_id)

    assert campaign_repo.get(campaign.campaign_id) is None
