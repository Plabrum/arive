"""Authentication-related database models."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import BaseDBModel
from app.utils.sqids import Sqid

if TYPE_CHECKING:
    from app.roster.models import Roster
    from app.teams.models import Team
    from app.users.models import User


class MagicLinkToken(BaseDBModel):
    """Model for magic link authentication tokens.

    Tokens are stored as SHA-256 hashes for security.
    The plaintext token is sent in the email link but never stored.
    """

    __tablename__ = "magic_link_tokens"

    token_hash: Mapped[str] = mapped_column(sa.Text, index=True, unique=True, nullable=False)
    """SHA-256 hash of the token (64 hex characters)"""

    user_id: Mapped[Sqid] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    """User this magic link is for"""

    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    """When this token expires (15 minutes from creation)"""

    used_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True, default=None)
    """When this token was used (null if not used yet)"""

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="magic_link_tokens")

    @classmethod
    def create_for_user(cls, user_id: int, token_hash: str, expires_in_minutes: int = 15) -> "MagicLinkToken":
        """Create a new magic link token for a user.

        Args:
            user_id: ID of the user
            token_hash: SHA-256 hash of the token
            expires_in_minutes: Minutes until expiration (default: 15)

        Returns:
            New MagicLinkToken instance
        """
        return cls(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=datetime.now(tz=UTC) + timedelta(minutes=expires_in_minutes),
        )

    def is_valid(self) -> bool:
        """Check if token is valid (not expired, not used)."""
        now = datetime.now(tz=UTC)
        return self.expires_at > now and self.used_at is None

    def mark_as_used(self) -> None:
        """Mark this token as used."""
        self.used_at = datetime.now(tz=UTC)


class TeamInvitationToken(BaseDBModel):
    """Model for team invitation tokens.

    Tokens are stored as SHA-256 hashes for security.
    The plaintext token is sent in the email link but never stored.
    """

    __tablename__ = "team_invitation_tokens"
    __table_args__ = (
        # Prevent duplicate pending regular team invitations
        sa.Index(
            "ix_team_invitation_pending",
            "team_id",
            "invited_email",
            unique=True,
            postgresql_where=sa.text("accepted_at IS NULL AND roster_id IS NULL"),
        ),
        # Prevent duplicate pending roster invitations
        sa.Index(
            "ix_roster_invitation_pending",
            "team_id",
            "roster_id",
            "invited_email",
            unique=True,
            postgresql_where=sa.text("accepted_at IS NULL AND roster_id IS NOT NULL"),
        ),
    )

    token_hash: Mapped[str] = mapped_column(sa.Text, index=True, unique=True, nullable=False)
    """SHA-256 hash of the token (64 hex characters)"""

    team_id: Mapped[Sqid] = mapped_column(sa.ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    """Team the user is being invited to"""

    invited_email: Mapped[str] = mapped_column(sa.Text, index=True, nullable=False)
    """Email address of the invited user"""

    invited_by_user_id: Mapped[Sqid] = mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    """User who sent the invitation"""

    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    """When this token expires (72 hours from creation)"""

    accepted_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True, default=None)
    """When this invitation was accepted (null if not accepted yet)"""

    # Optional fields for roster member invitations
    roster_id: Mapped[Sqid | None] = mapped_column(
        sa.ForeignKey("roster.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    """If this is a roster member invitation, the roster record being invited"""

    invited_role_level: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
    )
    """The role level to assign (e.g., 'MEMBER', 'ROSTER_MEMBER'). Defaults to MEMBER if null."""

    # Relationships
    team: Mapped["Team"] = relationship("Team", back_populates="invitation_tokens")
    invited_by: Mapped["User"] = relationship("User", foreign_keys=[invited_by_user_id])
    roster: Mapped["Roster | None"] = relationship("Roster")

    @classmethod
    def create_invitation(
        cls,
        team_id: int,
        invited_email: str,
        invited_by_user_id: int,
        token_hash: str,
        expires_in_hours: int = 72,
        roster_id: int | None = None,
        invited_role_level: str | None = None,
    ) -> "TeamInvitationToken":
        """Create a new team invitation token.

        Args:
            team_id: ID of the team
            invited_email: Email of the invited user
            invited_by_user_id: ID of the user sending the invitation
            token_hash: SHA-256 hash of the token
            expires_in_hours: Hours until expiration (default: 72)
            roster_id: If roster member invitation, the roster record ID
            invited_role_level: Role to assign (defaults to MEMBER if None)

        Returns:
            New TeamInvitationToken instance
        """
        return cls(
            team_id=team_id,
            invited_email=invited_email.lower(),  # Normalize email to lowercase
            invited_by_user_id=invited_by_user_id,
            token_hash=token_hash,
            expires_at=datetime.now(tz=UTC) + timedelta(hours=expires_in_hours),
            roster_id=roster_id,
            invited_role_level=invited_role_level,
        )

    def is_valid(self) -> bool:
        """Check if invitation is valid (not expired, not accepted)."""
        now = datetime.now(tz=UTC)
        return self.expires_at > now and self.accepted_at is None

    def mark_as_accepted(self) -> None:
        """Mark this invitation as accepted."""
        self.accepted_at = datetime.now(tz=UTC)
