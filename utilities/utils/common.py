from __future__ import annotations

import math
import re

from datetime       import datetime
from discord import Colour, Embed, EmbedField
from discord.embeds import EmptyEmbed
from typing         import TYPE_CHECKING, Any, List, Optional, Tuple, Union

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "make_embed",
    "draw_separator",
    "titleize"
)

################################################################################
def make_embed(
    *,
    title: str = EmptyEmbed,
    description: str = EmptyEmbed,
    url: str = EmptyEmbed,
    color: Union[Colour, int] = EmptyEmbed,
    thumbnail_url: str = EmptyEmbed,
    image_url: str = EmptyEmbed,
    author_text: str = EmptyEmbed,
    author_url: str = EmptyEmbed,
    author_icon: str = EmptyEmbed,
    footer_text: str = EmptyEmbed,
    footer_icon: str = EmptyEmbed,
    timestamp: Union[datetime, bool] = False,
    fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None
) -> Embed:
    """Creates and returns a Discord embed with the provided parameters.

    All parameters are optional.

    Parameters:
    -----------
    title: :class:`str`
        The embed's title.

    description: :class:`str`
        The main text body of the embed.

    url: :class:`str`
        The URL for the embed title to link to.

    color: Optional[Union[:class:`Colour`, :class:`int`]]
        The desired accent color. Defaults to :func:`colors.random_all()`

    thumbnail_url: :class:`str`
        The URL for the embed's desired thumbnail image.

    image_url: :class:`str`
        The URL for the embed's desired main image.

    footer_text: :class:`str`
        The text to display at the bottom of the embed.

    footer_icon: :class:`str`
        The icon to display to the left of the footer text.

    author_name: :class:`str`
        The text to display at the top of the embed.

    author_url: :class:`str`
        The URL for the author text to link to.

    author_icon: :class:`str`
        The icon that appears to the left of the author text.

    timestamp: Union[:class:`datetime`, `bool`]
        Whether to add the current time to the bottom of the embed.
        Defaults to ``False``.

    fields: Optional[List[Union[Tuple[:class:`str`, Any, :class:`bool`], :class:`EmbedField`]]]
        List of tuples or EmbedFields, each denoting a field to be added
        to the embed. If entry is a tuple, values are as follows:
            0 -> Name | 1 -> Value | 2 -> Inline (bool)
        Note that in the event of a tuple, the value at index one is automatically cast to a string for you.

    Returns:
    --------
    :class:`Embed`
        The finished embed object.

    """

    embed = Embed(
        colour=color,
        title=title,
        description=description,
        url=url
    )

    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=image_url)

    if author_text is not EmptyEmbed:
        embed.set_author(
            name=author_text,
            url=author_url,
            icon_url=author_icon
        )

    if footer_text is not EmptyEmbed:
        embed.set_footer(
            text=footer_text,
            icon_url=footer_icon
        )

    if isinstance(timestamp, datetime):
        embed.timestamp = timestamp
    elif timestamp is True:
        embed.timestamp = datetime.now()

    if fields is not None:
        if all(isinstance(f, EmbedField) for f in fields):
            embed.fields = fields
        else:
            for f in fields:
                if isinstance(f, EmbedField):
                    embed.fields.append(f)
                elif isinstance(f, tuple):
                    embed.add_field(name=f[0], value=f[1], inline=f[2])
                else:
                    continue

    return embed

################################################################################
def draw_separator(*, text: str = "", num_emoji: int = 0, extra: float = 0.0) -> str:

    text_value = extra + (1.95 * num_emoji)

    for c in text:
        if c == "'":
            text_value += 0.25
        elif c in ("i", "j", ".", " "):
            text_value += 0.30
        elif c in ("I", "!", ";", "|", ","):
            text_value += 0.35
        elif c in ("f", "l", "`", "[", "]"):
            text_value += 0.40
        elif c in ("(", ")", "t"):
            text_value += 0.45
        elif c in ("r", "t", "1" "{", "}", '"', "\\", "/"):
            text_value += 0.50
        elif c in ("s", "z", "*", "-"):
            text_value += 0.60
        elif c in ("x", "^"):
            text_value += 0.65
        elif c in ("a", "c", "e", "g", "k", "v", "y", "J", "7", "_", "=", "+", "~", "<", ">", "?"):
            text_value += 0.70
        elif c in ("n", "o", "u", "2", "5", "6", "8", "9"):
            text_value += 0.75
        elif c in ("b", "d", "h", "p", "q", "E", "F", "L", "S", "T", "Z", "3", "4", "$"):
            text_value += 0.80
        elif c in ("P", "V", "X", "Y", "0"):
            text_value += 0.85
        elif c in ("A", "B", "C", "D", "K", "R", "#", "&"):
            text_value += 0.90
        elif c in ("G", "H", "U"):
            text_value += 0.95
        elif c in ("w", "N", "O", "Q", "%"):
            text_value += 1.0
        elif c in ("m", "W"):
            text_value += 1.15
        elif c == "M":
            text_value += 1.2
        elif c == "@":
            text_value += 1.3

    return "═" * math.ceil(text_value)

################################################################################
def titleize(text: str) -> str:

    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        text
    )

################################################################################
