"""DEPRECATED: Utility functions for roster member invitations.

This module is deprecated in favor of the universal invitation system.
Use app.invitations.generate_invitation_link() instead.

Old:
    from app.roster.utils import generate_roster_invitation_link
    link = await generate_roster_invitation_link(...)

New:
    from app.invitations import InvitationType, generate_invitation_link
    link = await generate_invitation_link(
        invitation_type=InvitationType.ROSTER_MEMBER,
        invitation_context={"roster_id": roster_id},
        ...
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession


async def generate_roster_invitation_link(
    db_session: AsyncSession,
    roster_id: int,
    team_id: int,
    invited_email: str,
    invited_by_user_id: int,
    expires_in_hours: int = 72,
) -> str:
    """DEPRECATED: Use app.invitations.generate_invitation_link() instead.

    This function is kept for backward compatibility but will be removed in a future version.
    """
    import warnings

    from app.invitations import InvitationType, generate_invitation_link

    warnings.warn(
        "generate_roster_invitation_link() is deprecated. "
        "Use app.invitations.generate_invitation_link() with InvitationType.ROSTER_MEMBER instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Delegate to new universal service
    return await generate_invitation_link(
        db_session=db_session,
        team_id=team_id,
        invited_email=invited_email,
        invited_by_user_id=invited_by_user_id,
        invitation_type=InvitationType.ROSTER_MEMBER,
        invitation_context={"roster_id": roster_id},
        expires_in_hours=expires_in_hours,
    )
