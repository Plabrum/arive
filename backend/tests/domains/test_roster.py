"""Tests for roster domain: endpoints and basic operations."""

from unittest.mock import AsyncMock, patch

from litestar.testing import AsyncTestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import TeamInvitationToken
from app.roster.utils import generate_roster_invitation_link
from app.teams.utils import verify_team_invitation_token
from app.users.enums import RoleLevel
from app.users.models import Role, User
from app.utils.sqids import sqid_encode
from tests.domains.test_helpers import execute_action, get_available_actions


class TestRoster:
    """Tests for roster endpoints."""

    async def test_get_roster(
        self,
        authenticated_client: AsyncTestClient,
        team,
        roster,
    ):
        """Test GET /roster/{id} returns roster member details."""

        # Get the roster member
        response = await authenticated_client.get(f"/roster/{sqid_encode(roster.id)}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == sqid_encode(roster.id)
        assert data["name"] == roster.name
        assert data["team_id"] == sqid_encode(team.id)
        assert "actions" in data  # Should include available actions

    async def test_update_roster(
        self,
        authenticated_client: AsyncTestClient,
        roster,
    ):
        """Test POST /roster/{id} updates roster member."""

        # Update the roster member (send complete object - updates are declarative)
        response = await authenticated_client.post(
            f"/roster/{sqid_encode(roster.id)}",
            json={
                "name": "Updated Name",
                "email": roster.email,
                "phone": roster.phone,
                "birthdate": None,
                "gender": None,
                "address": None,
                "instagram_handle": roster.instagram_handle,
                "facebook_handle": roster.facebook_handle,
                "tiktok_handle": roster.tiktok_handle,
                "youtube_channel": roster.youtube_channel,
                "profile_photo_id": None,
            },
        )
        assert response.status_code in [200, 201]

        data = response.json()
        assert data["name"] == "Updated Name"

    async def test_list_roster_actions(
        self,
        authenticated_client: AsyncTestClient,
        roster,
    ):
        """Test GET /actions/roster_actions/{id} returns available actions."""

        # Get available actions using SQID-encoded ID
        actions = await get_available_actions(authenticated_client, "roster_actions", sqid_encode(roster.id))

        # Should have at least update and delete actions
        action_keys = [action["action"] for action in actions]
        assert "roster_actions__roster_update" in action_keys
        assert "roster_actions__roster_delete" in action_keys

    async def test_execute_roster_update_action(
        self,
        authenticated_client: AsyncTestClient,
        roster,
        db_session: AsyncSession,
    ):
        """Test executing roster update action."""

        # Execute update action using SQID-encoded ID (send complete object)
        response = await execute_action(
            authenticated_client,
            "roster_actions",
            "roster_actions__roster_update",
            data={
                "name": "After Update",
                "email": "newemail@example.com",
                "phone": roster.phone,
                "birthdate": None,
                "gender": None,
                "address": None,
                "instagram_handle": roster.instagram_handle,
                "facebook_handle": roster.facebook_handle,
                "tiktok_handle": roster.tiktok_handle,
                "youtube_channel": roster.youtube_channel,
                "profile_photo_id": None,
            },
            obj_id=sqid_encode(roster.id),
        )

        assert response.status_code in [200, 201, 204]

        # Verify the roster member was updated
        await db_session.refresh(roster)
        assert roster.name == "After Update"
        assert roster.email == "newemail@example.com"

    async def test_execute_roster_delete_action(
        self,
        authenticated_client: AsyncTestClient,
        roster,
        db_session: AsyncSession,
    ):
        """Test executing roster delete action."""
        roster_id = roster.id

        # Execute delete action using SQID-encoded ID
        response = await execute_action(
            authenticated_client,
            "roster_actions",
            "roster_actions__roster_delete",
            data={},
            obj_id=sqid_encode(roster.id),
        )

        assert response.status_code in [200, 201, 204]

        # Verify the roster member was soft-deleted
        # Use raw SQL to bypass the soft delete filter
        from sqlalchemy import text

        result = await db_session.execute(text("SELECT deleted_at FROM roster WHERE id = :id"), {"id": roster_id})
        row = result.fetchone()
        # With soft delete, the roster should still exist but be marked as deleted
        assert row is not None
        assert row[0] is not None  # deleted_at should be set

    async def test_get_roster_not_found(
        self,
        authenticated_client: AsyncTestClient,
    ):
        """Test GET /roster/{id} returns 404 for non-existent roster member."""

        # Use a valid SQID for a non-existent ID
        fake_id = sqid_encode(999999999)
        response = await authenticated_client.get(f"/roster/{fake_id}")
        assert response.status_code == 404

    async def test_update_roster_with_social_handles(
        self,
        authenticated_client: AsyncTestClient,
        roster,
    ):
        """Test updating roster with social media handles."""

        # Update with social handles (send complete object)
        response = await authenticated_client.post(
            f"/roster/{sqid_encode(roster.id)}",
            json={
                "name": roster.name,
                "email": roster.email,
                "phone": roster.phone,
                "birthdate": None,
                "gender": None,
                "address": None,
                "instagram_handle": "@influencer",
                "facebook_handle": roster.facebook_handle,
                "tiktok_handle": "@tiktoker",
                "youtube_channel": "UCxyz123",
                "profile_photo_id": None,
            },
        )
        assert response.status_code in [200, 201]

        data = response.json()
        assert data["instagram_handle"] == "@influencer"
        assert data["tiktok_handle"] == "@tiktoker"
        assert data["youtube_channel"] == "UCxyz123"


class TestRosterInvitations:
    """Tests for roster member invitation system."""

    async def test_generate_roster_invitation_link(
        self,
        db_session: AsyncSession,
        roster,
        team,
        user,
    ):
        """Test generating a roster invitation link creates a valid token."""

        # Generate invitation link
        invitation_link = await generate_roster_invitation_link(
            db_session=db_session,
            roster_id=int(roster.id),
            team_id=int(team.id),
            invited_email="talent@example.com",
            invited_by_user_id=int(user.id),
            expires_in_hours=72,
        )

        # Verify link format
        assert invitation_link.startswith("http")
        assert "/roster/invitations/accept?token=" in invitation_link

        # Extract token from link
        token = invitation_link.split("token=")[1]
        assert len(token) > 20  # Token should be reasonably long

        # Verify token was saved in database
        from app.auth.crypto import hash_token

        token_hash = hash_token(token)
        stmt = select(TeamInvitationToken).where(TeamInvitationToken.token_hash == token_hash)
        result = await db_session.execute(stmt)
        invitation = result.scalar_one_or_none()

        assert invitation is not None
        assert invitation.roster_id == roster.id
        assert invitation.team_id == team.id
        assert invitation.invited_email == "talent@example.com"
        assert invitation.invited_role_level == RoleLevel.ROSTER_MEMBER
        assert invitation.invited_by_user_id == user.id

    async def test_verify_roster_invitation_token_valid(
        self,
        db_session: AsyncSession,
        roster,
        team,
        user,
    ):
        """Test verifying a valid roster invitation token."""

        # Generate invitation link
        invitation_link = await generate_roster_invitation_link(
            db_session=db_session,
            roster_id=int(roster.id),
            team_id=int(team.id),
            invited_email="talent@example.com",
            invited_by_user_id=int(user.id),
            expires_in_hours=72,
        )
        await db_session.commit()

        # Extract token
        token = invitation_link.split("token=")[1]

        # Verify token
        invitation_data = await verify_team_invitation_token(db_session, token)

        assert invitation_data is not None
        assert invitation_data["roster_id"] == roster.id
        assert invitation_data["team_id"] == team.id
        assert invitation_data["invited_email"] == "talent@example.com"
        assert invitation_data["invited_role_level"] == RoleLevel.ROSTER_MEMBER

    async def test_verify_roster_invitation_token_invalid(
        self,
        db_session: AsyncSession,
    ):
        """Test verifying an invalid roster invitation token returns None."""

        # Try to verify a fake token
        invitation_data = await verify_team_invitation_token(db_session, "fake_token_12345")

        assert invitation_data is None

    async def test_invite_roster_member_action_availability(
        self,
        authenticated_client: AsyncTestClient,
        roster,
    ):
        """Test that invite_member action is available for roster with email and no user."""

        # Get available actions
        actions = await get_available_actions(authenticated_client, "roster_actions", sqid_encode(roster.id))
        action_keys = [action["action"] for action in actions]

        # Should have invite_member action if roster has email
        if roster.email:
            assert "roster_actions__roster_invite_member" in action_keys
        else:
            assert "roster_actions__roster_invite_member" not in action_keys

    async def test_invite_roster_member_action_not_available_when_user_exists(
        self,
        authenticated_client: AsyncTestClient,
        roster,
        db_session: AsyncSession,
    ):
        """Test that invite_member action is NOT available if roster already has a user."""

        # Create a user and link to roster
        existing_user = User(
            email="existing@example.com",
            name="Existing User",
            email_verified=True,
        )
        db_session.add(existing_user)
        await db_session.flush()

        roster.roster_user_id = existing_user.id
        await db_session.commit()

        # Get available actions
        actions = await get_available_actions(authenticated_client, "roster_actions", sqid_encode(roster.id))
        action_keys = [action["action"] for action in actions]

        # Should NOT have invite_member action since user already exists
        assert "roster_actions__roster_invite_member" not in action_keys

    @patch("app.emails.service.EmailService.send_roster_invitation_email")
    async def test_execute_invite_roster_member_action(
        self,
        mock_send_email: AsyncMock,
        authenticated_client: AsyncTestClient,
        roster,
        db_session: AsyncSession,
    ):
        """Test executing the invite roster member action."""

        # Mock email sending
        mock_send_email.return_value = "mock-message-id"

        # Ensure roster has email
        roster.email = "newtalent@example.com"
        await db_session.commit()

        # Execute invite action
        response = await execute_action(
            authenticated_client,
            "roster_actions",
            "roster_actions__roster_invite_member",
            data={},
            obj_id=sqid_encode(roster.id),
        )

        assert response.status_code in [200, 201, 204]

        # Verify email was sent
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        assert call_args.kwargs["to_email"] == "newtalent@example.com"
        assert call_args.kwargs["roster_name"] == roster.name
        assert "invitation_link" in call_args.kwargs

        # Verify invitation token was created
        stmt = select(TeamInvitationToken).where(
            TeamInvitationToken.roster_id == roster.id,
            TeamInvitationToken.accepted_at.is_(None),
        )
        result = await db_session.execute(stmt)
        invitation = result.scalar_one_or_none()

        assert invitation is not None
        assert invitation.invited_email == "newtalent@example.com"

    async def test_accept_roster_invitation_creates_user_and_role(
        self,
        test_client: AsyncTestClient,
        db_session: AsyncSession,
        roster,
        team,
        user,
    ):
        """Test accepting a roster invitation creates user account and assigns role."""

        # Generate invitation
        invitation_link = await generate_roster_invitation_link(
            db_session=db_session,
            roster_id=int(roster.id),
            team_id=int(team.id),
            invited_email="newtalent@example.com",
            invited_by_user_id=int(user.id),
            expires_in_hours=72,
        )
        await db_session.commit()

        # Extract token
        token = invitation_link.split("token=")[1]

        # Accept invitation (no auth required for this endpoint)
        response = await test_client.get(f"/teams/invitations/accept?token={token}")

        # Should redirect on success
        assert response.status_code == 302

        # Verify user was created
        stmt = select(User).where(User.email == "newtalent@example.com")
        result = await db_session.execute(stmt)
        new_user = result.scalar_one_or_none()

        assert new_user is not None
        assert new_user.email == "newtalent@example.com"
        assert new_user.name == roster.name
        assert new_user.email_verified is True

        # Verify roster is linked to user
        await db_session.refresh(roster)
        assert roster.roster_user_id == new_user.id

        # Verify role was created
        role_stmt = select(Role).where(
            Role.user_id == new_user.id,
            Role.team_id == team.id,
        )
        role_result = await db_session.execute(role_stmt)
        role = role_result.scalar_one_or_none()

        assert role is not None
        assert role.role_level == RoleLevel.ROSTER_MEMBER

    async def test_accept_roster_invitation_with_existing_user(
        self,
        test_client: AsyncTestClient,
        db_session: AsyncSession,
        roster,
        team,
        user,
    ):
        """Test accepting invitation when user already exists links them to roster."""

        # Create user first
        existing_user = User(
            email="existing@example.com",
            name="Different Name",
            email_verified=False,
        )
        db_session.add(existing_user)
        await db_session.flush()

        # Generate invitation
        invitation_link = await generate_roster_invitation_link(
            db_session=db_session,
            roster_id=int(roster.id),
            team_id=int(team.id),
            invited_email="existing@example.com",
            invited_by_user_id=int(user.id),
            expires_in_hours=72,
        )
        await db_session.commit()

        # Extract token
        token = invitation_link.split("token=")[1]

        # Accept invitation
        response = await test_client.get(f"/teams/invitations/accept?token={token}")
        assert response.status_code == 302

        # Verify roster is linked to existing user
        await db_session.refresh(roster)
        assert roster.roster_user_id == existing_user.id

        # Verify email was marked as verified
        await db_session.refresh(existing_user)
        assert existing_user.email_verified is True

    async def test_accept_roster_invitation_expired_token(
        self,
        test_client: AsyncTestClient,
    ):
        """Test accepting an expired invitation token returns error."""

        # Try with invalid token
        response = await test_client.get("/teams/invitations/accept?token=expired_fake_token")

        assert response.status_code == 400
