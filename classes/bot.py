from __future__ import annotations

from discord    import Attachment, Bot, NotFound, TextChannel
from typing     import TYPE_CHECKING, Dict, List, Optional, Tuple

from utilities  import convert_db_list, db_connection

from classes.profiles   import Profile
from classes.config     import GuildConfiguration

if TYPE_CHECKING:
    from classes.guild  import GuildData
################################################################################

__all__ = (
    "FrogBot",
)

################################################################################
class FrogBot(Bot):
    """Represents the main bot instance being run.

    Attributes
    -----------
    frog_guilds: :class:`list`
        A list of custom guild objects that hold data pertaining
        to bot features.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frog_guilds: List[GuildData] = []
        self.image_dump: Optional[TextChannel] = None

################################################################################
    async def load_guilds(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM guild_config")

        data = c.fetchall()
        c.close()

        for record in data:
            post_channel_ids = [int(c) for c in convert_db_list(record[1])]

            post_channels = []
            for ch in post_channel_ids:
                channel = await self.get_or_fetch_channel(ch)
                if channel is not None:
                    post_channels.append(channel)

            guild = self.get_frog(record[0])

            config = GuildConfiguration.load(guild, post_channels)
            guild.config = config

################################################################################
    async def load_profiles(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM profile_master")
        data = c.fetchall()

        for record in data:
            user = await self.get_or_fetch_user(record[1]) or record[1]

            for frog in self.frog_guilds:
                if frog.parent.id == record[2]:
                    profile = Profile.load(user, frog, record)
                    frog.profiles.append(profile)
                    break

        c.execute("SELECT * FROM addl_images")
        data = c.fetchall()
        c.close()

        additional_images: Dict[str, List[Tuple[str, str, str, Optional[str]]]] = {}
        for img in data:
            try:
                additional_images[img[0]].append(img)
            except KeyError:
                additional_images[img[0]] = [img]

        if additional_images:
            for profile_id in additional_images.keys():
                p = self._get_profile(profile_id)
                if p is None:
                    continue

                p.images.additional_images_from_data(additional_images[profile_id])

################################################################################
    def _get_profile(self, profile_id: str) -> Optional[Profile]:

        for frog in self.frog_guilds:
            for profile in frog.profiles:
                if profile.id == profile_id:
                    return profile

################################################################################
    async def load_frog_channels(self) -> None:

        # Image Dump
        try:
            self.image_dump = await self.fetch_channel(991902526188302427)
        except:
            raise

################################################################################
    async def dump_image(self, image: Attachment) -> str:

        file = await image.to_file()
        post = await self.image_dump.send(file=file)

        return post.attachments[0].url

################################################################################
    def get_frog(self, guild_id: int) -> GuildData:

        for frog in self.frog_guilds:
            if frog.parent.id == guild_id:
                return frog

################################################################################
    async def get_or_fetch_channel(self, channel_id: int) -> Optional[TextChannel]:

        ret = self.get_channel(channel_id)

        if ret is not None:
            return ret  # type: ignore

        try:
            return await self.fetch_channel(channel_id)  # type:ignore
        except NotFound:
            return None

################################################################################
