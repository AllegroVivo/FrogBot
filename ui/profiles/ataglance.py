from __future__ import annotations

import math
import re

from discord    import InputTextStyle, Interaction, Member, User
from discord.ui import InputText, Select
from typing     import TYPE_CHECKING, Optional, Tuple, Union

from utilities  import *

from ui.common import *
from ui.view import *

if TYPE_CHECKING:
    from classes.profiles   import ProfileAtAGlance
################################################################################

__all__ = (
    "AtAGlanceView",
    "GenderPronounView",
    "RaceClanSelectView",
    "OrientationSelectView",
    "MareInputModal",
    "AgeInputModal",
    "HeightInputModal"
)

################################################################################
class GenderPronounButton(ProfileSectionButton):

    def __init__(self, gender: Optional[Union[Gender, str]]):

        super().__init__(
            label="Gender/Pronouns",
            disabled=False,
            row=0
        )

        self.set_style(gender)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_gender(interaction)

        self.set_style(aag._gender)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class RaceClanButton(ProfileSectionButton):

    def __init__(self, race: Optional[Union[Race, str]]):

        super().__init__(
            label="Race/Clan",
            disabled=False,
            row=0
        )

        self.set_style(race)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_raceclan(interaction)

        self.set_style(aag._clan)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class OrientationButton(ProfileSectionButton):

    def __init__(self, orientation: Optional[Union[Orientation, str]]):

        super().__init__(
            label="Orientation",
            disabled=False,
            row=0
        )

        self.set_style(orientation)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_orientation(interaction)

        self.set_style(aag._orientation)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class HeightButton(ProfileSectionButton):

    def __init__(self, height: Optional[int]):

        super().__init__(
            label="Height",
            disabled=False,
            row=1
        )

        self.set_style(height)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_height(interaction)

        self.set_style(aag._height)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class AgeButton(ProfileSectionButton):

    def __init__(self, age: Optional[str]):
        super().__init__(
            label="Age",
            disabled=False,
            row=1
        )

        self.set_style(age)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_age(interaction)

        self.set_style(aag._age)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class MareButton(ProfileSectionButton):

    def __init__(self, mare: Optional[str]):
        super().__init__(
            label="Friend ID",
            disabled=False,
            row=1
        )

        self.set_style(mare)

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        await aag.set_mare(interaction)

        self.set_style(aag._mare)

        await edit_message_helper(
            interaction=interaction,
            embed=aag.status(),
            view=self.view
        )

################################################################################
class AtAGlanceView(FrogView):

    def __init__(self, owner: Union[Member, User], profile_obj: ProfileAtAGlance, *args, **kwargs):

        super().__init__(owner, *args, **kwargs)

        self.aag: ProfileAtAGlance = profile_obj

        button_list = [
            RaceClanButton(self.aag._race),
            GenderPronounButton(self.aag._gender),
            OrientationButton(self.aag._orientation),
            HeightButton(self.aag._height),
            AgeButton(self.aag._age),
            MareButton(self.aag._mare),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
class CustomGenderModal(FrogModal):

    def __init__(self, cur_val: Optional[Union[Gender, str]]):

        super().__init__(title="Set Custom Gender Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom gender identity below.",
                value=(
                    "Enter your custom gender identity in the box below.\n"
                    "You can choose your preferred pronouns after this."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Custom Gender",
                placeholder="eg. 'Amphibian'",
                value=cur_val if not isinstance(cur_val, Gender) else None,
                max_length=30,
                required=True
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class PronounSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select your preferred pronouns...",
            options=Pronoun.select_options(),
            max_values=len(Pronoun.select_options()),
            row=1
        )

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        aag.pronouns = [Pronoun(int(i)) for i in self.values]

        self.view.complete = True

        await interaction.response.edit_message()
        await edit_message_helper(interaction, embed=aag.status())

        await self.view.stop()  # type: ignore

################################################################################
class GenderSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select Your Preferred Gender...",
            options=Gender.select_options(),
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        aag = self.view.aag

        if int(self.values[0]) != 4:
            aag.gender = Gender(int(self.values[0]))
            await interaction.response.edit_message()
        else:
            modal = CustomGenderModal(aag._gender)

            await interaction.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                await self.view.stop()  # type: ignore
            else:
                aag.gender = modal.value

        self.placeholder = str(aag.gender)
        self.disabled = True
        self.view.add_item(PronounSelect())

        await edit_message_helper(interaction=interaction, view=self.view)

################################################################################
class GenderPronounView(FrogView):

    def __init__(self, owner: Union[Member, User], aag: ProfileAtAGlance, *args, **kwargs):

        super().__init__(owner, *args, close_on_complete=True, **kwargs)

        self.aag: ProfileAtAGlance = aag

        self.add_item(GenderSelect())

################################################################################
class CustomRaceClanModal(FrogModal):

    def __init__(self, cur_race: Optional[Union[Race, str]], cur_clan: Optional[Union[Clan, str]]):

        super().__init__(title="Set Custom Race & Clan Values")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom race and clan values below.",
                value="Enter your custom race and clan values below. Only race is required.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Race",
                placeholder="eg. 'Amphibarian'",
                value=cur_race if not isinstance(cur_race, Race) else None,
                max_length=25,
                required=True
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Clan",
                placeholder="eg. 'Pad Leaper'",
                value=cur_clan if not isinstance(cur_clan, Clan) else None,
                max_length=25,
                required=False
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = (
            self.children[1].value,
            self.children[2].value if self.children[2].value else None
        )
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class CustomClanModal(FrogModal):

    def __init__(self, cur_clan: Optional[Union[Clan, str]]):

        super().__init__(title="Set Custom Clan Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom Clan value in the blow below.",
                value=(
                    "Enter your custom Clan value below. This isn't required, and if \n"
                    "you don't want to enter one, simply submit a blank dialog."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Clan",
                placeholder="eg. 'Pad Leaper'",
                value=cur_clan if not isinstance(cur_clan, Clan) else None,
                max_length=25,
                required=False
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ClanSelect(Select):

    def __init__(self, race: Race):
        super().__init__(
            placeholder="Select Your Clan...",
            options=Clan.select_options(race),
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        response = Clan(int(self.values[0]))

        if response is Clan.Custom:
            modal = CustomClanModal(aag._clan)

            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.complete:
                response = modal.value

        aag.clan = response
        self.view.complete = True

        try:
            await interaction.response.edit_message()
        except:
            pass

        await self.view.stop()  # type: ignore

################################################################################
class RaceSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select Your Race...",
            options=Race.select_options(),
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        response = Race(int(self.values[0]))

        if response is Race.Custom:
            modal = CustomRaceClanModal(aag._race, aag._clan)

            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.complete:
                aag.race = modal.value[0]
                aag.clan = modal.value[1]

            await self.view.stop()  # type: ignore
            return
        else:
            await interaction.response.edit_message()

        aag.race = response
        self.placeholder = response.proper_name
        self.disabled = True
        self.view.add_item(ClanSelect(response))

        await edit_message_helper(interaction, view=self.view)

################################################################################
class RaceClanSelectView(FrogView):

    def __init__(self, owner: Union[Member, User], aag: ProfileAtAGlance, *args, **kwargs):

        super().__init__(owner, *args, close_on_complete=True, **kwargs)

        self.aag: ProfileAtAGlance = aag

        self.add_item(RaceSelect())

################################################################################
class CustomOrientationModal(FrogModal):

    def __init__(self, cur_value: Optional[Union[Orientation, str]]):
        super().__init__(title="Set Your Custom Orientation Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom sexual orientation.",
                value="Enter the text you want to display as your sexual orientation.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Sexual Orientation",
                placeholder="eg. 'Frogge'",
                required=False,
                max_length=40
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class OrientationSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select Your Orientation...",
            options=Orientation.select_options(),
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        aag = self.view.aag
        response = Orientation(int(self.values[0]))

        if response is Orientation.Custom:
            modal = CustomOrientationModal(aag._orientation)

            await interaction.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            response = modal.value
        else:
            await interaction.response.edit_message()

        aag.orientation = response
        self.view.complete = True

        await self.view.stop()  # type: ignore

################################################################################
class OrientationSelectView(FrogView):

    def __init__(self, owner: Union[Member, User], profile_obj: ProfileAtAGlance):
        super().__init__(owner, close_on_complete=True)

        self.aag: ProfileAtAGlance = profile_obj

        self.add_item(OrientationSelect())

################################################################################
class HeightInputModal(FrogModal):

    def __init__(self, cur_val: Optional[int]):
        super().__init__(title="Height Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your height in feet and inches.",
                value="Enter your height in feet and inches, or centimeters.",
                required=False
            )
        )

        if cur_val is not None:
            inches = int(cur_val / 2.54)
            feet = inches // 12
            leftover = int(inches % 12)
            cur_val = f"{feet}' {leftover}\""

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Height",
                placeholder="eg. '6ft 2in'",
                value=cur_val,
                required=False,
                max_length=20
            )
        )

    async def callback(self, interaction: Interaction):
        if self.children[1].value:
            if result := re.match(
                r"^(\d+)\s*cm\.?|(\d+)\s*(?:ft\.?|feet|')$|(\d+)\s*(?:in\.?|inches|\"|'')|"
                r"(\d+)\s*(?:ft\.?|feet|')\s*(\d+)\s*(?:in\.?|inches|\"|'')",
                self.children[1].value,
            ):
                if result[1]:
                    self.value = int(result[1])
                elif result[2]:
                    cm = int(result[2]) * 12 * 2.54
                    self.value = math.ceil(cm)
                elif result[3]:
                    cm = int(result[3]) * 2.54
                    self.value = math.ceil(cm)
                elif result[4] and result[5]:
                    inches = int(result[4]) * 12 + int(result[5])
                    self.value = math.ceil(inches * 2.54)
            else:
                error = HeightInputError(self.children[1].value)
                await interaction.response.send_message(embed=error, ephemeral=True)

        try:
            await interaction.response.edit_message()
        except:
            pass

        self.complete = True
        self.stop()

################################################################################
class AgeInputModal(FrogModal):

    def __init__(self, cur_val: Optional[Union[str, int]]):
        super().__init__(title="Age Value Input")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your age below.",
                value="Enter your age. It may be a numerical value or text.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Age",
                placeholder="eg. '32' -or- 'Older than you think...'",
                value=str(cur_val) if cur_val is not None else None,
                required=False,
                max_length=30
            )
        )

    async def callback(self, interaction: Interaction):
        if self.children[1].value:
            if self.children[1].value.isdigit():
                self.value = abs(int(self.children[1].value))
            else:
                self.value = self.children[1].value

        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class MareInputModal(FrogModal):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(title="Friend ID Code Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your friend ID/pairing code.",
                value="Enter your alphanumeric Friend Pairing ID below.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Friend ID",
                placeholder="eg. 'A1B2C3D4E5'",
                value=cur_val,
                required=False,
                max_length=30
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
