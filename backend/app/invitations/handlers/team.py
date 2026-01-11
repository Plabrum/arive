"""Team member invitation handler."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.enums import RoleLevel

logger = logging.getLogger(__name__)


class TeamMemberInvitationHandler:
    """Handles regular team member invitations.

    Team members get full team access with MEMBER role.
    No special post-accept logic needed.
    """

    @staticmethod
    def get_role_level() -> str:
        """Team members get MEMBER role."""
        return RoleLevel.MEMBER.value

    @staticmethod
    async def post_accept_hook(
        session: AsyncSession,
        user_id: int,
        team_id: int,
        invitation_context: dict,
    ) -> None:
        """No special logic needed for team members.

        Team members just need:
        1. User account created (done by accept flow)
        2. Role created (done by accept flow)
        """
        logger.info(f"Team member invitation accepted: user_id={user_id}, team_id={team_id}")

    @staticmethod
    async def validate_invitation_context(
        session: AsyncSession,
        context: dict,
    ) -> bool:
        """Team member invitations always valid.

        No additional context required beyond email + team.
        """
        return True
