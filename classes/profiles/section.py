from __future__ import annotations

from discord    import Embed, Interaction, PartialEmoji
from typing     import TYPE_CHECKING, Any, Optional, Tuple, Type, TypeVar

from assets     import BotEmojis
from utilities  import NS

if TYPE_CHECKING:
    from classes.profiles.profile import Profile
################################################################################

__all__ = ("ProfileSection", )

T = TypeVar("T")

################################################################################
class ProfileSection:

    __slots__ = ("parent", )

    def __init__(self, parent: Profile, *args, **kwargs):

        self.parent: Profile = parent

################################################################################
    @classmethod
    def load(cls: Type[T], parent: Profile, data: Any) -> T:

        raise NotImplementedError

################################################################################
    def status(self) -> Embed:

        raise NotImplementedError

################################################################################
    def progress(self) -> str:

        raise NotImplementedError

################################################################################
    def compile(self) -> Tuple[Any, ...]:

        raise NotImplementedError

################################################################################
    async def set(self, interaction: Interaction) -> None:

        raise NotImplementedError

################################################################################
    def update(self) -> None:

        raise NotImplementedError

################################################################################
    @staticmethod
    def progress_emoji(attribute: Optional[Any]) -> str:

        if isinstance(attribute, list):
            if len(attribute) == 0:
                return str(BotEmojis.Cross.value)

        if attribute in (None, NS, Embed.Empty):
            return str(BotEmojis.Cross.value)

        return str(BotEmojis.Check.value)

################################################################################
