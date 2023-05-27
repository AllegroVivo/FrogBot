from __future__ import annotations

from discord    import Colour, Embed, EmbedField, Interaction
from typing     import (
    TYPE_CHECKING,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union
)

from assets         import BotEmojis
from utilities      import *
from ui.profiles    import *

from .section   import ProfileSection

if TYPE_CHECKING:
    from .profile   import Profile
################################################################################

__all__ = (
    "ProfileDetails",
)

PD = TypeVar("PD", bound="ProfileDetails")

################################################################################
class ProfileDetails(ProfileSection):

    __slots__ = (
        "_char_name",
        "_url",
        "_color",
        "_jobs",
        "_rates",
        "_post_url"
    )

################################################################################
    def __init__(self, parent: Profile, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._char_name: Optional[str] = kwargs.pop("char_name", None)
        self._url: Optional[str] = kwargs.pop("url", None) or kwargs.pop("custom_url", None)
        self._color: Optional[Colour] = kwargs.pop("color", None) or kwargs.pop("colour", None)
        self._jobs: List[str] = kwargs.pop("jobs", []) or []
        self._rates: Optional[str] = kwargs.pop("rates", None)
        self._post_url: Optional[str] = kwargs.pop("post_url", None)

################################################################################
    @classmethod
    def load(
        cls: Type[PD],
        parent: Profile,
        data: List[Optional[Union[str, int]]]
    ) -> PD:

        return cls(
            parent=parent,
            char_name=data[0],
            custom_url=data[1],
            color=Colour(data[2]) if data[2] is not None else None,
            jobs=convert_db_list(data[3]),
            rates=data[4],
            post_url=data[5]
        )

################################################################################
    def status(self) -> Embed:

        jobs = "- " + "\n- ".join(self._jobs) if self._jobs else str(NS)

        if self._color is not None:
            color_field = f"{BotEmojis.ArrowLeft.value} -- (__{str(self.color).upper()}__)"
        else:
            color_field = str(NS)

        fields = [
            EmbedField("__Color__", color_field, True),
            EmbedField("__Jobs__", jobs, True),
            EmbedField("__Custom URL__", str(self.url), False),
            EmbedField("__Rates__", str(self.rates), False)
        ]

        char_name = f"**Character Name:** {str(self.char_name)}"

        return make_embed(
            title="Profile Details",
            color=self.color,
            description=(
                f"{draw_separator(text=char_name)}\n"
                f"{char_name}\n"
                f"{draw_separator(text=char_name)}\n"
                "Select a button to add/edit the corresponding profile attribute."
            ),
            fields=fields
        )

################################################################################
    def compile(
        self
    ) -> Tuple[
        Optional[str],
        Optional[str],
        Optional[Colour],
        Optional[str],
        Optional[EmbedField]
    ]:

        return (
            self.char_name,
            self.url,
            self.color,
            self.jobs,
            self.rates_field()
        )

################################################################################
    def progress(self) -> str:

        em_color = self.progress_emoji(self._color)
        em_name = self.progress_emoji(self._char_name)
        em_url = self.progress_emoji(self._url)
        em_jobs = self.progress_emoji(self._jobs)
        em_rates = self.progress_emoji(self._rates)

        return (
            f"{draw_separator(extra=15)}\n"
            "__**Details**__\n"
            f"{em_name} -- Character Name\n"
            f"{em_url} -- Custom URL\n"
            f"{em_color} -- Accent Color\n"
            f"{em_jobs} -- Jobs List\n"
            f"{em_rates} -- Rates Field\n"
        )

################################################################################
    def rates_field(self) -> Optional[EmbedField]:

        if self.rates is NS:
            return

        return EmbedField(
            name=f"{BotEmojis.FlyingMoney.value} __Rates__ {BotEmojis.FlyingMoney.value}",
            value=(
                f"{self.rates}\n"
                f"{draw_separator(extra=15)}"
            ),
            inline=False
        )

################################################################################
    @property
    def char_name(self) -> Optional[str]:

        return self._char_name or NS

################################################################################
    @char_name.setter
    def char_name(self, value: str) -> None:

        self._char_name = value
        self.update()

################################################################################
    @property
    def url(self) -> Optional[str]:

        return self._url or NS

################################################################################
    @url.setter
    def url(self, value: Optional[str]) -> None:

        self._url = value
        self.update()

################################################################################
    @property
    def color(self) -> Optional[Colour]:

        return self._color or Embed.Empty

################################################################################
    @color.setter
    def color(self, value: Union[Colour, int]):

        if isinstance(value, Colour):
            self._color = value
        else:
            self._color = Colour(value)

        self.update()

################################################################################
    @property
    def jobs(self) -> Optional[str]:

        return "/".join(self._jobs) if self._jobs else NS

################################################################################
    @jobs.setter
    def jobs(self, value: Optional[List[str]]) -> None:

        self._jobs = value
        self.update()

################################################################################
    @property
    def rates(self) -> Optional[str]:

        return self._rates or NS

################################################################################
    @rates.setter
    def rates(self, value: Optional[str]) -> None:

        self._rates = value
        self.update()

################################################################################
    @property
    def post_url(self) -> Optional[str]:

        return self._post_url or NS

################################################################################
    @post_url.setter
    def post_url(self, value: Optional[str]) -> None:

        self._post_url = value
        self.update()

################################################################################
    async def set_char_name(self, interaction: Interaction) -> None:

        modal = CharNameModal(self._char_name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.char_name = modal.value

        return

################################################################################
    async def set_url(self, interaction: Interaction) -> None:

        modal = ProfileURLModal(self._url)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.url = modal.value

        return

################################################################################
    async def set_color(self, interaction: Interaction) -> None:

        modal = ColorModal(self._color)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.color = modal.value

        return

################################################################################
    async def set_jobs(self, interaction: Interaction) -> None:

        modal = JobsModal(self._jobs)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.jobs = [j for j in modal.value if j is not None]

        return

################################################################################
    async def set_rates(self, interaction: Interaction) -> None:

        modal = RatesModal(self._rates)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.rates = modal.value

        return

################################################################################
    async def set(self, interaction: Interaction) -> None:

        status = self.status()
        view = DetailsStatusView(interaction.user, self)

        await interaction.response.send_message(embed=status, view=view)
        await view.wait()

        return

################################################################################
    def update(self) -> None:

        color_value = self._color.value if self._color is not None else None

        c = db_connection.cursor()
        c.execute(
            "UPDATE details SET char_name = %s, url = %s, color = %s, jobs = %s, "
            "rates = %s, post_url = %s WHERE profile_id = %s",
            (
                self._char_name, self._url, color_value, self._jobs, self._rates,
                self._post_url, self.parent.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
