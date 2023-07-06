from __future__ import annotations

from discord    import Embed, EmbedField, Interaction
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

from .section   import ProfileSection

if TYPE_CHECKING:
    from .profile   import Profile
################################################################################

__all__ = ("ProfilePersonality", )

PP = TypeVar("PP", bound="ProfilePersonality")

################################################################################
class ProfilePersonality(ProfileSection):

    __slots__ = (
        "_likes",
        "_dislikes",
        "_personality",
        "_aboutme"
    )

################################################################################
    def __init__(self, parent: Profile, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._likes: List[str] = kwargs.pop("likes", None) or []
        self._dislikes: List[str] = kwargs.pop("dislikes", None) or []
        self._personality: Optional[str] = kwargs.pop("personality", None)
        self._aboutme: Optional[str] = kwargs.pop("aboutme", None)

################################################################################
    @classmethod
    def load(cls: Type[PP], parent: Profile, data: List[Optional[str]]) -> PP:

        return cls(
            parent=parent,
            likes=convert_db_list(data[0]),
            dislikes=convert_db_list(data[1]),
            personality=data[2],
            aboutme=data[3]
        )

################################################################################
    @property
    def likes(self) -> str:

        return NS if not self._likes else "- " + "\n- ".join(self._likes)

################################################################################
    @likes.setter
    def likes(self, value: Optional[List[str]]) -> None:

        self._likes = [] if not value else value
        self.update()

################################################################################
    @property
    def dislikes(self) -> str:

        return NS if not self._dislikes else "- " + "\n- ".join(self._dislikes)

################################################################################
    @dislikes.setter
    def dislikes(self, value: Optional[List[str]]) -> None:

        self._dislikes = [] if not value else value
        self.update()

################################################################################
    @property
    def personality(self) -> Optional[str]:

        return self._personality or NS

################################################################################
    @personality.setter
    def personality(self, value: Optional[str]) -> None:

        self._personality = value
        self.update()

################################################################################
    @property
    def aboutme(self) -> Optional[str]:

        return self._aboutme or NS

################################################################################
    @aboutme.setter
    def aboutme(self, value: Optional[str]) -> None:

        self._aboutme = value
        self.update()

################################################################################
    def status(self) -> Embed:

        return make_embed(
            color=self.parent.color,
            title=f"Personality Attributes for __{self.parent.char_name}__",
            description=draw_separator(extra=40),
            timestamp=False,
            fields=[
                self.likes_field(SectionType.Likes),
                self.likes_field(SectionType.Dislikes),
                self.personality_field(),
                self.preview_aboutme()
            ]
        )

################################################################################
    def compile(
        self
    ) -> Tuple[
        Optional[EmbedField],
        Optional[EmbedField],
        Optional[EmbedField],
        Optional[Embed]
    ]:

        return (
            self.likes_field(SectionType.Likes) if self.likes is not NS else None,
            self.likes_field(SectionType.Dislikes) if self.dislikes is not NS else None,
            self.personality_field() if self.personality is not NS else None,
            self.compile_aboutme()
        )

################################################################################
    def progress(self) -> str:

        em_likes = self.progress_emoji(self._likes)
        em_dislikes = self.progress_emoji(self._dislikes)
        em_personality = self.progress_emoji(self._personality)
        em_aboutme = self.progress_emoji(self._aboutme)

        return (
            f"{draw_separator(extra=15)}\n"
            "__**Personality**__\n"
            f"{em_likes} -- Likes\n"
            f"{em_dislikes} -- Dislikes\n"
            f"{em_personality} -- Personality\n"
            f"{em_aboutme} -- About Me\n"
        )

################################################################################
    def likes_field(self, section: SectionType) -> EmbedField:

        if section is SectionType.Likes:
            section_name = f"{BotEmojis.Check.value}  __Likes__"
            field_value = self.likes if self.likes is not NS else str(self.likes)
            field_value += f"\n{draw_separator(extra=15)}"
        else:
            section_name = f"{BotEmojis.Cross.value}  __Dislikes__"
            field_value = self.dislikes if self.dislikes is not NS else str(self.dislikes)

        return EmbedField(
            name=section_name,
            value=field_value,
            inline=True
        )

################################################################################
    def personality_field(self) -> EmbedField:

        value = self.personality if self.personality is not NS else str(self.personality)

        return EmbedField(
            name=f"{BotEmojis.Goose.value}  __Personality__  {BotEmojis.Goose.value}",
            value=f"{value}\n{draw_separator(extra=15)}",
            inline=False
        )

################################################################################
    def preview_aboutme(self) -> EmbedField:

        if self.aboutme is NS:
            value = str(self.aboutme)
        elif len(self.aboutme) < 500:
            value = self.aboutme
        else:
            value = self.aboutme[:501] + "...\n*(Preview Only -- Click below to see the whole thing!)*"

        return EmbedField(
            name=f"{BotEmojis.Scroll.value}  __About Me / Biography__  {BotEmojis.Scroll.value}",
            value=f"{value}\n{draw_separator(extra=15)}",
            inline=False
        )

################################################################################
    def compile_aboutme(self) -> Optional[Embed]:

        if not self.aboutme:
            return

        return make_embed(
            color=self.parent.color,
            title=f"About {self.parent.char_name}",
            description=self.aboutme,
            footer_text=(
                self.parent.details.url
                if self.parent.details.url is not NS
                else Embed.Empty
            ),
            timestamp=False
        )

################################################################################
    async def set(self, interaction: Interaction) -> None:

        status = self.status()
        view = PersonalityView(interaction.user, self)

        await interaction.response.send_message(embed=status, view=view)
        await view.wait()

        return

################################################################################
    def return_section(self, section: SectionType) -> Optional[Union[List[str], str]]:

        if section is SectionType.Likes:
            return self._likes
        elif section is SectionType.Dislikes:
            return self._dislikes
        elif section is SectionType.Personality:
            return self._personality
        else:
            return self._aboutme

################################################################################
    def set_section(self, section: SectionType, value: Optional[Union[List[str], str]]) -> None:

        if section is SectionType.Likes:
            self.likes = value
        elif section is SectionType.Dislikes:
            self.dislikes = value
        elif section is SectionType.Personality:
            self.personality = value
        else:
            self.aboutme = value

################################################################################
    async def set_personality_section(self, interaction: Interaction, section: SectionType) -> None:

        modal = PersonalityModal(section, self.return_section(section))

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.set_section(section, modal.value)

        return

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE personality SET likes = %s, dislikes = %s, personality = %s, "
            "aboutme = %s WHERE profile_id = %s",
            (
                self._likes, self._dislikes, self._personality, self._aboutme,
                self.parent.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
