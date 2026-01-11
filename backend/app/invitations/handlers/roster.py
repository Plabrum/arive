"""Roster member invitation handler."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.enums import RoleLevel

logger = logging.getLogger(__name__)


class RosterInvitationHandler:
    """Handles roster member (talent/influencer) invitations.

    Roster members get limited campaign access with ROSTER_MEMBER role.
    Post-accept: Link user to their roster record.
    """

    @staticmethod
    def get_role_level() -> str:
        """Roster members get ROSTER_MEMBER role (limited campaign access)."""
        return RoleLevel.ROSTER_MEMBER.value

    @staticmethod
    async def get_user_name(
        session: AsyncSession,
        invited_email: str,
        invitation_context: dict,
    ) -> str | None:
        """Get roster name for the new user account.

        Args:
            session: Database session
            invited_email: The email address of the invitee
            invitation_context: Must contain 'roster_id'

        Returns:
            Roster name, or None if roster not found (falls back to email prefix)
        """
        from app.roster.models import Roster

        roster_id = invitation_context.get("roster_id")
        if not roster_id:
            logger.warning(f"Roster invitation missing roster_id in context: {invitation_context}")
            return None

        roster = await session.get(Roster, roster_id)
        if roster:
            return roster.name
        else:
            logger.warning(f"Roster {roster_id} not found, using email prefix for user name")
            return None

    @staticmethod
    async def post_accept_hook(
        session: AsyncSession,
        user_id: int,
        team_id: int,
        invitation_context: dict,
    ) -> None:
        """Link user to roster record.

        Args:
            session: Database session
            user_id: The user who accepted
            team_id: The team they're joining
            invitation_context: Must contain 'roster_id'
        """
        from app.roster.models import Roster

        roster_id = invitation_context.get("roster_id")
        if not roster_id:
            logger.warning(f"Roster invitation missing roster_id in context: {invitation_context}")
            return

        # Link user to roster record
        roster = await session.get(Roster, roster_id)
        if roster:
            roster.roster_user_id = user_id  # type: ignore[assignment]
            logger.info(f"Linked roster {roster_id} to user {user_id}")
        else:
            logger.warning(f"Roster {roster_id} not found for invitation, skipping roster link")

    @staticmethod
    async def validate_invitation_context(
        session: AsyncSession,
        context: dict,
    ) -> bool:
        """Ensure roster exists and has email.

        Args:
            session: Database session
            context: Must contain 'roster_id'

        Returns:
            True if roster exists and has email, False otherwise
        """
        from app.roster.models import Roster

        roster_id = context.get("roster_id")
        if not roster_id:
            logger.error("Roster invitation missing roster_id in context")
            return False

        roster = await session.get(Roster, roster_id)
        if not roster:
            logger.error(f"Roster {roster_id} not found")
            return False

        if not roster.email:
            logger.error(f"Roster {roster_id} has no email address")
            return False

        return True
