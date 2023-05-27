from enum       import Enum
from typing     import List

from discord    import SelectOption
################################################################################

__all__ = (
    "SectionType",
)

################################################################################
class FrogEnum(Enum):

    @property
    def proper_name(self) -> str:

        raise NotImplementedError

    @staticmethod
    def select_options() -> List[SelectOption]:

        raise NotImplementedError

################################################################################
class SectionType(FrogEnum):

    Likes = 1
    Dislikes = 2
    Personality = 3
    AboutMe = 4
    Thumbnail = 5
    MainImage = 6
    AdditionalImages = 7

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 4:
            return "About Me"
        elif self.value == 6:
            return "Main Image"
        elif self.value == 7:
            return "Additional Image"

        return self.name

################################################################################
