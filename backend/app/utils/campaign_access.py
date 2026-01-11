"""Campaign access control utilities.

This module provides a flexible system for determining which campaigns a user can access.
Access can be granted through multiple mechanisms:
- Roster member assignment (assigned_roster_id)
- Direct campaign permissions (future)
- Guest access tokens (future)
- Team membership (via RLS)
"""

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.campaigns.models import Campaign
from app.roster.models import Roster
from app.users.enums import RoleLevel
from app.users.models import Role

if TYPE_CHECKING:
    pass


async def get_accessible_campaign_ids(
    session: AsyncSession,
    user_id: int,
    team_id: int,
) -> list[int] | None:
    """Get list of campaign IDs that a user can access.

    Returns:
        List of campaign IDs if user has limited access (e.g., roster member)
        None if user has full team access (will see all campaigns via RLS)
    """
    # Check if user has ROSTER_MEMBER role
    role_stmt = select(Role).where(
        Role.user_id == user_id,
        Role.team_id == team_id,
        Role.role_level == RoleLevel.ROSTER_MEMBER,
    )
    role_result = await session.execute(role_stmt)
    role = role_result.scalar_one_or_none()

    if not role:
        # User is not a roster member, they have full team access via RLS
        return None

    # User is a roster member - find their roster record
    roster_stmt = select(Roster).where(
        Roster.roster_user_id == user_id,
        Roster.team_id == team_id,
    )
    roster_result = await session.execute(roster_stmt)
    roster = roster_result.scalar_one_or_none()

    if not roster:
        # Roster member but no roster record found - no access
        return []

    # Get campaigns assigned to this roster member
    campaign_stmt = select(Campaign.id).where(Campaign.assigned_roster_id == roster.id)
    campaign_result = await session.execute(campaign_stmt)
    campaign_ids = [int(cid) for cid in campaign_result.scalars().all()]

    return campaign_ids


def apply_campaign_access_filter(
    query: Select,
    campaign_ids: list[int],
) -> Select:
    """Filter campaigns to only those in the accessible list."""
    if not campaign_ids:
        # No accessible campaigns - return empty result
        return query.where(Campaign.id == -1)
    return query.where(Campaign.id.in_(campaign_ids))


def apply_media_access_filter(
    query: Select,
    campaign_ids: list[int],
) -> Select:
    """Filter media to only show items for accessible campaigns."""
    from app.media.models import Media

    if not campaign_ids:
        # No accessible campaigns - return empty result
        return query.where(Media.id == -1)

    return query.where(Media.campaign_id.in_(campaign_ids))


def apply_deliverable_access_filter(
    query: Select,
    campaign_ids: list[int],
) -> Select:
    """Filter deliverables to only those for accessible campaigns."""
    from app.deliverables.models import Deliverable

    if not campaign_ids:
        # No accessible campaigns - return empty result
        return query.where(Deliverable.id == -1)

    return query.where(Deliverable.campaign_id.in_(campaign_ids))


async def apply_campaign_scoped_filter(
    query: Select,
    session: AsyncSession,
    user_id: int,
    team_id: int,
    model_class: type,
) -> Select:
    """Apply campaign-based access filtering to a query if needed.

    This helper checks if the user has limited campaign access (e.g., roster member)
    and applies appropriate filtering based on the model class being queried.

    Args:
        query: The SQLAlchemy query to filter
        session: Database session
        user_id: Current user ID
        team_id: Current team ID
        model_class: The model class being queried (Campaign, Media, Deliverable, etc.)

    Returns:
        Filtered query if user has limited access, otherwise unchanged query
    """
    # Get accessible campaign IDs for this user
    campaign_ids = await get_accessible_campaign_ids(session, user_id, team_id)

    if campaign_ids is None:
        # User has full team access, no filtering needed
        return query

    # Apply filtering based on model class
    model_name = model_class.__name__

    if model_name == "Campaign":
        return apply_campaign_access_filter(query, campaign_ids)
    elif model_name == "Media":
        return apply_media_access_filter(query, campaign_ids)
    elif model_name == "Deliverable":
        return apply_deliverable_access_filter(query, campaign_ids)
    else:
        # For other models, users with limited access shouldn't see anything
        # Return a query that will match nothing
        return query.where(model_class.id == -1)


# Legacy aliases for backward compatibility (to be removed)
async def get_roster_for_user(
    session: AsyncSession,
    user_id: int,
    team_id: int,
) -> Roster | None:
    """Legacy: Get the Roster record for a user if they are a roster member.

    DEPRECATED: Use get_accessible_campaign_ids() instead.
    """
    role_stmt = select(Role).where(
        Role.user_id == user_id,
        Role.team_id == team_id,
        Role.role_level == RoleLevel.ROSTER_MEMBER,
    )
    role_result = await session.execute(role_stmt)
    role = role_result.scalar_one_or_none()

    if not role:
        return None

    roster_stmt = select(Roster).where(
        Roster.roster_user_id == user_id,
        Roster.team_id == team_id,
    )
    roster_result = await session.execute(roster_stmt)
    return roster_result.scalar_one_or_none()
