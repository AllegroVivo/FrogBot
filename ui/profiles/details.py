from __future__ import annotations

from discord    import Colour, InputTextStyle, Interaction, Member, User
from discord.ui import InputText
from typing     import TYPE_CHECKING, List, Optional, Union

from utilities  import *

from ui.common import CloseMessageButton, FrogModal, ProfileSectionButton
from ui.view import FrogView

if TYPE_CHECKING:
    from classes.profiles   import ProfileDetails
################################################################################

__all__ = (
    "DetailsStatusView",
    "CharNameModal",
    "ProfileURLModal",
    "ColorModal",
    "JobsModal",
    "RatesModal"
)

################################################################################
class RatesButton(ProfileSectionButton):

    def __init__(self, rates: Optional[str]):

        super().__init__(
            label="Rates",
            disabled=False,
            row=1
        )

        self.set_style(rates)

    async def callback(self, interaction: Interaction):
        details = self.view.details
        await details.set_rates(interaction)

        self.set_style(details._rates)

        await edit_message_helper(
            interaction=interaction,
            embed=details.status(),
            view=self.view
        )

################################################################################
class JobsButton(ProfileSectionButton):

    def __init__(self, jobs: Optional[List[str]]):

        super().__init__(
            label="RP Jobs",
            disabled=False,
            row=1
        )

        self.set_style(jobs)

    async def callback(self, interaction: Interaction):
        details = self.view.details
        await details.set_jobs(interaction)

        self.set_style(details._jobs)

        await edit_message_helper(
            interaction=interaction,
            embed=details.status(),
            view=self.view
        )

################################################################################
class ColorButton(ProfileSectionButton):

    def __init__(self, color: Optional[Colour]):

        super().__init__(
            label="Accent Color",
            disabled=False,
            row=0
        )

        self.set_style(color)

    async def callback(self, interaction: Interaction):
        details = self.view.details
        await details.set_color(interaction)

        self.set_style(details._color)

        await edit_message_helper(
            interaction=interaction,
            embed=details.status(),
            view=self.view
        )

################################################################################
class URLButton(ProfileSectionButton):

    def __init__(self, url: Optional[str]):

        super().__init__(
            label="Custom URL",
            disabled=False,
            row=0
        )

        self.set_style(url)

    async def callback(self, interaction: Interaction):
        details = self.view.details
        await details.set_url(interaction)

        self.set_style(details._url)

        await edit_message_helper(
            interaction=interaction,
            embed=details.status(),
            view=self.view
        )

################################################################################
class CharNameButton(ProfileSectionButton):

    def __init__(self, name: Optional[str]):

        super().__init__(
            label="Character Name",
            disabled=False,
            row=0
        )

        self.set_style(name)

    async def callback(self, interaction: Interaction):
        details = self.view.details
        await details.set_char_name(interaction)

        self.set_style(details._char_name)

        await edit_message_helper(
            interaction=interaction,
            embed=details.status(),
            view=self.view
        )

################################################################################
class DetailsStatusView(FrogView):

    def __init__(self, owner: Union[Member, User], details: ProfileDetails, *args, **kwargs):

        super().__init__(owner, *args, **kwargs)

        self.details: ProfileDetails = details

        button_list = [
            CharNameButton(self.details._char_name),
            URLButton(self.details._url),
            ColorButton(self.details._color),
            JobsButton(self.details._jobs),
            RatesButton(self.details._rates),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
class CharNameModal(FrogModal):

    def __init__(self, cur_val: Optional[str]):

        super().__init__(title="Character Name Modal")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your character's name.",
                value="Enter or edit your character's name on the line below.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Character Name",
                placeholder="eg. 'Allegro Vivo'",
                value=cur_val,
                required=True,
                max_length=50
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ProfileURLModal(FrogModal):

    def __init__(self, cur_val: Optional[str]):

        super().__init__(title="Edit Profile URL")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your desired custom URL.",
                value=(
                    "Enter your desired custom URL.\n"
                    "This will be the link that your character name will redirect to if clicked."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Custom URL",
                placeholder="eg. 'https://twitter.com/HomeHopping'",
                value=cur_val,
                required=False
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ColorModal(FrogModal):

    def __init__(self, cur_val: Optional[Colour]):

        super().__init__(title="Custom Profile URL")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your desired accent color.",
                value=(
                    "Enter the 6-character HEX code for your desired profile accent color.\n"
                    "Google Color Picker:\n"
                    "https://g.co/kgs/psoVFb"
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Accent Color HEX",
                placeholder="#4ABC23",
                value=str(cur_val).upper() if cur_val is not None else None,
                min_length=6,
                max_length=7,
                required=True
            )
        )

    async def callback(self, interaction: Interaction):
        value = self.children[1].value.upper()
        if value.startswith("#"):
            value = value[1:]

        try:
            self.value = int(value, 16) if self.children[1].value else None
        except:
            error = InvalidColorError(value)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
        else:
            self.complete = True
            await interaction.response.edit_message()

        self.stop()

################################################################################
class JobsModal(FrogModal):

    def __init__(self, cur_val: Optional[List[str]]):

        super().__init__(title="Edit Character Jobs")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter up to three RP professions for your character.",
                value=(
                    "Enter the RP professions to display on your profile. "
                    "(Limit 3 for formatting reasons.)\n"
                    "If you want to delete a job, just empty the corresponding box "
                    "and submit the dialog."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Job #1",
                placeholder="eg. 'Professional Frog'",
                value=cur_val[0] if cur_val is not None and len(cur_val) > 0 else None,
                max_length=20,
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Job #2",
                placeholder="eg. 'Taco Wrangler'",
                value=cur_val[1] if cur_val is not None and len(cur_val) > 1 else None,
                max_length=20,
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Job #3",
                placeholder="eg. 'Stunt Camel'",
                value=cur_val[2] if cur_val is not None and len(cur_val) > 2 else None,
                max_length=20,
                required=False
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = [
            self.children[1].value if self.children[1].value else None,
            self.children[2].value if self.children[2].value else None,
            self.children[3].value if self.children[3].value else None,
        ]
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class RatesModal(FrogModal):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(title="Profile Rates Section")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your Rates section information below.",
                value=(
                    "Enter the information for your 'Rates' section "
                    "exactly as you want it displayed on your profile.\n"
                    "This supports markdown and emojis."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Rates Section",
                placeholder="eg. '250k gil per photoshoot'",
                value=cur_val,
                max_length=500,
                required=False
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
