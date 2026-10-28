import pytest

from mip.domain.enums import CampaignStatus, Category, ContentType, CreatorTier, Platform
from mip.domain.models import Campaign, Creator, SocialPost
from mip.exceptions import BusinessRuleError, NotFoundError
from mip.repositories.in_memory import InMemoryRepo
from mip.schemas.dto import CreateCreatorDTO
from mip.services.creator_service import CreatorService


@pytest.fixture
def creator_service() -> CreatorService:
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    social_post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    return CreatorService(creator_repo, campaign_repo, social_post_repo)


def make_creator(
    creator_id: str = "CR_01",
    creator_name: str = "Sample Creator",
) -> Creator:
    return Creator(
        creator_id=creator_id,
        creator_name=creator_name,
        creator_bio="Sample bio",
        creator_niche=Category.FASHION,
        creator_tier=CreatorTier.MICRO,
        creator_follower_count=12_000,
    )


def make_campaign(creator_ids: list[str]) -> Campaign:
    return Campaign(
        campaign_id="CP_01",
        campaign_business_id="BS_01",
        campaign_domain=Category.FASHION,
        campaign_budget=20_000,
        campaign_status=CampaignStatus.DRAFT,
        campaign_start_date="2030-01-01",
        campaign_end_date="2030-02-01",
        campaign_creator_ids=creator_ids,
    )


def make_post(creator_id: str) -> SocialPost:
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
        creator_id=creator_id,
        campaign_id=None,
        business_id=None,
    )


def make_request(name: str = "Sample Creator") -> CreateCreatorDTO:
    return CreateCreatorDTO(
        creator_name=name,
        creator_bio="Sample bio",
        creator_niche=Category.FASHION,
        creator_tier=CreatorTier.MICRO,
        creator_follower_count=12_000,
    )


def test_create_creator_stores_creator(creator_service: CreatorService) -> None:
    created = creator_service.create_creator(make_request())

    assert created.creator_id.startswith("CR_")
    assert creator_service.get_creator(created.creator_id) == created


def test_create_creator_rejects_duplicate_name_niche_and_tier() -> None:
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    social_post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    creator_repo.add(make_creator())
    service = CreatorService(creator_repo, campaign_repo, social_post_repo)

    with pytest.raises(BusinessRuleError):
        service.create_creator(make_request("  SAMPLE CREATOR  "))


def test_delete_creator_rejects_campaign_reference() -> None:
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    social_post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    creator_repo.add(make_creator())
    campaign_repo.add(make_campaign(["CR_01"]))
    service = CreatorService(creator_repo, campaign_repo, social_post_repo)

    with pytest.raises(BusinessRuleError, match="campaign"):
        service.delete_creator("CR_01")

    assert creator_repo.get("CR_01") is not None


def test_delete_creator_rejects_post_reference() -> None:
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    social_post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    creator_repo.add(make_creator())
    social_post_repo.add(make_post("CR_01"))
    service = CreatorService(creator_repo, campaign_repo, social_post_repo)

    with pytest.raises(BusinessRuleError, match="social post"):
        service.delete_creator("CR_01")


def test_delete_unreferenced_creator_succeeds() -> None:
    creator_repo = InMemoryRepo(get_id=lambda creator: creator.creator_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    social_post_repo = InMemoryRepo(get_id=lambda post: post.post_id)
    creator_repo.add(make_creator())
    service = CreatorService(creator_repo, campaign_repo, social_post_repo)

    service.delete_creator("CR_01")

    with pytest.raises(NotFoundError):
        service.get_creator("CR_01")


def test_delete_missing_creator_raises_not_found(
    creator_service: CreatorService,
) -> None:
    with pytest.raises(NotFoundError):
        creator_service.delete_creator("missing")
