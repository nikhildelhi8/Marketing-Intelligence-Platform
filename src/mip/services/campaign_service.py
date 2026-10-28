from datetime import date, datetime
from typing import Protocol
from uuid import uuid4

from mip.domain.enums import CampaignStatus
from mip.domain.models import Business, Campaign, Creator, SocialPost
from mip.exceptions import BusinessRuleError
from mip.schemas.dto import CreateCampaignDTO


class CampaignRepository(Protocol):
    def add(self, entity: Campaign) -> None: ...

    def get_or_raise(self, entity_id: str) -> Campaign: ...

    def delete(self, entity_id: str) -> None: ...

    def list(self) -> list[Campaign]: ...


class BusinessRepository(Protocol):
    def list(self) -> list[Business]: ...


class CreatorRepository(Protocol):
    def list(self) -> list[Creator]: ...


class SocialPostRepository(Protocol):
    def list(self) -> list[SocialPost]: ...


class CampaignService:
    def __init__(
        self,
        business_repo: BusinessRepository,
        campaign_repo: CampaignRepository,
        creator_repo: CreatorRepository,
        social_post_repo: SocialPostRepository,
    ) -> None:
        self._campaign_repo = campaign_repo
        self._business_repo = business_repo
        self._creator_repo = creator_repo
        self._social_post_repo = social_post_repo

    def get_campaign(self, campaign_id: str) -> Campaign:
        return self._campaign_repo.get_or_raise(campaign_id)

    def get_campaign_list_per_status(self, status: str) -> list[Campaign]:
        normalized_status = status.strip().casefold()
        return [
            campaign
            for campaign in self._campaign_repo.list()
            if campaign.campaign_status.value.casefold() == normalized_status
        ]

    def create_campaign(self, request: CreateCampaignDTO) -> Campaign:
        available_business_ids = {
            business.business_id for business in self._business_repo.list()
        }
        if request.campaign_business_id not in available_business_ids:
            raise BusinessRuleError(
                f"{request.campaign_business_id} is not a valid business ID"
            )

        if request.campaign_status is not CampaignStatus.DRAFT:
            raise BusinessRuleError("A new campaign must have draft status")

        try:
            start_date = date.fromisoformat(request.campaign_start_date)
            end_date = date.fromisoformat(request.campaign_end_date)
        except ValueError as exc:
            raise BusinessRuleError(
                "Campaign start and end dates must be valid ISO dates (YYYY-MM-DD)"
            ) from exc

        if start_date <= datetime.now().astimezone().date():
            raise BusinessRuleError("Campaign start date must be in the future")

        if end_date <= start_date:
            raise BusinessRuleError("Campaign end date must be after its start date")

        available_creator_ids = {
            creator.creator_id for creator in self._creator_repo.list()
        }
        invalid_creator_ids = [
            creator_id
            for creator_id in request.campaign_creator_ids
            if creator_id not in available_creator_ids
        ]
        if invalid_creator_ids:
            raise BusinessRuleError(
                f"Unknown creator IDs: {', '.join(invalid_creator_ids)}"
            )

        campaign = Campaign(
            campaign_id=f"CP_{uuid4().hex[:8]}",
            campaign_business_id=request.campaign_business_id,
            campaign_domain=request.campaign_domain,
            campaign_budget=request.campaign_budget,
            campaign_status=request.campaign_status,
            campaign_start_date=start_date.isoformat(),
            campaign_end_date=end_date.isoformat(),
            campaign_creator_ids=list(request.campaign_creator_ids),
        )
        self._campaign_repo.add(campaign)
        return campaign

    def delete_campaign(self, campaign_id: str) -> None:
        self._campaign_repo.get_or_raise(campaign_id)

        has_referencing_posts = any(
            post.campaign_id == campaign_id
            for post in self._social_post_repo.list()
        )
        if has_referencing_posts:
            raise BusinessRuleError(
                f"Campaign {campaign_id} cannot be deleted because posts reference it"
            )

        self._campaign_repo.delete(campaign_id)
