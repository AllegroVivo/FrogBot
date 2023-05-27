from __future__ import annotations

from discord            import Attachment, Embed, EmbedField, Interaction
from discord.ext.pages  import Page
from typing             import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar

from assets         import *
from ui.profiles    import *
from utilities      import *

from .section   import ProfileSection

if TYPE_CHECKING:
    from .profile   import Profile
################################################################################

__all__ = (
    "ProfileImages",
    "AdditionalImage"
)

AI = TypeVar("AI", bound="AdditionalImage")
PI = TypeVar("PI", bound="ProfileImages")

################################################################################
class AdditionalImage:

    __slots__ = (
        "id",
        "url",
        "_caption"
    )

################################################################################
    def __init__(self, *, image_id: str, url: str, caption: Optional[str] = None):

        self.id: str = image_id
        self.url: str = url
        self._caption: Optional[str] = caption

################################################################################
    @classmethod
    def new(cls: Type[AI], parent_id: str, url: str, caption: Optional[str]) -> AI:

        image_id = new_additional_image(parent_id, url, caption)

        self = cls.__new__(cls)

        self.id = image_id
        self.url = url
        self._caption = caption

        return self

################################################################################
    def page(self, interaction: Interaction, parent: ProfileImages) -> Page:

        return Page(
            embeds=[
                make_embed(
                    title="Additional Images",
                    image_url=self.url,
                    footer_text=f"Caption: {self.caption}" if self.caption is not NS else Embed.Empty,
                    timestamp=False
                )
            ],
            custom_view=AdditionalImageView(interaction.user, parent, self.id)
        )

################################################################################
    def compile(self) -> str:

        if self.caption is NS:
            return self.url

        return f"[{self.caption}]({self.url})"

################################################################################
    @property
    def caption(self) -> Optional[str]:

        return self._caption or NS

################################################################################
    @caption.setter
    def caption(self, value: Optional[str]) -> None:

        self._caption = value
        self.update()

################################################################################
    def delete(self) -> None:

        c = db_connection.cursor()
        c.execute("DELETE FROM addl_images WHERE image_id = %s", (self.id, ))

        db_connection.commit()
        c.close()

        return

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE addl_images SET caption = %s WHERE image_id = %s",
            (self._caption, self.id)
        )

        db_connection.commit()
        c.close()

        return

################################################################################
class ProfileImages(ProfileSection):

    __slots__ = (
        "_thumbnail",
        "_main_image",
        "additional"
    )

################################################################################
    def __init__(self, parent: Profile, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        self._thumbnail: Optional[str] = kwargs.pop("thumbnail", None)
        self._main_image: Optional[str] = kwargs.pop("main_image", None)
        self.additional: List[AdditionalImage] = kwargs.pop("additional", [])

################################################################################
    @classmethod
    def load(cls: Type[PI], parent: Profile, data: List[Optional[str]]) -> PI:

        return cls(
            parent=parent,
            thumbnail=data[0],
            main_image=data[1],
            additional=[]
        )

################################################################################
    def status(self) -> Embed:

        down_arrow = BotEmojis.ArrowDown.value
        right_arrow = BotEmojis.ArrowRight.value

        fields: List[EmbedField] = [
            EmbedField(draw_separator(extra=30), "** **", False),
            self.additional_status(),
            EmbedField(draw_separator(extra=30), "** **", False),
            EmbedField(
                name="__Main Image__",
                value=f"-{down_arrow}{down_arrow}{down_arrow}-",
                inline=True
            ),
            EmbedField("** **", "** **", True),
            EmbedField(
                name="__Thumbnail__",
                value=f"-{right_arrow}{right_arrow}{right_arrow}-",
                inline=True
            ),
        ]

        return make_embed(
            color=self.parent.color,
            title=f"Image Details for `{self.parent.char_name}`",
            description=(
                "The buttons below allow you to remove and image attached to your profile\n"
                "or to view a paginated list of your current additional images.\n\n"
                
                "***To change your thumbnail and main image assets, or to add an additional image\n"
                "to your profile, use the `/profiles add_image` command.***"
            ),
            thumbnail_url=self._thumbnail or BotImages.ThumbnailMissing.value,
            image_url=self._main_image or BotImages.MainImageMissing.value,
            timestamp=False,
            fields=fields
        )

################################################################################
    def additional_status(self) -> EmbedField:

        if not self.additional:
            return EmbedField(
                name="__Addtional Images__",
                value=str(NS),
                inline=False
            )

        return self.compile_additional()

################################################################################
    def create_pages(self, interaction: Interaction) -> List[Page]:

        pages: List[Page] = []
        for img in self.additional:
            pages.append(img.page(interaction, self))

        if not pages:
            pages.append(
                Page(
                    embeds=[
                        make_embed(
                            title="Additional Images",
                            description="`No Images Uploaded!`",
                            timestamp=False
                        )
                    ],
                    custom_view=AdditionalImageView(interaction.user, self)
                )
            )

        return pages

################################################################################
    def compile_additional(self) -> Optional[EmbedField]:

        if not self.additional:
            return

        images_text = ""
        for image in self.additional:
            images_text += f"{image.compile()}\n"

        return EmbedField(
            name=f"{BotEmojis.Camera.value} __Additional Images__ {BotEmojis.Camera.value}",
            value=images_text,
            inline=False
        )

################################################################################
    def progress(self) -> str:

        em_thumb = self.progress_emoji(self._thumbnail)
        em_mainimg = self.progress_emoji(self._main_image)
        em_addl = self.progress_emoji(self.additional)

        return (
            f"{draw_separator(extra=15)}\n"
            "__**Images**__\n"
            f"{em_thumb} -- Thumbnail *(Upper-Right)*\n"
            f"{em_mainimg} -- Main Image *(Bottom-Center)*\n"
            f"{em_addl} -- (`{len(self.additional)}`) -- Additional Images\n"
        )

################################################################################
    @property
    def thumbnail(self) -> Optional[str]:

        return self._thumbnail or Embed.Empty

################################################################################
    @thumbnail.setter
    def thumbnail(self, value: Optional[str]) -> None:

        self._thumbnail = value
        self.update()

################################################################################
    @property
    def main_image(self) -> Optional[str]:

        return self._main_image or Embed.Empty

################################################################################
    @main_image.setter
    def main_image(self, value: Optional[str]) -> None:

        self._main_image = value
        self.update()

################################################################################
    async def set(self, interaction: Interaction) -> None:

        embed = self.status()
        view = ImageStatusView(interaction.user, self)

        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        return

################################################################################
    @staticmethod
    async def get_caption(interaction: Interaction) -> Optional[str]:

        modal = ImageCaptionModal()

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        return modal.value

################################################################################
    def compile(self) -> Tuple[Optional[str], Optional[str], Optional[EmbedField]]:

        return (
            self.thumbnail,
            self.main_image,
            self.compile_additional()
        )

################################################################################
    def modify_caption(self, image_id: str, caption: Optional[str]) -> None:

        for i in self.additional:
            if i.id == image_id:
                i.caption = caption
                return

################################################################################
    def additional_images_from_data(self, data: List[Tuple[str, str, str, Optional[str]]]) -> None:

        for i in data:
            self.additional.append(
                AdditionalImage(
                    image_id=i[1],
                    url=i[2],
                    caption=i[3]
                )
            )

################################################################################
    async def handle_image(self, interaction: Interaction, section: SectionType, image: Attachment) -> None:

        if image.content_type not in (
            "image/jpeg", "image/png", "image/gif", "image/apng", "image/webp"
        ):
            error = InvalidFileTypeError(image.content_type, section.proper_name)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        if section is not SectionType.AdditionalImages:
            await interaction.response.defer()
        else:
            if len(self.additional) == 10:
                error = TooManyImages()
                await interaction.response.send_message(embed=error, ephemeral=True)
                return

            caption = await self.get_caption(interaction)

        image_url = await interaction.client.dump_image(image)  # type: ignore
        message = ""

        if section is SectionType.Thumbnail:
            self.thumbnail = image_url
            message = "Your thumbnail image was updated successfully!"
        elif section is SectionType.MainImage:
            self.main_image = image_url
            message = "Your main image was updated successfully!"
        elif section is SectionType.AdditionalImages:
            self.additional.append(AdditionalImage.new(self.parent.id, image_url, caption))
            message = "A new additional image was added to your profile!"

        confirm = self.status()
        confirm.title = "Success!"
        confirm.description = message

        view = ImageStatusView(interaction.user, self)

        await interaction.followup.send(embed=confirm, view=view)
        await view.wait()

        return

################################################################################
    async def remove_image(
        self,
        interaction: Interaction,
        section: SectionType,
        image_id: Optional[str] = None
    ) -> None:

        thumbnail_img = main_img = footer_text = Embed.Empty
        if section is SectionType.Thumbnail:
            thumbnail_img = self.thumbnail
        elif section is SectionType.MainImage:
            main_img = self.main_image
        else:
            image = self.get_additional(image_id)
            main_img = image.url
            footer_text = image.caption if image.caption is not NS else "(No Caption)"

        confirm = make_embed(
            color=self.parent.color,
            title="Confirm Image Removal",
            description=(
                "Confirm that you want to remove the attached image from the "
                "corresponding spot on your profile.\n\n"
                
                "*(It's gone forever and you'll need to re-upload it again if "
                "you change your mind!)*"
            ),
            thumbnail_url=thumbnail_img,
            image_url=main_img,
            footer_text=footer_text,
            timestamp=False
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.response.send_message(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        if section is SectionType.Thumbnail:
            self.thumbnail = None
        elif section is SectionType.MainImage:
            self.main_image = None
        else:
            image.delete()
            for i, img in enumerate(self.additional):
                if img.id == image_id:
                    self.additional.pop(i)

        return

################################################################################
    def get_additional(self, image_id: str) -> Optional[AdditionalImage]:

        if self.additional:
            for image in self.additional:
                if image.id == image_id:
                    return image

################################################################################
    async def paginate_additional(self, interaction: Interaction) -> None:

        frogginator = ImageFrogginator(
            pages=self.create_pages(interaction),
            images=self,
            show_disabled=True,
            close_on_complete=True,
            loop_pages=True,
            default_button_row=1,
            timeout=180
        )
        await frogginator.respond(interaction)

        return

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE images SET thumbnail = %s, main_image = %s WHERE profile_id = %s",
            (self._thumbnail, self._main_image, self.parent.id)
        )

        db_connection.commit()
        c.close()

        return

################################################################################
