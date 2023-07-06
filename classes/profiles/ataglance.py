from __future__ import annotations

from discord    import Embed, EmbedField, Interaction
from typing     import TYPE_CHECKING, List, Optional, Type, TypeVar, Union

from assets         import *
from ui.profiles    import *
from utilities      import *

from .section   import ProfileSection

if TYPE_CHECKING:
    from .profile   import Profile
################################################################################

__all__ = ("ProfileAtAGlance", )

AAG = TypeVar("AAG", bound="ProfileAtAGlance")

################################################################################
class ProfileAtAGlance(ProfileSection):

    __slots__ = (
        "_gender",
        "_pronouns",
        "_race",
        "_clan",
        "_orientation",
        "_height",
        "_age",
        "_mare"
    )

################################################################################
    def __init__(self, parent: Profile, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._gender: Optional[Union[Gender, str]] = kwargs.pop("gender", None)
        self._pronouns: List[Pronoun] = kwargs.pop("pronouns", None) or []
        self._race: Optional[Union[Race, str]] = kwargs.pop("race", None)
        self._clan: Optional[Union[Clan, str]] = kwargs.pop("clan", None)
        self._orientation: Optional[Union[Orientation, str]] = kwargs.pop("orientation", None)
        self._height: Optional[Union[str, int]] = kwargs.pop("height", None)
        self._age: Optional[Union[str, int]] = kwargs.pop("age", None)
        self._mare: Optional[str] = kwargs.pop("mare", None)

################################################################################
    @classmethod
    def load(cls: Type[AAG], parent: Profile, data: List[str]) -> AAG:

        gender_val = (
            Gender(int(data[0])) if data[0] is not None
            and data[0].isdigit() and int(data[0]) <= len(Gender)
            else None
        )
        pronoun_val = (
            [Pronoun(int(i)) for i in convert_db_list(data[1])]
            if data[1] is not None
            else []
        )
        race_val = (
            Race(int(data[2])) if data[2] is not None
            and data[2].isdigit() and int(data[2]) <= len(Race)
            else None
        )
        clan_val = (
            Clan(int(data[3])) if data[3] is not None
            and data[3].isdigit() and int(data[3]) <= len(Clan)
            else None
        )
        orientation_val = (
            Orientation(int(data[4])) if data[4] is not None
            and data[4].isdigit() and int(data[4]) <= len(Orientation)
            else None
        )
        height_val = (
            int(data[5]) if data[5] is not None and data[5].isdigit()
            else None
        )
        age_val = (
            int(data[6]) if data[6] is not None and data[6].isdigit()
            else None
        )

        return cls(
            parent=parent,
            gender=gender_val,
            pronouns=pronoun_val,
            race=race_val,
            clan=clan_val,
            orientation=orientation_val,
            height=height_val,
            age=age_val,
            mare=data[7]
        )

################################################################################
    @property
    def gender(self) -> Optional[str]:

        if self._gender is None:
            return NS
        elif isinstance(self._gender, Gender):
            return self._gender.proper_name
        else:
            return self._gender

################################################################################
    @gender.setter
    def gender(self, value: Optional[Union[Gender, str]]) -> None:

        self._gender = value
        self.update()

################################################################################
    @property
    def pronouns(self) -> Optional[str]:

        if not self._pronouns:
            return NS

        return "/".join([p.proper_name for p in self._pronouns])

################################################################################
    @pronouns.setter
    def pronouns(self, value: Optional[List[Pronoun]]) -> None:

        self._pronouns = [] if value is None else value
        self.update()

################################################################################
    def compile_gender(self) -> str:

        if self.gender is NS:
            return ""

        ret = f"__Gender:__ {self.gender}"

        if self.pronouns is not NS:
            ret += f" -- *({self.pronouns})*"

        ret += "\n"

        return ret

################################################################################
    @property
    def race(self) -> Optional[str]:

        if self._race is None:
            return NS
        elif isinstance(self._race, Race):
            return self._race.proper_name
        else:
            return self._race

################################################################################
    @race.setter
    def race(self, value: Optional[Union[Race, str]]) -> None:

        self._race = value
        self.update()

################################################################################
    @property
    def clan(self) -> Optional[str]:

        if self._clan is None:
            return NS
        elif isinstance(self._clan, Clan):
            return self._clan.proper_name
        else:
            return self._clan

################################################################################
    @clan.setter
    def clan(self, value: Optional[Union[Race, str]]) -> None:

        self._clan = value
        self.update()

################################################################################
    def compile_raceclan(self) -> str:

        if self.race is NS:
            return ""

        ret = f"__Race:__ {self.race}"

        if self.clan is not NS:
            ret += f" / {self.clan}"

        ret += "\n"

        return ret

################################################################################
    @property
    def orientation(self) -> Optional[str]:

        if self._orientation is None:
            return NS
        elif isinstance(self._orientation, Orientation):
            return self._orientation.proper_name
        else:
            return self._orientation

################################################################################
    @orientation.setter
    def orientation(self, value: Optional[Union[Orientation, str]]) -> None:

        self._orientation = value
        self.update()

################################################################################
    def compile_orientation(self) -> str:

        if self.orientation is NS:
            return ""

        return f"__Orientation:__ {self.orientation}\n"

################################################################################
    @property
    def height(self) -> Optional[Union[str, int]]:

        if self._height is None:
            return NS
        elif isinstance(self._height, int):
            return int(self._height)
        else:
            return f"`{self._height}`"

################################################################################
    @height.setter
    def height(self, value: Optional[Union[str, int]]) -> None:

        self._height = value
        self.update()

################################################################################
    @property
    def formatted_height(self) -> str:

        if self._height is None or isinstance(self._height, str):
            return self.height

        inches = int(self._height / 2.54)
        feet = inches // 12
        leftover = int(inches % 12)

        return f"{feet}' {leftover}\" (~{self.height} cm.)"

################################################################################
    def compile_height(self) -> str:

        return "" if self.height is NS else f"__Height:__ {self.formatted_height}\n"

################################################################################
    @property
    def age(self) -> Optional[Union[str, int]]:

        if self._age is None:
            return NS
        elif isinstance(self._age, int):
            return int(self._age)
        else:
            return f"`{self._age}`"

################################################################################
    @age.setter
    def age(self, value: Optional[Union[str, int]]) -> None:

        self._age = value
        self.update()

################################################################################
    def compile_age(self) -> str:

        return "" if self.age is NS else f"__Age:__ {self.age}\n"

################################################################################
    @property
    def mare(self) -> Optional[str]:

        return NS if self._mare is None else self._mare

################################################################################
    @mare.setter
    def mare(self, value: Optional[str]) -> None:

        self._mare = value
        self.update()

################################################################################
    def compile_mare(self) -> str:

        return "" if self.mare is NS else f"__Friend ID:__ {self.mare}\n"

################################################################################
    def status(self) -> Embed:

        race_val = clan_val = str(NS)
        if self.race is not NS:
            race_val = self.race
        if self.clan is not NS:
            clan_val = self.clan

        raceclan = f"{race_val}/{clan_val}"
        if isinstance(self._race, str) or isinstance(self._clan, str):
            raceclan += "\n*(Custom Value(s))*"

        gender_val = pronoun_val = str(NS)
        if self.gender is not NS:
            gender_val = self.gender
        if self.pronouns is not NS:
            pronoun_val = self.pronouns

        gp_combined = f"{gender_val} -- *({pronoun_val})*"
        if isinstance(self._gender, str):
            gp_combined += "\n*(Custom Value)*"

        orientation_val = self.orientation if self.orientation is not NS else str(NS)
        if isinstance(self._orientation, str):
            orientation_val += "\n*(Custom Value)*"

        height_val = age_val = mare_val = str(NS)
        if self.height is not NS:
            height_val = self.formatted_height
        if self.age is not NS:
            age_val = self.age
        if self.mare is not NS:
            mare_val = self.mare

        fields = [
            EmbedField("__Race/Clan__", raceclan, True),
            EmbedField("__Gender/Pronouns__", gp_combined, True),
            EmbedField("", draw_separator(extra=30), False),
            EmbedField("__Orientation__", orientation_val, True),
            EmbedField("__Friend ID__", mare_val, True),
            EmbedField("", draw_separator(extra=30), False),
            EmbedField("__Height__", height_val, True),
            EmbedField("__Age__", age_val, True),
        ]

        return make_embed(
            color=self.parent.color,
            title=f"At A Glance Section Details for {self.parent.char_name}",
            description=(
                "*All sections, aside from **Race/Clan** are optional.*\n"
                "*(Click the corresponding button below to edit each data point.)*\n"
                f"{draw_separator(extra=38)}"
            ),
            fields=fields,
            timestamp=False
        )

################################################################################
    def _raw_string(self) -> str:

        ret = (
            self.compile_gender() +
            self.compile_raceclan() +
            self.compile_orientation() +
            self.compile_height() +
            self.compile_age() +
            self.compile_mare()
        )

        if ret:
            ret += draw_separator(extra=15)

        return ret

################################################################################
    def compile(self) -> Optional[EmbedField]:

        if not self._raw_string():
            return

        return EmbedField(
            name=f"{BotEmojis.Eyes.value}  __At A Glance__ {BotEmojis.Eyes.value}",
            value=self._raw_string(),
            inline=False
        )

################################################################################
    def progress(self) -> str:

        em_gender = self.progress_emoji(self._gender)
        em_race = self.progress_emoji(self._race)
        em_orientation = self.progress_emoji(self._orientation)
        em_height = self.progress_emoji(self._height)
        em_age = self.progress_emoji(self._age)
        em_mare = self.progress_emoji(self._mare)

        return (
            f"{draw_separator(extra=15)}\n"
            "__**At A Glance**__\n"
            f"{em_gender} -- Gender / Pronouns\n"
            f"{em_race} -- Race / Clan\n"
            f"{em_orientation} -- Orientation\n"
            f"{em_height} -- Height\n"
            f"{em_age} -- Age\n"
            f"{em_mare} -- Friend ID\n"
        )

################################################################################
    async def set(self, interaction: Interaction) -> None:

        view = AtAGlanceView(interaction.user, self)

        await interaction.response.send_message(embed=self.status(), view=view)
        await view.wait()

################################################################################
    async def set_gender(self, interaction: Interaction) -> None:

        prompt = make_embed(
            title="Gender/Pronoun Selection",
            description=(
                "Select your preferred gender from the selector below.\n"
                "Don't worry,  you'll be able to choose your pronouns next!\n\n"
                
                "**If you select `Custom`, a pop-up will appear for you\n"
                "to provide your custom gender text.**"
            ),
            timestamp=False
        )
        view = GenderPronounView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        return

################################################################################
    async def set_raceclan(self, interaction: Interaction) -> None:

        prompt = make_embed(
            title="Select Your Race & Clan",
            description=(
                "Select your character's race from the drop-down below.\n"
                "An additional selector will then appear for you to choose your clan.\n\n"
                
                "**If none of those apply, you may select `Custom`, and a pop-up will\n"
                "appear for you to enter your own custom information into.**"
            ),
            timestamp=False
        )
        view = RaceClanSelectView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        return

################################################################################
    async def set_orientation(self, interaction: Interaction) -> None:

        prompt = make_embed(
            title="Select Your Orientation",
            description=(
                "Select your preferred orientation from the selector below.\n\n"
                
                "**If you select `Custom`, a pop-up will appear for\n"
                "you to provide your custom orientation value.**"
            ),
            timestamp=False
        )
        view = OrientationSelectView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        return

################################################################################
    async def set_height(self, interaction: Interaction) -> None:

        modal = HeightInputModal(self._height)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.height = modal.value

        return

################################################################################
    async def set_age(self, interaction: Interaction) -> None:

        modal = AgeInputModal(self._age)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.age = modal.value

        return

################################################################################
    async def set_mare(self, interaction: Interaction) -> None:

        modal = MareInputModal(self._mare)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.mare = modal.value

        return

################################################################################
    def update(self) -> None:

        gender_val = (
            self._gender if isinstance(self._gender, str) or self._gender is None
            else str(self._gender.value)
        )
        pronoun_val = [p.value for p in self._pronouns] if self._pronouns else None
        race_val = (
            self._race if isinstance(self._race, str) or self._race is None
            else str(self._race.value)
        )
        clan_val = (
            self._clan if isinstance(self._clan, str) or self._clan is None
            else str(self._clan.value)
        )
        orientation_val = (
            self._orientation if isinstance(self._orientation, str) or self._orientation is None
            else str(self._orientation.value)
        )
        height_val = (
            self._height if isinstance(self._height, str) or self._height is None
            else str(self._height)
        )
        age_val = (
            self._age if isinstance(self._age, str) or self._age is None
            else str(self._age)
        )

        c = db_connection.cursor()
        c.execute(
            "UPDATE ataglance SET gender = %s, pronouns = %s, race = %s, clan = %s, "
            "orientation = %s, height = %s, age = %s, mare = %s WHERE profile_id = %s",
            (
                gender_val, pronoun_val, race_val, clan_val, orientation_val,
                height_val, age_val, self._mare, self.parent.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
