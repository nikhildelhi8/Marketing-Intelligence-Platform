import pytest

from mip.domain.enums import CampaignStatus, Category
from mip.domain.models import Business, Campaign
from mip.exceptions import BusinessRuleError, NotFoundError
from mip.repositories.in_memory import InMemoryRepo
from mip.schemas.dto import CreateBusinessDTO
from mip.services.business_service import BusinessService


@pytest.fixture
def business_service() -> BusinessService:
    business_repo = InMemoryRepo(get_id=lambda business: business.business_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    return BusinessService(business_repo, campaign_repo)


def make_business(business_id: str = "BS_01") -> Business:
    return Business(
        business_id=business_id,
        business_name="Example Business",
        business_domain=Category.FASHION,
        business_budget=300_000,
    )


def make_campaign(status: CampaignStatus) -> Campaign:
    return Campaign(
        campaign_id="CP_01",
        campaign_business_id="BS_01",
        campaign_domain=Category.FASHION,
        campaign_budget=50_000,
        campaign_status=status,
        campaign_start_date="2030-01-01",
        campaign_end_date="2030-02-01",
    )


def test_create_business_returns_and_stores_business(
    business_service: BusinessService,
) -> None:
    request = CreateBusinessDTO(
        business_name="Example Business",
        business_domain=Category.FASHION,
        business_budget=300_000,
    )

    created = business_service.create_business(request)

    assert created.business_id.startswith("BS_")
    assert business_service.get_business(created.business_id) == created


def test_delete_business_with_active_campaign_is_blocked() -> None:
    business_repo = InMemoryRepo(get_id=lambda business: business.business_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    business_repo.add(make_business())
    campaign_repo.add(make_campaign(CampaignStatus.ACTIVE))
    service = BusinessService(business_repo, campaign_repo)

    with pytest.raises(BusinessRuleError):
        service.delete_business("BS_01")

    assert business_repo.get("BS_01") is not None


def test_delete_business_without_active_campaign_succeeds() -> None:
    business_repo = InMemoryRepo(get_id=lambda business: business.business_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    service = BusinessService(business_repo, campaign_repo)
    business = service.create_business(
        CreateBusinessDTO(
            business_name="Example Business",
            business_domain=Category.FASHION,
            business_budget=300_000,
        )
    )

    service.delete_business(business.business_id)

    with pytest.raises(NotFoundError):
        service.get_business(business.business_id)


def test_delete_missing_business_raises_not_found(
    business_service: BusinessService,
) -> None:
    with pytest.raises(NotFoundError):
        business_service.delete_business("missing")


def test_draft_campaign_does_not_block_business_deletion() -> None:
    business_repo = InMemoryRepo(get_id=lambda business: business.business_id)
    campaign_repo = InMemoryRepo(get_id=lambda campaign: campaign.campaign_id)
    business_repo.add(make_business())
    campaign_repo.add(make_campaign(CampaignStatus.DRAFT))
    service = BusinessService(business_repo, campaign_repo)

    service.delete_business("BS_01")

    assert business_repo.get("BS_01") is None
