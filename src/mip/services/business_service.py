from typing import Protocol
from uuid import uuid4

from mip.domain.enums import CampaignStatus
from mip.domain.models import Business, Campaign
from mip.exceptions import BusinessRuleError
from mip.schemas.dto import CreateBusinessDTO


class BusinessRepository(Protocol):
    def add(self, entity: Business) -> None: ...

    def get_or_raise(self, entity_id: str) -> Business: ...

    def delete(self, entity_id: str) -> None: ...


class CampaignRepository(Protocol):
    def list(self) -> list[Campaign]: ...


class BusinessService :

    def __init__(
        self,
        business_repo: BusinessRepository,
        campaign_repo: CampaignRepository,
    ) -> None:

        self._business_repo = business_repo
        self._campaign_repo = campaign_repo


    def create_business(
        self,
        request: CreateBusinessDTO,
    ) -> Business:

        business_id = f"BS_{uuid4().hex[:8]}"

        business = Business(
            business_id=business_id,
            business_name=request.business_name,
            business_domain=request.business_domain,
            business_budget=request.business_budget,
        )

        self._business_repo.add(business)

        return business


    def delete_business(self, business_id: str) -> None:
        self._business_repo.get_or_raise(business_id)

        has_active_campaign = any(
            campaign.campaign_business_id == business_id
            and campaign.campaign_status is CampaignStatus.ACTIVE
            for campaign in self._campaign_repo.list()
        )

        if has_active_campaign:
            raise BusinessRuleError(
                f"{business_id} has active campaigns listed, cannot delete it"
            )

        self._business_repo.delete(business_id)


    def get_business(self, business_id: str) -> Business:
        return self._business_repo.get_or_raise(business_id)





