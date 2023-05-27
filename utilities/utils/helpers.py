from __future__ import annotations

from discord    import Interaction
################################################################################

__all__ = (
    "edit_message_helper",
)

################################################################################
async def edit_message_helper(interaction: Interaction, *args, **kwargs) -> None:

    try:
        await interaction.message.edit(*args, **kwargs)
    except:
        try:
            await interaction.edit_original_response(*args, **kwargs)
        except:
            print("Edit Message Helper FAILED")

################################################################################
