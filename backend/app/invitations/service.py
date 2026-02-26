"""Universal invitation service."""

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.invitations.registry import get_handler
from app.invitations.types import InvitationType
from app.utils.configure import config

logger = logging.getLogger(__name__)


async def generate_invitation_link(
    db_session: AsyncSession,
    team_id: int,
    invited_email: str,
    invited_by_user_id: int,
    invitation_type: InvitationType,
    invitation_context: dict | None = None,
    expires_in_hours: int = 72,
) -> str:
    """Universal invitation link generator - works for all invitation types!

    This replaces type-specific functions like:
    - generate_roster_invitation_link()
    - generate_team_invitation_link()
    - generate_brand_invitation_link() (future)

    Args:
        db_session: Database session
        team_id: Team the user is being invited to
        invited_email: Email address of invitee
        invited_by_user_id: User sending the invitation
        invitation_type: Type of invitation (team, roster, brand, etc.)
        invitation_context: Type-specific context (e.g., {'roster_id': 123})
        expires_in_hours: Hours until invitation expires (default: 72)

    Returns:
        Frontend invitation URL with token

    Raises:
        ValueError: If invitation context is invalid for this type

    Example:
        # Team member invitation
        link = await generate_invitation_link(
            db_session=session,
            team_id=1,
            invited_email="user@example.com",
            invited_by_user_id=1,
            invitation_type=InvitationType.TEAM_MEMBER,
        )

        # Roster member invitation
        link = await generate_invitation_link(
            db_session=session,
            team_id=1,
            invited_email="talent@example.com",
            invited_by_user_id=1,
            invitation_type=InvitationType.ROSTER_MEMBER,
            invitation_context={"roster_id": 123},
        )
    """
    from app.auth.crypto import generate_secure_token, hash_token
    from app.auth.models import TeamInvitationToken

    # Validate context using type-specific handler
    handler = get_handler(invitation_type)
    if invitation_context and not await handler.validate_invitation_context(db_session, invitation_context):
        raise ValueError(f"Invalid invitation context for {invitation_type}: {invitation_context}")

    # Generate secure token
    plaintext_token = generate_secure_token()
    token_hash = hash_token(plaintext_token)

    # Create invitation record
    invitation = TeamInvitationToken(
        team_id=team_id,
        invited_email=invited_email.lower().strip(),
        invited_by_user_id=invited_by_user_id,
        token_hash=token_hash,
        expires_at=datetime.now(tz=UTC) + timedelta(hours=expires_in_hours),
        invitation_type=invitation_type.value,
        invitation_context=invitation_context or {},
    )

    db_session.add(invitation)
    await db_session.flush()

    logger.info(
        f"Created {invitation_type.value} invitation: "
        f"team_id={team_id}, email={invited_email}, context={invitation_context}"
    )

    # Build frontend URL
    base_url = config.FRONTEND_ORIGIN.rstrip("/")
    invitation_url = f"{base_url}/invite/accept?token={plaintext_token}"

    return invitation_url
