from discord        import (
    ApplicationContext,
    Cog,
    EmbedField,
    Option,
    OptionChoice,
    SlashCommandGroup,
    SlashCommandOptionType
)
from typing         import TYPE_CHECKING

from ui             import DetailsStatusView
from utilities      import *

from classes.profiles   import Profile, ProfileDetails

if TYPE_CHECKING:
    from classes.bot    import FrogBot
################################################################################
class Profiles(Cog):

    def __init__(self, bot: "FrogBot"):

        self.bot: "FrogBot" = bot

################################################################################

    profiles = SlashCommandGroup(
        name="profiles",
        description="Profile creation commands."
    )

################################################################################
    @profiles.command(
        name="details",
        description="View and update name, custom URL, jobs, accent color, & rates."
    )
    async def profile_details(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.details.set(ctx.interaction)

        return

################################################################################
    @profiles.command(
        name="personality",
        description="View and update your Likes, Dislikes, Personality, and About Me sections."
    )
    async def profile_personality(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.personality.set(ctx.interaction)

################################################################################
    @profiles.command(
        name="ataglance",
        description="Edit or delete your gender, pronouns, race, clan, and other demographic info."
    )
    async def profile_ataglance(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.ataglance.set(ctx.interaction)

################################################################################
    @profiles.command(
        name="images",
        description="View or remove your thumbnail, main image, or additional images."
    )
    async def profile_images(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.images.set(ctx.interaction)

################################################################################
    @profiles.command(
        name="add_image",
        description="Add a Thumbnail, Main Image, or Additional Image to your profile."
    )
    async def profile_add_image(
        self,
        ctx: ApplicationContext,
        section: Option(
            name="field",
            description="Which profile field you want to set with the provided image.",
            choices=[
                OptionChoice(
                    name=SectionType.Thumbnail.proper_name,
                    value=str(SectionType.Thumbnail.value)  # type: ignore
                ),
                OptionChoice(
                    name=SectionType.MainImage.proper_name,
                    value=str(SectionType.MainImage.value)  # type: ignore
                ),
                OptionChoice(
                    name=SectionType.AdditionalImages.proper_name,
                    value=str(SectionType.AdditionalImages.value)  # type: ignore
                )
            ],
            required=True
        ),
        file: Option(
            SlashCommandOptionType.attachment,
            name="file",
            description="The image file to set in the specified field.",
            required=True
        )
    ):

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.images.handle_image(ctx.interaction, SectionType(int(section)), file)

################################################################################
    @profiles.command(
        name="preview",
        description="Preview your current profile! (Duh.)"
    )
    async def profile_preview(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.preview(ctx.interaction)

################################################################################
    @profiles.command(
        name="finalize",
        description="Finalize and post/update your profile"
    )
    async def profile_finalize(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)

        if not guild_data.config.profile_channels:
            error = NoPostChannelsConfigured()
            await ctx.respond(embed=error, ephemeral=True)
            return

        profile = guild_data.get_profile(ctx.user)
        await profile.post(ctx.interaction)

        return

################################################################################
    @profiles.command(
        name="progress",
        description="A command to view a progress dialog for your profile."
    )
    async def profile_progress(self, ctx: ApplicationContext) -> None:

        guild_data = self.bot.get_frog(ctx.guild_id)
        profile = guild_data.get_profile(ctx.user)

        await profile.progress(ctx.interaction)

################################################################################
def setup(bot: "FrogBot") -> None:

    bot.add_cog(Profiles(bot))

################################################################################
