"""Utility functions for roster member invitations."""

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

    # Use frontend origin to match team invitation pattern
    # Frontend will handle the redirect to backend /teams/invitations/accept
    base_url = config.FRONTEND_ORIGIN.rstrip("/")
    invitation_url = f"{base_url}/invite/accept?token={plaintext_token}"

    return invitation_url
