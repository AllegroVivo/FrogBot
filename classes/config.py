from __future__ import annotations

from discord    import Embed, TextChannel
from typing     import TYPE_CHECKING, List, Type, TypeVar

from utilities  import *

if TYPE_CHECKING:
    from classes.guild  import GuildData
################################################################################

__all__ = ("GuildConfiguration", )

GC = TypeVar("GC", bound="GuildConfiguration")

################################################################################
class GuildConfiguration:

    __slots__ = (
        "parent",
        "profile_channels"
    )

################################################################################
    def __init__(self, parent: GuildData, profile_channels: List[TextChannel]):

        self.parent: GuildData = parent
        self.profile_channels: List[TextChannel] = profile_channels

################################################################################
    @classmethod
    def load(cls: Type[GC], parent: GuildData, data: List[TextChannel]) -> GC:

        return cls(
            parent=parent,
            profile_channels=data
        )

################################################################################
    def status(self) -> Embed:

        description = str(NS)
        if self.profile_channels:
            description = "- " + "\n- ".join([c.mention for c in self.profile_channels])

        return make_embed(
            title="Available Profile Posting Channels",
            description=(
                f"{draw_separator(extra=20)}\n"
                f"{description}"
            ),
            timestamp=False
        )

################################################################################
    @property
    def post_channel_ids(self):

        return [c.id for c in self.profile_channels]

################################################################################
    def add_profile_channel(self, channel: TextChannel) -> None:

        if channel.id not in self.post_channel_ids:
            self.profile_channels.append(channel)
            self.update()

################################################################################
    def remove_profile_channel(self, channel: TextChannel) -> None:

        for i, c in enumerate(self.profile_channels):
            if c.id == channel.id:
                self.profile_channels.pop(i)
                self.update()
                return

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE guild_config SET post_channels = %s WHERE guild_id = %s",
            (self.post_channel_ids, self.parent.guild_id)
        )

        db_connection.commit()
        c.close()

        return

################################################################################
