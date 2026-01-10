"""Utility functions for roster member invitations."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.enums import RoleLevel
from app.utils.configure import config


async def generate_roster_invitation_link(
    db_session: AsyncSession,
    roster_id: int,
    team_id: int,
    invited_email: str,
    invited_by_user_id: int,
    expires_in_hours: int = 72,
) -> str:
    """Generate secure roster invitation link with token."""
    from app.auth.crypto import generate_secure_token, hash_token
    from app.auth.models import TeamInvitationToken

    plaintext_token = generate_secure_token()
    token_hash = hash_token(plaintext_token)

    invitation = TeamInvitationToken.create_invitation(
        team_id=team_id,
        invited_email=invited_email.lower(),
        invited_by_user_id=invited_by_user_id,
        token_hash=token_hash,
        expires_in_hours=expires_in_hours,
        roster_id=roster_id,  # NEW: Mark as roster invitation
        invited_role_level=RoleLevel.ROSTER_MEMBER,  # NEW: Assign roster role
    )

    db_session.add(invitation)
    await db_session.flush()

    base_url = config.FRONTEND_ORIGIN.rstrip("/")
    invitation_url = f"{base_url}/roster/invitations/accept?token={plaintext_token}"

    return invitation_url


async def verify_roster_invitation_token(
    session: AsyncSession,
    token: str,
) -> dict[str, Any] | None:
    """Verify roster invitation token and return invitation data if valid."""
    from app.auth.crypto import hash_token
    from app.auth.models import TeamInvitationToken

    token_hash = hash_token(token)

    stmt = select(TeamInvitationToken).where(
        TeamInvitationToken.token_hash == token_hash,
        TeamInvitationToken.roster_id.is_not(None),  # Ensure it's a roster invitation
    )
    result = await session.execute(stmt)
    invitation = result.scalar_one_or_none()

    if not invitation or not invitation.is_valid():
        return None

    return {
        "roster_id": invitation.roster_id,
        "team_id": invitation.team_id,
        "invited_email": invitation.invited_email,
        "invited_role_level": invitation.invited_role_level or RoleLevel.ROSTER_MEMBER,
    }
