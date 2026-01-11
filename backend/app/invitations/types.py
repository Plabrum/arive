"""Core types and protocols for the invitation system."""

from enum import Enum
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class InvitationType(Enum):
    """Types of invitations supported by the platform.

    Each type has a corresponding handler that defines:
    - Role level to assign
    - Post-accept logic (linking records, etc.)
    - Validation rules
    """

    TEAM_MEMBER = "team_member"
    """Regular team member with full team access"""

    ROSTER_MEMBER = "roster_member"
    """Talent/influencer with limited campaign access"""

    GUEST_BRAND = "guest_brand"
    """Brand with access to their campaigns (future)"""

    AGENCY_PARTNER = "agency_partner"
    """Agency with access to client campaigns (future)"""


class InvitationHandler(Protocol):
    """Interface for invitation type handlers.

    Each invitation type must implement this protocol.
    Handlers encapsulate type-specific logic while keeping
    the accept flow universal and branch-free.
    """

    @staticmethod
    def get_role_level() -> str:
        """Return the role level to assign (e.g., 'MEMBER', 'ROSTER_MEMBER').

        Returns:
            String value from RoleLevel enum
        """
        ...

    @staticmethod
    async def post_accept_hook(
        session: AsyncSession,
        user_id: int,
        team_id: int,
        invitation_context: dict,
    ) -> None:
        """Execute type-specific logic after user is created/linked to team.

        Examples:
        - Roster: Link user to roster record
        - Brand: Link user to brand record and campaigns
        - Team: No additional logic needed

        Args:
            session: Database session
            user_id: The user who accepted the invitation
            team_id: The team they're joining
            invitation_context: Type-specific data from invitation token
                               (e.g., {'roster_id': 123} or {'brand_id': 456})
        """
        ...

    @staticmethod
    async def validate_invitation_context(
        session: AsyncSession,
        context: dict,
    ) -> bool:
        """Validate invitation-specific context before creating invitation.

        Examples:
        - Roster: Ensure roster exists and has email
        - Brand: Ensure brand exists and has email
        - Team: Always valid

        Args:
            session: Database session
            context: Type-specific context to validate

        Returns:
            True if context is valid, False otherwise
        """
        ...
