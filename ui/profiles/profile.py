from __future__ import annotations

from discord    import (
    ButtonStyle,
    Interaction,
    Member,
    SelectOption,
    TextChannel,
    User
)
from discord.ui import Button, Select
from typing     import TYPE_CHECKING, List, Optional, Union

from ui.common import CloseMessageButton, CloseMessageView
from ui.view import FrogView

if TYPE_CHECKING:
    from classes.profiles   import Profile
################################################################################

__all__ = (
    "ProfileChannelSelectorView",
    "ProfilePreView"
)

################################################################################
class ProfileChannelSelect(Select):

    def __init__(self, options: List[SelectOption]):
        super().__init__(
            placeholder="Select Your Posting Channel...",
            options=options,
            disabled=True if len(options) == 0 else False
        )

    async def callback(self, interaction: Interaction):
        self.view.value = int(self.values[0])
        self.view.complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore

################################################################################
class CancelButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.danger,
            label="Cancel",
            disabled=False,
            row=4
        )

    async def callback(self, interaction: Interaction):
        self.view.value = False
        self.view.complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore

################################################################################
class ProfileChannelSelectorView(FrogView):

    def __init__(self, owner: Union[Member, User], channels: List[TextChannel]):

        super().__init__(owner, close_on_complete=True)

        options = []
        for ch in channels:
            options.append(
                SelectOption(
                    label=ch.name,
                    value=str(ch.id)
                )
            )

        self.add_item(ProfileChannelSelect(options))
        self.add_item(CancelButton())

################################################################################
class ProfilePreviewButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Main Profile",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        profile, _ = self.view.profile.compile()
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=profile, view=view)
        await view.wait()


################################################################################
class AboutMePreviewButton(Button):

    def __init__(self, aboutme: Optional[str]):
        super().__init__(
            style=ButtonStyle.primary if aboutme is not None else ButtonStyle.secondary,
            label="About Me Section",
            disabled=aboutme is None,
            row=0
        )

    async def callback(self, interaction: Interaction):
        _, aboutme = self.view.profile.compile()
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=aboutme, view=view)
        await view.wait()

################################################################################
class ProfilePreView(FrogView):

    def __init__(self, owner: Union[Member, User], profile_obj: Profile):
        super().__init__(owner)

        self.profile: Profile = profile_obj

        button_list = [
            ProfilePreviewButton(),
            AboutMePreviewButton(self.profile.personality._aboutme),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
