from __future__ import annotations

from discord    import (
    ButtonStyle,
    Embed,
    InputTextStyle,
    Interaction,
    Member,
    NotFound,
    User
)
from discord.ext.pages  import Page, Paginator
from discord.ui         import Button, InputText
from typing             import TYPE_CHECKING, List, Optional, Union

from utilities  import *

from ui.common import CloseMessageButton, FrogModal, ProfileSectionButton
from ui.view import FrogView

if TYPE_CHECKING:
    from classes.profiles   import AdditionalImage, ProfileImages
################################################################################

__all__ = (
    "ImageStatusView",
    "ImageFrogginator",
    "ImageCaptionModal",
    "AdditionalImageView"
)

################################################################################
class RemoveThumbnailButton(ProfileSectionButton):

    def __init__(self, thumbnail: Optional[str]):
        super().__init__(
            label="Remove Thumbnail",
            disabled=True if not thumbnail else False,
            row=0
        )

        self.set_style(thumbnail)

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        await images.remove_image(interaction, SectionType.Thumbnail)

        self.set_style(images._thumbnail)
        self.disabled = images._thumbnail is None

        await edit_message_helper(
            interaction=interaction,
            embed=images.status(),
            view=self.view
        )

################################################################################
class RemoveMainImageButton(ProfileSectionButton):

    def __init__(self, image: Optional[str]):
        super().__init__(
            label="Remove Main Image",
            disabled=True if not image else False,
            row=0
        )

        self.set_style(image)

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        await images.remove_image(interaction, SectionType.MainImage)

        self.set_style(images._main_image)
        self.disabled = images._main_image is None

        await edit_message_helper(
            interaction=interaction,
            embed=images.status(),
            view=self.view
        )

################################################################################
class PaginateAdditionalImagesButton(ProfileSectionButton):

    def __init__(self, images: List[AdditionalImage]):
        super().__init__(
            label="View Additional Images",
            disabled=True if not images else False,
            row=0
        )

        self.set_style(images)

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        await images.paginate_additional(interaction)

        self.view._close_on_complete = True
        await self.view.stop()  # type: ignore

################################################################################
class ImageStatusView(FrogView):

    def __init__(
        self,
        owner: Union[Member, User],
        profile_obj: ProfileImages,
        *args,
        **kwargs
    ):

        super().__init__(owner, *args, **kwargs)

        self.images: ProfileImages = profile_obj

        button_list = [
            RemoveThumbnailButton(self.images._thumbnail),
            RemoveMainImageButton(self.images._main_image),
            PaginateAdditionalImagesButton(self.images.additional),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
class ImageFrogginator(Paginator):

    def __init__(
        self,
        pages: List[Page],
        images: ProfileImages,
        close_on_complete: bool = False,
        **kwargs
    ):

        super().__init__(pages=pages, author_check=True, **kwargs)

        self.images: ProfileImages = images
        self._interaction: Optional[Interaction] = None
        self._close_on_complete: bool = close_on_complete

################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:

        self._interaction = interaction
        return await super().interaction_check(interaction)

################################################################################
    async def on_timeout(self) -> None:

        try:
            await super().on_timeout()
        except NotFound:
            pass
        except:
            raise

################################################################################
    async def cancel(
        self,
        include_custom: bool = False,
        page: Optional[str, Page, List[Embed], Embed] = None,
    ) -> None:

        if self._close_on_complete:
            if self._interaction is not None:
                try:
                    await self.message.delete()
                except:
                    print("Error in Frogginator Cancel")
        else:
            await super().cancel(include_custom, page)

################################################################################
class ImageCaptionModal(FrogModal):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(title="Enter Image Caption")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the caption for your image.",
                value=(
                    "Enter the caption for your additional image. This text will "
                    "take the place of the ugly-looking link text on your profile."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Image Caption",
                placeholder="eg. 'Having a ribbiting good time~'",
                value=cur_val,
                required=False,
                max_length=50
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.send_message("** **", delete_after=0.1)
        self.stop()

################################################################################
class EditCaptionButton(Button):

    def __init__(self, image_id: str):
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Caption",
            disabled=False,
            row=0
        )

        self.image_id: str = image_id

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images

        caption = await images.get_caption(interaction)
        images.modify_caption(self.image_id, caption)

        await images.paginate_additional(interaction)
        await self.view.cancel()

################################################################################
class RemoveImageButton(Button):

    def __init__(self, image_id: str):
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Image",
            disabled=False,
            row=0
        )

        self.image_id: str = image_id

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        await images.remove_image(interaction, SectionType.AdditionalImages, self.image_id)

        await images.paginate_additional(interaction)
        await self.view.cancel()

################################################################################
class ViewImagesStatusButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="View Images Status",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images

        self.view._close_on_complete = True
        await self.view.cancel()  # type: ignore

        await images.set(interaction)

################################################################################
class AdditionalImageView(FrogView):

    def __init__(self, owner: Union[Member, User], images: ProfileImages, image_id: str = None):

        super().__init__(owner, close_on_complete=True)

        self.images: ProfileImages = images

        if image_id is not None:
            self.add_item(EditCaptionButton(image_id))
            self.add_item(RemoveImageButton(image_id))

        self.add_item(ViewImagesStatusButton())
        self.add_item(CloseMessageButton())

################################################################################
