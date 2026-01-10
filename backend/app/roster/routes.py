import logging
from datetime import UTC

from litestar import Request, Router, get, post
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


roster_router = Router(
    path="/roster",
    guards=[requires_session],
    route_handlers=[
        get_roster,
        update_roster,
    ],
    tags=["roster"],
)
