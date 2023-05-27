from __future__ import annotations

from .common    import ErrorMessage
################################################################################

__all__ = (
    "HeightInputError",
    "TooManyImages",
    "CharNameNotSet",
    "NoPostChannelsConfigured"
)

################################################################################
class HeightInputError(ErrorMessage):
    """An error message for when a user-provided value can't be parsed
    into a height value. (ie. ft./in. or cm.)

    Overview:
    ---------
    Title:
        "Invalid Height Input"

    Description:
        ""

    Message:
        "The value: {entry} couldn't be interpreted."

    Solution:
        "The following are acceptable input styles:
            - `X feet X inches`
            - `X ft. X in.`
            - `X in.`
            - `X cm.`"

    """

    def __init__(self, entry: str):

        super().__init__(
            title="Invalid Height Input",
            message=f"The value `{entry}` couldn't be interpreted.",
            solution=(
                "The following are acceptable input styles:\n"
                "- `X feet X inches`\n"
                "- `X ft. X in.`\n"
                "- `X in.`\n"
                "- `X cm.`"
            )
        )

################################################################################
class TooManyImages(ErrorMessage):
    """An error message for when a user already has the maximum of 10
    images on their profile.

    Overview:
    ---------
    Title:
        "Too Many Images"

    Description:
        ""

    Message:
        "You already have the maximum of 10 additional images on your profile."

    Solution:
        "Sorry, I can't add any more because of formatting restrictions. :("

    """

    def __init__(self):
        super().__init__(
            title="Image Maximum Reached",
            message="You already have the maximum of 10 additional images on your profile.",
            solution="Sorry, I can't add any more because of formatting restrictions. :("
        )

####################################################################################################
class CharNameNotSet(ErrorMessage):
    """An error message for when a user attempts to post their profile without having
    set a character name for themselves.

    Overview:
    ---------
    Title:
        "No Character Name Set"

    Description:
        ""

    Message:
        "You haven't set a character name for yourself!"

    Solution:
        "You can't post until you at least do that. Use `/profile details` to change it."

    """

    def __init__(self):
        super().__init__(
            title="Character Name Not Set",
            message="You haven't set a character name for your profile!",
            solution=(
                "You can't post your profile until you complete at least that much.\n"
                "Use `/profile details` to change it."
            )
        )

################################################################################
class NoPostChannelsConfigured(ErrorMessage):
    """An error message for when a user attempts to post their profile, but server admins
    have yet to set any available posting channels for the bot.

    Overview:
    ---------
    Title:
        "No Profile Channels Set-Up"

    Description:
        "*(You're going to want to contact a server administrator for this one.)*"

    Message:
        "There are no configured profile posting channels for your server."

    Solution:
        "Have a server administrator run the `/config post_channel` command to set one up."

    """

    def __init__(self):
        super().__init__(
            title="No Profile Channels Configured",
            description="*(You're going to want to contact a server administrator for this one.)*",
            message="There are not configured profile posting channels for your server.",
            solution=(
                "Have a server administrator run the `/profile post_channel` "
                "command to set one up."
            )
        )

################################################################################
