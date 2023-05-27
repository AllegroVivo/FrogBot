from __future__ import annotations

from datetime   import datetime
from discord    import Colour, Embed
from typing     import Optional

from assets     import BotImages
################################################################################

__all__ = (
    "InvalidColorError",
    "InvalidFileTypeError",
    "ChannelTypeError",
    "ExceedsMaxLengthError",
    "ChannelNotFoundError"
)

################################################################################
class ErrorMessage(Embed):
    """A subclassed Discord embed object acting as an error message."""

    def __init__(
        self,
        *,
        title: str,
        message: str,
        solution: str,
        description: Optional[str] = None
    ):

        super().__init__(
            title=title,
            description=description if description is not None else Embed.Empty,
            colour=Colour.red()
        )

        self.add_field(
            name="What Happened?",
            value=message,
            inline=True,
        )

        self.add_field(
            name="How to Fix?",
            value=solution,
            inline=True
        )

        self.timestamp = datetime.now()
        self.set_thumbnail(url=BotImages.ErrorFrog.value)

################################################################################
class InvalidColorError(ErrorMessage):
    """An error message for when a user provides an invalid value for
    their profile accent color.

    Overview:
    ---------
    Title:
        "Invalid Color Value"

    Description:
        "You entered ``{invalid_value}`` for your accent color."

    Message:
        "The value you entered couldn't be parsed into a color."

    Solution:
        "Ensure you're entering the 6-character HEX code for your
        desired color with or without the '`#`'."

    """

    def __init__(self, invalid_value: str):

        super().__init__(
            title="Invalid Color Value",
            description=f"You entered `{invalid_value}` for your accent color.",
            message="The value you entered in the modal couldn't be parsed into a HEX color.",
            solution=(
                "Ensure you're entering a valid HEX code comprised of 6 characters, "
                "numbers `0 - 9` and letters `A - F`."
            )
        )

################################################################################
class InvalidFileTypeError(ErrorMessage):
    """An error message for when a user provides an invalid type of file for an image upload.

    Overview:
    ---------
    Title:
        "Invalid File Type"

    Description:
        "You submitted a file of type ``{image_type}`` for your {section_type}."

    Message:
        "The attachment you submitted couldn't be used as a profile image."

    Solution:
        "Only '`.JPEG`', '`.GIF`', '`.WEBP`' and '`.PNG`' type files are allowed."

    """

    def __init__(self, image_type: str, section_type: str):

        super().__init__(
            title="Invalid File Type",
            description=f"You submitted a file of type ``{image_type}`` for your {section_type}.",
            message="The attachment you submitted couldn't be used as a profile image.",
            solution="Only '`.JPEG`', '`.GIF`', '`.WEBP`' and '`.PNG`' type files are allowed."
        )

####################################################################################################
class ChannelTypeError(ErrorMessage):
    """An error message for when a channel of an incorrect type
    was provided for a prompt.

    Overview:
    ---------
    Title:
        "Invalid Channel Type"

    Description:
        [None]

    Message:
        "You entered a channel of an incorrect type."

    Solution:
        "Channel argument must be of type ``{required_type}``."

    """

    def __init__(self, required_type: str):
        super().__init__(
            title="Invalid Channel Type",
            message="You entered a channel of an invalid type.",
            solution=f"Channel argument must be of type {required_type}."
        )

################################################################################
class ExceedsMaxLengthError(ErrorMessage):
    """An error message for when a user attempts to post their profile, but it exceeds the
    Discord-required embed size limit of 6,000 characters.

    Overview:
    ---------
    Title:
        "Profile Too Large!"

    Description:
        "Current Character Count: `{length}`"

    Message:
        "Your profile is larger than Discord's mandatory 6,000-character
        limit for embedded messages."

    Solution:
        "The total number of characters in all your profile's fields may not exceed 6,000."

    """

    def __init__(self, embed_length: int):
        super().__init__(
            title="Profile Too Large!",
            description=f"Current Character Count: `{embed_length}`.",
            message=(
                "Your profile is larger than Discord's mandatory 6,000-character "
                "limit for embedded messages."
            ),
            solution=(
                "The total number of character in all your profile's sections "
                "must not exceed 6,000."
            )
        )

################################################################################
class ChannelNotFoundError(ErrorMessage):
    """An error message for when a user attempts to post their profile, but the selected
    channel is invalid.

    Overview:
    ---------
    Title:
        "Posting Channel Error"

    Description:
        ""

    Message:
        "The selected posting channel wasn't found."

    Solution:
        "Try finalizing one more time. <_<"

    """

    def __init__(self):
        super().__init__(
            title="Posting Channel Error",
            message="The selected posting channel wasn't found",
            solution="Try finalizing one more time... <_<"
        )

################################################################################
