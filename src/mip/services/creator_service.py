from typing import Protocol
from uuid import uuid4

from mip.domain.models import Campaign, Creator, SocialPost
from mip.exceptions import BusinessRuleError
from mip.schemas.dto import CreateCreatorDTO


class CreatorRepository(Protocol):
    def add(self, entity: Creator) -> None: ...

    def get_or_raise(self, entity_id: str) -> Creator: ...

    def delete(self, entity_id: str) -> None: ...

    def list(self) -> list[Creator]: ...


class CampaignRepository(Protocol):
    def list(self) -> list[Campaign]: ...


class SocialPostRepository(Protocol):
    def list(self) -> list[SocialPost]: ...


class CreatorService:
    def __init__(
        self,
        creator_repo: CreatorRepository,
        campaign_repo: CampaignRepository,
        social_post_repo: SocialPostRepository,
    ) -> None:
        self._creator_repo = creator_repo
        self._campaign_repo = campaign_repo
        self._social_post_repo = social_post_repo

    def create_creator(self, request: CreateCreatorDTO) -> Creator:
        normalized_name = request.creator_name.strip().casefold()
        has_duplicate_creator = any(
            creator.creator_name.strip().casefold() == normalized_name
            and creator.creator_tier is request.creator_tier
            and creator.creator_niche is request.creator_niche
            for creator in self._creator_repo.list()
        )

        if has_duplicate_creator:
            raise BusinessRuleError(
                f"{request.creator_name} with {request.creator_tier.value} "
                f"in {request.creator_niche.value} is already present"
            )

        creator_id = f"CR_{uuid4().hex[:8]}"

        creator = Creator(
            creator_id=creator_id,
            creator_name=request.creator_name.strip(),
            creator_bio=request.creator_bio,
            creator_niche=request.creator_niche,
            creator_tier=request.creator_tier,
            creator_follower_count=request.creator_follower_count,
        )

        self._creator_repo.add(creator)
        return creator

    def delete_creator(self, creator_id: str) -> None:
        self._creator_repo.get_or_raise(creator_id)

        has_campaign_reference = any(
            creator_id in campaign.campaign_creator_ids
            for campaign in self._campaign_repo.list()
        )
        if has_campaign_reference:
            raise BusinessRuleError(
                f"Creator {creator_id} cannot be deleted because a campaign references it"
            )

        has_post_reference = any(
            post.creator_id == creator_id for post in self._social_post_repo.list()
        )
        if has_post_reference:
            raise BusinessRuleError(
                f"Creator {creator_id} cannot be deleted because a social post references it"
            )

        self._creator_repo.delete(creator_id)

    def get_creator(self, creator_id: str) -> Creator:
        return self._creator_repo.get_or_raise(creator_id)

    

        
