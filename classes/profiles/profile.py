from __future__ import annotations

from discord    import (
    ApplicationCommandInvokeError,
    Colour,
    Embed,
    EmbedField,
    Guild,
    Interaction,
    Member,
    Message,
    NotFound,
    PartialEmoji,
    User
)
from typing     import (
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union
)

from assets         import *
from ui.profiles    import *
from utilities      import *

from classes.profiles   import *

if TYPE_CHECKING:
    from classes.bot    import FrogBot
    from classes.guild  import GuildData
################################################################################

__all__ = ("Profile", )

P = TypeVar("P", bound="Profile")

################################################################################
class Profile:

    __slots__ = (
        "id",
        "user",
        "guild",
        "details",
        "ataglance",
        "personality",
        "images"
    )

################################################################################
    def __init__(
        self,
        *,
        profile_id: str,
        user: Union[Member, User, int],
        guild: Optional[GuildData],
        details: ProfileDetails,
        personality: ProfilePersonality,
        ataglance: ProfileAtAGlance,
        images: ProfileImages
    ):

        self.id: str = profile_id
        self.user: Union[Member, User, int] = user
        self.guild: Optional[GuildData] = guild

        self.details: ProfileDetails = details
        self.personality: ProfilePersonality = personality
        self.ataglance: ProfileAtAGlance = ataglance
        self.images: ProfileImages = images

################################################################################
    @classmethod
    def new(cls: Type[P], user: Union[Member, User], guild: GuildData) -> P:

        self: P = cls.__new__(cls)

        self.id = new_profile_entry(guild_id=guild.parent.id, user_id=user.id)
        self.user = user
        self.guild = guild

        self.details = ProfileDetails(self)
        self.personality = ProfilePersonality(self)
        self.ataglance = ProfileAtAGlance(self)
        self.images = ProfileImages(self)

        return self

################################################################################
    @classmethod
    def load(
        cls: Type[P],
        user: Union[Member, User, int],
        guild: Optional[GuildData],
        data: List[Any]
    ) -> P:

        self: P = cls.__new__(cls)

        self.id = data[0]
        self.user = user
        self.guild = guild

        self.details = ProfileDetails.load(self, data[3:9])
        self.personality = ProfilePersonality.load(self, data[9:13])
        self.ataglance = ProfileAtAGlance.load(self, data[13:21])
        self.images = ProfileImages.load(self, data[21:23])

        return self

################################################################################
    @property
    def color(self) -> Optional[Colour]:

        return self.details.color

################################################################################
    @property
    def char_name(self) -> Optional[str]:

        return self.details.char_name

################################################################################
    def compile(self) -> Tuple[Embed, Optional[Embed]]:

        char_name, url, color, jobs, rates_field = self.details.compile()
        ataglance = self.ataglance.compile()
        likes, dislikes, personality, aboutme = self.personality.compile()
        thumbnail, main_image, additional_imgs = self.images.compile()

        if char_name is NS:
            char_name = f"Character Name: {NS}"
        elif url is not NS:
            char_name = f"{BotEmojis.Envelope.value}  {char_name}  {BotEmojis.Envelope.value}"

        description = Embed.Empty
        if jobs is not NS:
            description = (
                f"{draw_separator(text=jobs)}\n"
                f"{jobs}\n"
                f"{draw_separator(text=jobs)}"
            )

        fields: List[EmbedField] = []
        if ataglance is not None:
            fields.append(ataglance)
        if rates_field is not None:
            fields.append(rates_field)
        if likes is not None:
            fields.append(likes)
        if dislikes is not None:
            fields.append(dislikes)
        if personality is not None:
            fields.append(personality)
        if additional_imgs is not None:
            additional_imgs.value += draw_separator(extra=15)
            fields.append(additional_imgs)

        main_profile = make_embed(
            color=color,
            title=char_name,
            description=description,
            url=url if url is not NS else Embed.Empty,
            thumbnail_url=thumbnail,
            image_url=main_image,
            fields=fields
        )

        return main_profile, aboutme

################################################################################
    async def post(self, interaction: Interaction) -> None:

        if self.char_name is NS:
            error = CharNameNotSet()
            await interaction.response.send_message(embed=error, emphemeral=True)
            return

        main_profile, aboutme = self.compile()

        if len(main_profile) > 5999:
            error = ExceedsMaxLengthError(len(main_profile))
            await interaction.response.send_message(embed=error, emphemeral=True)
            return

        embeds = [main_profile]
        if aboutme is not None:
            embeds.append(aboutme)

        profile_msg = await self.fetch_post_message(interaction.client)  # type: ignore
        if profile_msg is not None:
            try:
                await profile_msg.edit(embeds=embeds)
            except NotFound:
                self.details.post_url = None

            await interaction.response.send_message(embed=self.success_message())
            return

        prompt = make_embed(
            title="Select Your Posting Channel",
            description=(
                "The select below is populated with the channels approved\n"
                "by your server admin(s) for profile posting.\n\n"
                
                "Pick one to finish the process!"
            ),
            timestamp=False
        )
        view = ProfileChannelSelectorView(interaction.user, self.guild.config.profile_channels)

        try:
            await interaction.response.send_message(embed=prompt, view=view)
        except ApplicationCommandInvokeError:
            await interaction.followup.send(embed=prompt, view=view)

        await view.wait()

        if not view.complete or view.value is False:
            return

        try:
            post_channel = await interaction.client.get_or_fetch_channel(view.value)  # type: ignore
        except NotFound:
            error = ChannelNotFoundError()
            await interaction.response.send_message(embed=error, emphemeral=True)
            return

        try:
            post_msg = await post_channel.send(embeds=embeds)
        except:
            raise
        else:
            self.details.post_url = post_msg.jump_url

        await interaction.followup.send(embed=self.success_message())

        return

################################################################################
    async def fetch_post_message(self, client: FrogBot) -> Optional[Message]:

        post_url = self.details.post_url
        if post_url is NS:
            return

        parts = post_url.split("/")
        channel_id = int(parts[5])
        msg_id = int(parts[6])

        profile_msg = None
        try:
            channel = await client.get_or_fetch_channel(channel_id)
        except:
            return
        else:
            try:
                profile_msg = await channel.fetch_message(msg_id)
            except:
                self.details.post_url = None

        return profile_msg

################################################################################
    def success_message(self) -> Embed:

        return make_embed(
            color=Colour.brand_green(),
            title="Profile Posted!",
            description=(
                "Hey, good job, you did it! Your profile was posted successfully!\n"
                f"{draw_separator(extra=37)}\n"
                f"(__Character Name:__ ***{self.char_name}***)\n\n"
                
                f"{BotEmojis.ArrowRight.value}  [Check It Out HERE!]"
                f"({self.details.post_url})  {BotEmojis.ArrowLeft.value}\n"
                f"{draw_separator(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog.value,
            footer_text="FrogBot: By Allegro#6969",
            footer_icon=BotImages.ThumbsUpFrog.value,
            timestamp=True
        )

################################################################################
    async def preview(self, interaction: Interaction) -> None:

        prompt = make_embed(
            color=self.color,
            title="Preview Profile",
            description=(
                "Select the button below corresponding to the section\n"
                "of your profile you would like to preview."
            ),
            timestamp=False
        )
        view = ProfilePreView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        return

################################################################################
    async def progress(self, interaction: Interaction) -> None:

        em_final = self.details.progress_emoji(self.details._post_url)

        value = (
            self.details.progress() +
            self.ataglance.progress() +
            self.personality.progress() +
            self.images.progress() +
            f"{draw_separator(extra=15)}\n"
            f"{em_final} -- Finalize"
        )

        progress = make_embed(
            color=self.color,
            title="Profile Progress",
            description=value,
            timestamp=False
        )
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=progress, view=view)
        await view.wait()

        return

################################################################################
