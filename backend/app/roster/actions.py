from datetime import UTC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.actions import (
    ActionGroupType,
    BaseObjectAction,
    BaseTopLevelAction,
    action_group_factory,
)
from app.actions.base import EmptyActionData
from app.actions.deps import ActionDeps
from app.actions.enums import ActionIcon
from app.actions.schemas import ActionExecutionResponse
from app.addresses.models import Address
from app.roster.enums import RosterActions
from app.roster.models import Roster
from app.roster.schemas import InviteRosterMemberSchema, RosterCreateSchema, RosterUpdateSchema
from app.utils.db import update_model

# Create roster action group
roster_actions = action_group_factory(
    ActionGroupType.RosterActions,
    default_invalidation="/o/roster",
    model_type=Roster,
    load_options=[joinedload(Roster.address)],
)


@roster_actions
class DeleteRoster(BaseObjectAction[Roster, EmptyActionData]):
    action_key = RosterActions.delete
    label = "Delete"
    is_bulk_allowed = True
    priority = 0
    icon = ActionIcon.trash
    confirmation_message = "Are you sure you want to delete this roster member?"
    should_redirect_to_parent = True

    @classmethod
    async def execute(
        cls, obj: Roster, data: EmptyActionData, transaction: AsyncSession, deps
    ) -> ActionExecutionResponse:
        from datetime import datetime

        # Soft delete by setting deleted_at
        obj.deleted_at = datetime.now(tz=UTC)
        await transaction.flush()
        return ActionExecutionResponse(
            message="Deleted roster member",
        )


@roster_actions
class UpdateRoster(BaseObjectAction[Roster, RosterUpdateSchema]):
    action_key = RosterActions.update
    label = "Edit"
    is_bulk_allowed = True
    priority = 50
    icon = ActionIcon.edit

    @classmethod
    async def execute(
        cls,
        obj: Roster,
        data: RosterUpdateSchema,
        transaction: AsyncSession,
        deps: ActionDeps,
    ) -> ActionExecutionResponse:
        # Handle creation of new address (update_model can't auto-create)
        if data.address and not obj.address:
            obj.address = Address(
                team_id=obj.team_id,
                address1=data.address.address1,
                address2=data.address.address2,
                city=data.address.city,
                state=data.address.state,
                zip=data.address.zip,
                country=data.address.country,
                address_type=data.address.address_type,
            )

        await update_model(
            session=transaction,
            model_instance=obj,
            update_vals=data,
            user_id=deps.user,
            team_id=obj.team_id,
        )

        return ActionExecutionResponse(
            message="Updated roster member",
        )


@roster_actions
class CreateRoster(BaseTopLevelAction[RosterCreateSchema]):
    action_key = RosterActions.create
    label = "Create Roster Member"
    is_bulk_allowed = False
    priority = 1
    icon = ActionIcon.add

    @classmethod
    async def execute(
        cls,
        data: RosterCreateSchema,
        transaction: AsyncSession,
        deps: ActionDeps,
    ) -> ActionExecutionResponse:
        roster = Roster(
            user_id=deps.user,
            team_id=deps.team_id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            birthdate=data.birthdate,
            gender=data.gender,
            instagram_handle=data.instagram_handle,
            facebook_handle=data.facebook_handle,
            tiktok_handle=data.tiktok_handle,
            youtube_channel=data.youtube_channel,
            profile_photo_id=data.profile_photo_id,
        )

        if data.address:
            roster.address = Address(
                team_id=deps.team_id,
                address1=data.address.address1,
                address2=data.address.address2,
                city=data.address.city,
                state=data.address.state,
                zip=data.address.zip,
                country=data.address.country,
                address_type=data.address.address_type,
            )

        transaction.add(roster)
        await transaction.flush()
        return ActionExecutionResponse(
            message="Created roster member",
            created_id=roster.id,
        )


@roster_actions
class InviteRosterMember(BaseObjectAction[Roster, InviteRosterMemberSchema]):
    action_key = RosterActions.invite_member
    label = "Invite to Portal"
    is_bulk_allowed = False
    priority = 75
    icon = ActionIcon.send
    confirmation_message = None
    should_redirect_to_parent = False

    @classmethod
    def is_available(cls, obj: Roster | None, deps: ActionDeps) -> bool:
        """Available if roster has email and no existing user login."""
        if obj is None or obj.is_deleted:
            return False
        return obj.email is not None and obj.roster_user_id is None

    @classmethod
    async def execute(
        cls,
        obj: Roster,
        data: InviteRosterMemberSchema,
        transaction: AsyncSession,
        deps: ActionDeps,
    ) -> ActionExecutionResponse:
        from litestar.exceptions import HTTPException
        from litestar.status_codes import HTTP_400_BAD_REQUEST
        from sqlalchemy import select

        from app.auth.models import TeamInvitationToken
        from app.users.models import User

        if not obj.email:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Roster member must have an email address",
            )

        invited_email = obj.email.lower().strip()

        # Check for pending roster invitation
        pending_invitation_stmt = select(TeamInvitationToken).where(
            TeamInvitationToken.roster_id == obj.id,
            TeamInvitationToken.accepted_at.is_(None),
        )
        pending_invitation_result = await transaction.execute(pending_invitation_stmt)
        existing_invitation = pending_invitation_result.scalar_one_or_none()

        if existing_invitation and existing_invitation.is_valid():
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"An invitation is already pending for {invited_email}",
            )

        # Generate invitation link using universal service
        from app.invitations import InvitationType, generate_invitation_link

        invitation_link = await generate_invitation_link(
            db_session=transaction,
            team_id=int(obj.team_id),
            invited_email=invited_email,
            invited_by_user_id=int(deps.user),
            invitation_type=InvitationType.ROSTER_MEMBER,
            invitation_context={"roster_id": int(obj.id)},
            expires_in_hours=72,
        )

        # Get inviter name for email
        inviter_stmt = select(User).where(User.id == deps.user)
        inviter_result = await transaction.execute(inviter_stmt)
        inviter = inviter_result.scalar_one()

        # Send invitation email
        await deps.email_service.send_roster_invitation_email(
            to_email=invited_email,
            roster_name=obj.name,
            inviter_name=inviter.name,
            invitation_link=invitation_link,
            expires_hours=72,
        )

        return ActionExecutionResponse(
            message=f"Portal invitation sent to {invited_email}. It will expire in 72 hours.",
        )
