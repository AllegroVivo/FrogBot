from __future__ import annotations

from discord            import ButtonStyle, Interaction, Member, User
from discord.ext.pages  import Paginator
from discord.ui         import Button, button, InputText, Modal, Select, View
from typing             import TYPE_CHECKING, Any, Optional, Union

from .view      import FrogView

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "ProfileSectionButton",
    "FrogModal",
    "ConfirmCancelView",
    "CloseMessageButton",
    "CloseMessageView"
)

################################################################################
class ProfileSectionButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

################################################################################
    def set_style(self, attribute: Optional[Any]) -> None:

        if attribute:
            self.style = ButtonStyle.primary
        else:
            self.style = ButtonStyle.secondary

################################################################################
class FrogModal(Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.complete: bool = False
        self.value: Optional[Any] = None

################################################################################
class ConfirmCancelView(FrogView):

    def __init__(self, owner: Union[Member, User], *args, **kwargs):

        super().__init__(owner, *args, close_on_complete=True, **kwargs)

    @button(
        style=ButtonStyle.success,
        label="Confirm",
        disabled=False,
        row=0
    )
    async def confirm(self, btn: Button, interaction: Interaction):
        self.value = True
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

    @button(
        style=ButtonStyle.danger,
        label="Cancel",
        disabled=False,
        row=0
    )
    async def cancel(self, btn: Button, interaction: Interaction):
        self.value = False
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

################################################################################
class CloseMessageButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.success,
            label="Close Message",
            disabled=False,
            row=4
        )

    async def callback(self, interaction: Interaction):
        self.view.value = True
        self.view.complete = True
        self.view._close_on_complete = True

        await interaction.response.edit_message()

        if isinstance(self.view, Paginator):
            await self.view.cancel()
        else:
            await self.view.stop()  # type: ignore

################################################################################
class CloseMessageView(FrogView):

    def __init__(self, owner: Union[Member, User]):
        super().__init__(owner, close_on_complete=True)

        self.add_item(CloseMessageButton())

################################################################################
