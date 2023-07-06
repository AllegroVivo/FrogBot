from enum       import Enum
from typing     import List

from discord    import SelectOption

from .common    import FrogEnum
################################################################################

__all__ = (
    "Gender",
    "Pronoun",
    "Race",
    "Clan",
    "Orientation"
)

################################################################################
class Gender(FrogEnum):

    Male = 1
    Female = 2
    NonBinary = 3
    Custom = 4

################################################################################
    @property
    def proper_name(self) -> str:

        return "Non-Binary" if self.value == 3 else self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(
                label=gender.proper_name,
                value=str(gender.value)
            ) for gender in Gender
        ]

################################################################################
class Pronoun(FrogEnum):

    He = 1
    Him = 2
    His = 3
    She = 4
    Her = 5
    Hers = 6
    They = 7
    Them = 8
    Theirs = 9
    Ze = 10
    Hir = 11
    Per = 12
    Pers = 13
    It = 14
    Its = 15

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(
                label=pronoun.proper_name,
                value=str(pronoun.value)
            ) for pronoun in Pronoun
        ]

################################################################################
class Race(FrogEnum):

    Aura = 1
    Elezen = 2
    FantasiaAddict = 3
    Hrothgar = 4
    Hyur = 5
    Lalafell = 6
    Miqote = 7
    Roegadyn = 8
    Viera = 9
    Custom = 999

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "Au ra"
        elif self.value == 3:
            return "Fantasia Addict"
        elif self.value == 7:
            return "Miqo'te"
        else:
            return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(
                label=race.proper_name,
                value=str(race.value)
            ) for race in Race
        ]

################################################################################
class Clan(Enum):

    Dunesfolk = 1
    Duskwight = 2
    Helion = 3
    Hellsguard = 4
    Highlander = 5
    KeeperOfTheMoon = 6
    Midlander = 7
    Plainsfolk = 8
    Raen = 9
    Rava = 10
    SeaWolf = 11
    SeekerOfTheSun = 12
    TheLost = 13
    Veena = 14
    Wildwood = 15
    Xaela = 16
    Custom = 998
    NA = 999

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 6:
            return "Keeper of the Moon"
        elif self.value == 11:
            return "Sea Wolf"
        elif self.value == 12:
            return "Seeker of the Sun"
        elif self.value == 13:
            return "The Lost"

        return self.name

################################################################################
    @staticmethod
    def select_options(race: Race) -> List[SelectOption]:

        if race is Race.Aura:
            clan_options = [Clan.Raen, Clan.Xaela, Clan.Custom, Clan.NA]
        elif race is Race.Elezen:
            clan_options = [Clan.Duskwight, Clan.Wildwood, Clan.Custom, Clan.NA]
        elif race is Race.Hrothgar:
            clan_options = [Clan.Helion, Clan.TheLost, Clan.Custom, Clan.NA]
        elif race is Race.Hyur:
            clan_options = [Clan.Highlander, Clan.Midlander, Clan.Custom, Clan.NA]
        elif race is Race.Lalafell:
            clan_options = [Clan.Dunesfolk, Clan.Plainsfolk, Clan.Custom, Clan.NA]
        elif race is Race.Miqote:
            clan_options = [Clan.KeeperOfTheMoon, Clan.SeekerOfTheSun, Clan.Custom, Clan.NA]
        elif race is Race.Roegadyn:
            clan_options = [Clan.Hellsguard, Clan.SeaWolf, Clan.Custom, Clan.NA]
        elif race is Race.Viera:
            clan_options = [Clan.Rava, Clan.Veena, Clan.Custom, Clan.NA]
        else:
            clan_options = [Clan.Custom, Clan.NA]

        return [
            SelectOption(
                label=clan.proper_name,
                value=str(clan.value)
            ) for clan in clan_options
        ]

################################################################################
class Orientation(FrogEnum):

    Aromantic = 1
    Asexual = 2
    Bisexual = 3
    Demiromantic = 4
    Demisexual = 5
    Gay = 6
    Lesbian = 7
    Pansexual = 8
    Straight = 9
    Custom = 999

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(
                label=orientation.proper_name,
                value=str(orientation.value)
            ) for orientation in Orientation
        ]

################################################################################
