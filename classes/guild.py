from __future__ import annotations

from discord    import Guild, Member, User
from typing     import List, Optional, Type, TypeVar, Union

from classes.profiles   import Profile
################################################################################

__all__ = ("GuildData", )

GD = TypeVar("GD", bound="GuildData")

################################################################################
class GuildData:

    __slots__ = (
        "parent",
        "profiles",
        "config"
    )

################################################################################
    def __init__(self, parent: Guild):

        self.parent: Guild = parent
        self.profiles: List[Profile] = []

################################################################################
    @classmethod
    def load(cls: Type[GD], parent: Guild) -> GD:

        self: GD = cls.__new__(cls)

        self.parent = parent
        self.profiles = []

        return self

################################################################################
    @property
    def guild_id(self) -> int:

        return self.parent.id

################################################################################
    def get_profile(self, user: Union[Member, User]) -> Profile:

        for profile in self.profiles:
            if profile.user.id == user.id:
                return profile

        profile = Profile.new(user, self)
        self.profiles.append(profile)

        return profile

################################################################################
