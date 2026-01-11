"""Handler registry for invitation types."""

from app.invitations.handlers.roster import RosterInvitationHandler
from app.invitations.handlers.team import TeamMemberInvitationHandler
from app.invitations.types import InvitationHandler, InvitationType

# from app.invitations.handlers.guest_brand import GuestBrandInvitationHandler  # Uncomment when ready


INVITATION_HANDLERS: dict[InvitationType, InvitationHandler] = {
    InvitationType.TEAM_MEMBER: TeamMemberInvitationHandler(),
    InvitationType.ROSTER_MEMBER: RosterInvitationHandler(),
    # InvitationType.GUEST_BRAND: GuestBrandInvitationHandler(),  # Uncomment when implemented
}
"""Registry of invitation type handlers.

To add a new invitation type:
1. Create handler class implementing InvitationHandler protocol
2. Add enum value to InvitationType
3. Register handler here
4. Add GUEST_BRAND to RoleLevel enum if needed
"""


def get_handler(invitation_type: InvitationType) -> InvitationHandler:
    """Get handler for invitation type.

    Args:
        invitation_type: The type of invitation

    Returns:
        Handler instance for this invitation type

    Raises:
        ValueError: If no handler registered for this type
    """
    handler = INVITATION_HANDLERS.get(invitation_type)
    if not handler:
        raise ValueError(f"No handler registered for {invitation_type}")
    return handler
