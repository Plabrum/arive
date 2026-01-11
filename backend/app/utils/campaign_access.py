"""Campaign access control for limited-access users.

This module provides a flexible, extensible system for determining which campaigns
a user can access based on their role and access type.

Supported access patterns:
- Roster members: See only campaigns they're assigned to
- Guest brands: See campaigns they're added to (future)
- Agency partners: See campaigns for their agency (future)
- Team members: See all campaigns (via RLS, no filtering)
"""

from enum import Enum
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


class AccessType(Enum):
    """Types of limited campaign access."""

    ROSTER_MEMBER = "roster_member"
    GUEST_BRAND = "guest_brand"  # Future
    AGENCY_PARTNER = "agency_partner"  # Future


class CampaignAccessPolicy(Protocol):
    """Interface for campaign access policies."""

    async def get_accessible_campaign_ids(self, session: AsyncSession, user_id: int, team_id: int) -> list[int] | None:
        """Return campaign IDs user can access, or None for full access."""
        ...


class RosterMemberAccess:
    """Campaign access for roster members (talent/influencers)."""

    async def get_accessible_campaign_ids(self, session: AsyncSession, user_id: int, team_id: int) -> list[int] | None:
        """Roster members see only campaigns they're assigned to.

        Returns:
            list[int]: Campaign IDs the roster member can access
            []: Roster member but no campaigns assigned (no access)
            None: Not a roster member (full access via other roles)
        """
        from app.campaigns.models import Campaign
        from app.roster.models import Roster
        from app.users.enums import RoleLevel
        from app.users.models import Role

        # Check if user has ROSTER_MEMBER role
        role = await session.scalar(
            select(Role).where(
                Role.user_id == user_id,
                Role.team_id == team_id,
                Role.role_level == RoleLevel.ROSTER_MEMBER,
            )
        )
        if not role:
            return None  # Not a roster member, has full access

        # Find their roster record
        roster = await session.scalar(
            select(Roster).where(
                Roster.roster_user_id == user_id,
                Roster.team_id == team_id,
            )
        )
        if not roster:
            return []  # Roster member but no record = no access

        # Get assigned campaigns
        campaign_ids = await session.scalars(select(Campaign.id).where(Campaign.assigned_roster_id == roster.id))
        return [int(cid) for cid in campaign_ids]


class GuestBrandAccess:
    """Campaign access for guest brands (future implementation)."""

    async def get_accessible_campaign_ids(self, session: AsyncSession, user_id: int, team_id: int) -> list[int] | None:
        """Guest brands see campaigns they're added to.

        TODO: Implement when guest brand invitations are added.
        Will check for GUEST_BRAND role, then query campaigns
        where brand_id matches or via campaign_brands junction table.
        """
        raise NotImplementedError("Guest brand access coming soon")


# Registry of access policies (checked in order)
ACCESS_POLICIES: dict[AccessType, CampaignAccessPolicy] = {
    AccessType.ROSTER_MEMBER: RosterMemberAccess(),
    # AccessType.GUEST_BRAND: GuestBrandAccess(),  # Uncomment when ready
}


async def get_user_campaign_access(
    session: AsyncSession,
    user_id: int,
    team_id: int,
) -> list[int] | None:
    """Get campaign IDs a user can access based on their roles.

    This function checks all registered access policies in order.
    The first policy that returns a non-None result determines access.

    Returns:
        list[int]: Specific campaign IDs if user has limited access
        []: User has limited access but no campaigns available
        None: User has full team access (no filtering needed)
    """
    # Check each access policy in order
    for policy in ACCESS_POLICIES.values():
        campaign_ids = await policy.get_accessible_campaign_ids(session, user_id, team_id)
        if campaign_ids is not None:  # Found a limiting policy
            return campaign_ids

    # No limiting policies matched = full access
    return None


def filter_by_campaign_access(query: Select, campaign_ids: list[int], model_class: type) -> Select:
    """Apply campaign-based filtering to a query.

    Works for any model that is either Campaign itself or has a campaign_id foreign key.
    Models without campaign relationship deny access for limited users.

    Args:
        query: The SQLAlchemy query to filter
        campaign_ids: List of accessible campaign IDs (empty list = no access)
        model_class: The model class being queried

    Returns:
        Filtered query
    """
    if not campaign_ids:
        # No accessible campaigns - return query that matches nothing
        return query.where(model_class.id == -1)

    # Determine how to filter based on model
    model_name = model_class.__name__

    if model_name == "Campaign":
        # Filtering Campaign model directly
        return query.where(model_class.id.in_(campaign_ids))
    elif hasattr(model_class, "campaign_id"):
        # Model has campaign_id FK (Media, Deliverable, etc.)
        return query.where(model_class.campaign_id.in_(campaign_ids))
    else:
        # Model isn't campaign-scoped - deny access for limited users
        return query.where(model_class.id == -1)
