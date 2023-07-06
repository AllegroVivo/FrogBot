from discord    import (
    ApplicationContext,
    ChannelType,
    Cog,
    Option,
    OptionChoice,
    SlashCommandGroup,
    SlashCommandOptionType
)
from typing     import TYPE_CHECKING

from ui         import *
from utilities  import *

if TYPE_CHECKING:
    from classes.bot    import FrogBot
################################################################################
class Configuration(Cog):

    def __init__(self, bot: "FrogBot"):

        self.bot: "FrogBot" = bot

################################################################################

    config = SlashCommandGroup(
        name="config",
        description="Commands pertaining to server-wide configuration."
    )

################################################################################
    @config.command(
        name="profile_channels",
        description="View a list of available profile posting channels for this server."
    )
    async def config_posting_channels(self, ctx: ApplicationContext) -> None:

        guild = self.bot.get_frog(ctx.guild_id)
        config = guild.config
        view = CloseMessageView(ctx.user)

        await ctx.respond(embed=config.status(), view=view)

################################################################################
    @config.command(
        name="post_channel",
        descripion="Add or Remove a profile posting channel."
    )
    async def config_posting_channel(
        self,
        ctx: ApplicationContext,
        op: Option(
            SlashCommandOptionType.string,
            name="operation",
            description="Whether to ADD or REMOVE an available profile posting channel.",
            required=True,
            choices=[
                OptionChoice("Add"),
                OptionChoice("Remove")
            ]
        ),
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The posting channel to ADD or REMOVE",
            required=True
        )
    ) -> None:

        if channel.type != ChannelType.text:
            error = ChannelTypeError("Text Channel")
            await ctx.respond(embed=error, ephemeral=True)
            return

        guild = self.bot.get_frog(ctx.guild_id)
        config = guild.config

        if op == "Add":
            config.add_profile_channel(channel)
        else:
            config.remove_profile_channel(channel)

        view = CloseMessageView(ctx.user)

        await ctx.respond(embed=config.status(), view=view)

        return

################################################################################
def setup(bot: "FrogBot") -> None:

    bot.add_cog(Configuration(bot))

################################################################################
