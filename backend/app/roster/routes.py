import logging
from datetime import UTC

from litestar import Request, Response, Router, get, post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.enums import ActionGroupType
from app.actions.registry import ActionRegistry
from app.addresses.schemas import AddressSchema
from app.auth.guards import requires_session
from app.roster.models import Roster
from app.roster.schemas import RosterSchema, RosterUpdateSchema
from app.threads.models import Thread
from app.utils.db import get_or_404, update_model
from app.utils.sqids import Sqid

logger = logging.getLogger(__name__)


@get("/{id:str}")
async def get_roster(
    id: Sqid,
    request: Request,
    transaction: AsyncSession,
    action_registry: ActionRegistry,
) -> RosterSchema:
    """Get a roster member by SQID."""
    from sqlalchemy.orm import joinedload, selectinload

    roster = await get_or_404(
        transaction,
        Roster,
        id,
        load_options=[
            joinedload(Roster.address),
            joinedload(Roster.thread).options(
                selectinload(Thread.messages),
                selectinload(Thread.read_statuses),
            ),
        ],
    )

    # Compute actions for this roster member
    action_group = action_registry.get_class(ActionGroupType.RosterActions)
    actions = action_group.get_available_actions(obj=roster)

    # Convert thread to unread info using the mixin method
    thread_info = roster.get_thread_unread_info(request.user)

    # Convert address to schema
    address_schema = None
    if roster.address:
        address_schema = AddressSchema(
            id=roster.address.id,
            address1=roster.address.address1,
            address2=roster.address.address2,
            city=roster.address.city,
            state=roster.address.state,
            zip=roster.address.zip,
            country=roster.address.country,
            address_type=roster.address.address_type,
            created_at=roster.address.created_at,
            updated_at=roster.address.updated_at,
            team_id=roster.address.team_id,
        )

    # Compute city from address
    city = roster.address.city if roster.address else None

    # Compute age from birthdate
    age = None
    if roster.birthdate:
        from datetime import datetime

        today = datetime.now(tz=UTC).date()
        age = (today - roster.birthdate).days // 365

    return RosterSchema(
        id=roster.id,
        name=roster.name,
        email=roster.email,
        phone=roster.phone,
        birthdate=roster.birthdate,
        gender=roster.gender,
        address=address_schema,
        instagram_handle=roster.instagram_handle,
        facebook_handle=roster.facebook_handle,
        tiktok_handle=roster.tiktok_handle,
        youtube_channel=roster.youtube_channel,
        profile_photo_id=roster.profile_photo_id,
        state=roster.state.name,
        created_at=roster.created_at,
        updated_at=roster.updated_at,
        team_id=roster.team_id,
        actions=actions,
        thread=thread_info,
        city=city,
        age=age,
    )


@post("/{id:str}")
async def update_roster(
    id: Sqid, data: RosterUpdateSchema, request: Request, transaction: AsyncSession
) -> RosterSchema:
    """Update a roster member by SQID."""
    from sqlalchemy.orm import joinedload

    roster = await get_or_404(
        transaction,
        Roster,
        id,
        load_options=[joinedload(Roster.address)],
    )
    await update_model(
        session=transaction,
        model_instance=roster,
        update_vals=data,
        user_id=request.user,
        team_id=roster.team_id,
    )

    # Convert address to schema
    address_schema = None
    if roster.address:
        address_schema = AddressSchema(
            id=roster.address.id,
            address1=roster.address.address1,
            address2=roster.address.address2,
            city=roster.address.city,
            state=roster.address.state,
            zip=roster.address.zip,
            country=roster.address.country,
            address_type=roster.address.address_type,
            created_at=roster.address.created_at,
            updated_at=roster.address.updated_at,
            team_id=roster.address.team_id,
        )

    # Compute city from address
    city = roster.address.city if roster.address else None

    # Compute age from birthdate
    age = None
    if roster.birthdate:
        from datetime import datetime

        today = datetime.now(tz=UTC).date()
        age = (today - roster.birthdate).days // 365

    return RosterSchema(
        id=roster.id,
        name=roster.name,
        email=roster.email,
        phone=roster.phone,
        birthdate=roster.birthdate,
        gender=roster.gender,
        address=address_schema,
        instagram_handle=roster.instagram_handle,
        facebook_handle=roster.facebook_handle,
        tiktok_handle=roster.tiktok_handle,
        youtube_channel=roster.youtube_channel,
        profile_photo_id=roster.profile_photo_id,
        state=roster.state.name,
        created_at=roster.created_at,
        updated_at=roster.updated_at,
        team_id=roster.team_id,
        actions=[],  # Update endpoints don't compute actions
        city=city,
        age=age,
    )


@get("/invitations/accept", guards=[])
async def accept_roster_invitation(
    request: Request,
    transaction: AsyncSession,
    token: str,
) -> Response:
    """Accept a roster member invitation and create/link user account."""
    from litestar.exceptions import HTTPException
    from litestar.status_codes import HTTP_302_FOUND, HTTP_400_BAD_REQUEST

    from app.auth.crypto import hash_token
    from app.auth.enums import ScopeType
    from app.auth.models import TeamInvitationToken
    from app.roster.models import Roster
    from app.roster.utils import verify_roster_invitation_token
    from app.users.enums import RoleLevel, UserStates
    from app.users.models import Role, User
    from app.utils.configure import config

    if not token:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Missing token parameter",
        )

    invitation_data = await verify_roster_invitation_token(transaction, token)

    if not invitation_data:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation. Please request a new invitation.",
        )

    roster_id = invitation_data["roster_id"]
    team_id = invitation_data["team_id"]
    invited_email = invitation_data["invited_email"]

    # Get the roster record
    roster = await get_or_404(transaction, Roster, roster_id)

    # Check if user exists for this email
    user_stmt = select(User).where(User.email == invited_email)
    user_result = await transaction.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if not user:
        user = User(
            email=invited_email,
            name=roster.name,
            email_verified=True,
        )
        transaction.add(user)
        await transaction.flush()
        logger.info(f"Created new user {user.id} for roster member {roster_id}")
    else:
        if not user.email_verified:
            user.email_verified = True
            logger.info(f"Marked user {user.id} email as verified")

    # Link user to roster record
    roster.roster_user_id = user.id

    # Get the role level from invitation (defaults to ROSTER_MEMBER)
    invited_role_level = invitation_data.get("invited_role_level", RoleLevel.ROSTER_MEMBER)

    # Check if user already has a role in this team
    role_check_stmt = select(Role).where(
        Role.user_id == user.id,
        Role.team_id == team_id,
    )
    role_check_result = await transaction.execute(role_check_stmt)
    existing_role = role_check_result.scalar_one_or_none()

    if existing_role:
        existing_role.role_level = invited_role_level
        logger.info(f"Updated user {user.id} role to {invited_role_level} in team {team_id}")
    else:
        role = Role(
            user_id=user.id,
            team_id=team_id,
            role_level=invited_role_level,
        )
        transaction.add(role)
        logger.info(f"Added user {user.id} to team {team_id} as {invited_role_level}")

    if user.state == UserStates.NEEDS_TEAM:
        user.state = UserStates.ACTIVE
        logger.info(f"Updated user {user.id} state to ACTIVE")

    # Mark invitation as accepted
    token_hash = hash_token(token)
    invitation_stmt = select(TeamInvitationToken).where(TeamInvitationToken.token_hash == token_hash).with_for_update()
    invitation_result = await transaction.execute(invitation_stmt)
    invitation_token = invitation_result.scalar_one_or_none()

    if invitation_token:
        invitation_token.mark_as_accepted()
        logger.info(f"Marked roster invitation as accepted for user {user.id}")

    # Create secure session with TEAM scope
    request.session["user_id"] = int(user.id)
    request.session["authenticated"] = True
    request.session["scope_type"] = ScopeType.TEAM.value
    request.session["team_id"] = int(team_id)

    frontend_url = config.SUCCESS_REDIRECT_URL
    logger.info(f"User {user.id} accepted roster invitation, redirecting to {frontend_url}")

    from litestar import Response

    return Response(
        content="",
        status_code=HTTP_302_FOUND,
        headers={"Location": frontend_url},
    )


roster_router = Router(
    path="/roster",
    guards=[requires_session],
    route_handlers=[
        get_roster,
        update_roster,
        accept_roster_invitation,
    ],
    tags=["roster"],
)
