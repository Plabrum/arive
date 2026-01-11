"""Guest brand invitation handler (future implementation)."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.enums import RoleLevel

logger = logging.getLogger(__name__)


class GuestBrandInvitationHandler:
    """Handles guest brand invitations (future).

    Guest brands get access to their campaigns with GUEST_BRAND role.
    Post-accept: Link user to brand record.

    TODO: Implement when guest brand feature is added
    """

    @staticmethod
    def get_role_level() -> str:
        """Guest brands get GUEST_BRAND role (campaign-scoped access)."""
        return RoleLevel.GUEST_BRAND.value

    @staticmethod
    async def get_user_name(
        session: AsyncSession,
        invited_email: str,
        invitation_context: dict,
    ) -> str | None:
        """Get brand name for the new user account.

        TODO: Implement when Brand model exists

        Args:
            session: Database session
            invited_email: The email address of the invitee
            invitation_context: Must contain 'brand_id'

        Returns:
            None to use email prefix (not yet implemented)
        """
        return None  # TODO: Fetch from Brand model

    @staticmethod
    async def post_accept_hook(
        session: AsyncSession,
        user_id: int,
        team_id: int,
        invitation_context: dict,
    ) -> None:
        """Link user to brand record and campaigns.

        TODO: Implement when Brand model exists

        Args:
            session: Database session
            user_id: The user who accepted
            team_id: The team they're joining
            invitation_context: Must contain 'brand_id'
        """
        # from app.brands.models import Brand
        #
        # brand_id = invitation_context.get("brand_id")
        # if not brand_id:
        #     logger.warning(f"Brand invitation missing brand_id in context: {invitation_context}")
        #     return
        #
        # brand = await session.get(Brand, brand_id)
        # if brand:
        #     brand.brand_user_id = user_id
        #     logger.info(f"Linked brand {brand_id} to user {user_id}")
        # else:
        #     logger.warning(f"Brand {brand_id} not found for invitation")

        raise NotImplementedError("Guest brand invitations not yet implemented")

    @staticmethod
    async def validate_invitation_context(
        session: AsyncSession,
        context: dict,
    ) -> bool:
        """Ensure brand exists and has email.

        TODO: Implement when Brand model exists

        Args:
            session: Database session
            context: Must contain 'brand_id'

        Returns:
            True if brand exists and has email, False otherwise
        """
        # from app.brands.models import Brand
        #
        # brand_id = context.get("brand_id")
        # if not brand_id:
        #     return False
        #
        # brand = await session.get(Brand, brand_id)
        # return brand is not None and brand.email is not None

        raise NotImplementedError("Guest brand invitations not yet implemented")
