"""Universal invitation system for all invitation types.

This module provides a platform for handling different types of invitations:
- Team member invitations
- Roster member invitations
- Guest brand invitations (future)
- Agency partner invitations (future)

Architecture:
- Strategy pattern: Each invitation type has its own handler
- No branching: Accept flow is universal
- Extensible: Add new types by creating handler + registering
"""

from app.invitations.registry import get_handler
from app.invitations.service import generate_invitation_link
from app.invitations.types import InvitationHandler, InvitationType

__all__ = [
    "InvitationType",
    "InvitationHandler",
    "get_handler",
    "generate_invitation_link",
]
