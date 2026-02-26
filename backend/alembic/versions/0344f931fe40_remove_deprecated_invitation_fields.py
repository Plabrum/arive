"""remove deprecated invitation fields

Revision ID: 0344f931fe40
Revises: 9e98993e91a5
Create Date: 2026-01-11 01:38:14.914888

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0344f931fe40"
down_revision: str | Sequence[str] | None = "9e98993e91a5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the old unique indexes
    op.drop_index("ix_team_invitation_pending", table_name="team_invitation_tokens")
    op.drop_index("ix_roster_invitation_pending", table_name="team_invitation_tokens")

    # Drop the roster_id foreign key constraint
    op.drop_constraint("team_invitation_tokens_roster_id_fkey", "team_invitation_tokens", type_="foreignkey")

    # Drop the deprecated columns
    op.drop_column("team_invitation_tokens", "roster_id")
    op.drop_column("team_invitation_tokens", "invited_role_level")

    # Create new universal unique index based on invitation_type
    op.create_index(
        "ix_invitation_pending_unique",
        "team_invitation_tokens",
        ["team_id", "invited_email", "invitation_type"],
        unique=True,
        postgresql_where=sa.text("accepted_at IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Note: This downgrade is for rollback purposes only
    # Re-adding these columns won't restore the data

    # Drop the new universal index
    op.drop_index("ix_invitation_pending_unique", table_name="team_invitation_tokens")

    # Re-add the deprecated columns
    op.add_column("team_invitation_tokens", sa.Column("invited_role_level", sa.Text(), nullable=True))
    op.add_column("team_invitation_tokens", sa.Column("roster_id", sa.Integer(), nullable=True))

    # Re-add the foreign key
    op.create_foreign_key(
        "team_invitation_tokens_roster_id_fkey",
        "team_invitation_tokens",
        "roster",
        ["roster_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Re-add the old indexes
    op.create_index(
        "ix_team_invitation_pending",
        "team_invitation_tokens",
        ["team_id", "invited_email"],
        unique=True,
        postgresql_where=sa.text("accepted_at IS NULL AND roster_id IS NULL"),
    )
    op.create_index(
        "ix_roster_invitation_pending",
        "team_invitation_tokens",
        ["team_id", "roster_id", "invited_email"],
        unique=True,
        postgresql_where=sa.text("accepted_at IS NULL AND roster_id IS NOT NULL"),
    )
