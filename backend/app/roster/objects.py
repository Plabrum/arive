from datetime import UTC, datetime

from sqlalchemy.orm import joinedload

from app.actions.enums import ActionGroupType
from app.objects.base import BaseObject
from app.objects.enums import ObjectTypes
from app.objects.schemas import (
    EmailFieldValue,
    EnumFieldValue,
    FieldType,
    IntFieldValue,
    ObjectColumn,
    PhoneFieldValue,
    StringFieldValue,
    media_to_image_field_value,
)
from app.roster.enums import RosterStates
from app.roster.models import Roster


class RosterObject(BaseObject[Roster]):
    object_type = ObjectTypes.Roster

    @classmethod
    def model(cls) -> type[Roster]:
        return Roster

    @classmethod
    def title_field(cls, obj: Roster) -> str:
        return obj.name

    @classmethod
    def subtitle_field(cls, obj: Roster) -> str:
        return obj.instagram_handle or ""

    @classmethod
    def state_field(cls, obj: Roster) -> str:
        return obj.state

    # Action groups
    top_level_action_group = ActionGroupType.RosterActions

    # Load options
    load_options = [joinedload(Roster.user), joinedload(Roster.profile_photo), joinedload(Roster.address)]

    column_definitions = [
        ObjectColumn(
            key="name",
            label="Name",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.name),
            sortable=True,
            default_visible=True,
            editable=False,
            include_in_list=True,
        ),
        ObjectColumn(
            key="email",
            label="Email",
            type=FieldType.Email,
            value=lambda obj: EmailFieldValue(value=obj.email) if obj.email else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="phone",
            label="Phone",
            type=FieldType.Phone,
            value=lambda obj: PhoneFieldValue(value=obj.phone) if obj.phone else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="gender",
            label="Gender",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.gender) if obj.gender else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="age",
            label="Age",
            type=FieldType.Int,
            value=lambda obj: (
                IntFieldValue(value=(datetime.now(tz=UTC).date() - obj.birthdate).days // 365)
                if obj.birthdate
                else None
            ),
            sortable=False,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="city",
            label="City",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.address.city) if obj.address else None,
            sortable=False,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="instagram_handle",
            label="Instagram",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.instagram_handle) if obj.instagram_handle else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="state",
            label="Status",
            type=FieldType.Enum,
            value=lambda obj: EnumFieldValue(value=obj.state),
            sortable=True,
            default_visible=True,
            available_values=[e.name for e in RosterStates],
            editable=False,
            include_in_list=True,
        ),
        ObjectColumn(
            key="profile_photo",
            label="Profile Photo",
            type=FieldType.Image,
            value=lambda obj: media_to_image_field_value(
                obj.profile_photo,
                BaseObject.registry.dependencies["s3_client"],
            )
            if obj.profile_photo
            else None,
            sortable=False,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="facebook_handle",
            label="Facebook",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.facebook_handle) if obj.facebook_handle else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="tiktok_handle",
            label="TikTok",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.tiktok_handle) if obj.tiktok_handle else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
        ObjectColumn(
            key="youtube_channel",
            label="YouTube",
            type=FieldType.String,
            value=lambda obj: StringFieldValue(value=obj.youtube_channel) if obj.youtube_channel else None,
            sortable=True,
            default_visible=True,
            editable=False,
            nullable=True,
            include_in_list=True,
        ),
    ]
