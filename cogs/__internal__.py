from __future__ import annotations

from discord        import Cog, Guild, TextChannel
from discord.abc    import GuildChannel
from typing         import TYPE_CHECKING

from classes.guild  import GuildData
from utilities      import *

if TYPE_CHECKING:
    from classes.bot    import FrogBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: FrogBot):

        self.bot: FrogBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def on_ready(self) -> None:

        print("Fetching internal channels...")
        await self.bot.load_frog_channels()

        print("Asserting database structure...")
        assert_db_structure()

        print("Asserting guild records...")
        assert_guild_records(self.bot.guilds)

        print("Loading custom guild data...")
        for guild in self.bot.guilds:
            self.bot.frog_guilds.append(GuildData.load(guild))

        print("Loading guild configurations...")
        await self.bot.load_guilds()

        print("Loading profiles...")
        await self.bot.load_profiles()

        print("FrogBot Online!")

################################################################################
    @Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: Guild) -> None:

        print(f"Guild Joined! || {guild.id} -- {guild.name}")

        new_guild_entry(guild.id)

        print("Database Entry Created...")

################################################################################
    @Cog.listener("on_guild_channel_delete")
    async def on_guild_channel_delete(self, channel: GuildChannel):

        guild = self.bot.get_frog(channel.guild.id)

        for i, ch in enumerate(guild.config.profile_channels):
            if ch.id == channel.id:
                guild.config.profile_channels.pop(i)
                guild.config.update()
                return

################################################################################
def setup(bot: FrogBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
