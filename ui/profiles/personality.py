from __future__ import annotations

from discord    import InputTextStyle, Interaction, Member, User
from discord.ui import InputText
from typing     import TYPE_CHECKING, List, Optional, Union

from ui.common import *
from ui.view import *
from utilities  import *

if TYPE_CHECKING:
    from classes.profiles   import ProfilePersonality
################################################################################

__all__ = (
    "PersonalityView",
    "PersonalityModal"
)

################################################################################
class PersonalityModal(FrogModal):

    def __init__(self, section: SectionType, cur_val: Optional[Union[List[str], str]]):

        super().__init__(title=f"Edit Your {section.proper_name}")

        self.section: SectionType = section

        if section is SectionType.Personality or section is SectionType.AboutMe:
            instructions = (
                f"Enter your desired {section.proper_name} section content here. "
                "Note that this accepts markdown, newlines, and emojis, "
                "so really make it your own. ♥"
            )
            max_len = 400 if section is SectionType.Personality else 4000
        else:
            instructions = (
                f"Enter a list of your {section.proper_name} separated by commas. "
                "Minimum three is suggested. Your likes list should "
                "be LONGER than your dislikes to avoid formatting "
                "issues."
            )
            max_len = 250
            cur_val = ", ".join(cur_val) if cur_val is not None else None

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder=f"Enter your {section.proper_name} section content.",
                value=instructions,
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label=section.proper_name,
                placeholder="eg. 'A beautiful froggy princess who loves flies.'",
                value=cur_val,
                required=False,
                max_length=max_len
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value or None
        if self.section is SectionType.Likes or self.section is SectionType.Dislikes:
            if self.value:
                self.value = [titleize(i.strip()) for i in self.value.split(",")]

        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class PersonalitySectionButton(ProfileSectionButton):

    def __init__(self, p: ProfilePersonality, operation: SectionType):
        super().__init__(
            label=operation.proper_name,
            disabled=False,
            row=0
        )

        self.set_style(p.return_section(operation))
        self.operation: SectionType = operation

    async def callback(self, interaction: Interaction):
        person = self.view.personality
        await person.set_personality_section(interaction, self.operation)

        self.set_style(person.return_section(self.operation))

        await edit_message_helper(
            interaction=interaction,
            embed=person.status(),
            view=self.view
        )

################################################################################
class PersonalityView(FrogView):

    def __init__(
        self,
        owner: Union[Member, User],
        profile_obj: ProfilePersonality,
        *args,
        **kwargs
    ):

        super().__init__(owner, *args, **kwargs)

        self.personality: ProfilePersonality = profile_obj

        button_list = [
            PersonalitySectionButton(self.personality, SectionType.Likes),
            PersonalitySectionButton(self.personality, SectionType.Dislikes),
            PersonalitySectionButton(self.personality, SectionType.Personality),
            PersonalitySectionButton(self.personality, SectionType.AboutMe),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
