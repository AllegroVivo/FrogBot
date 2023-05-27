from enum       import Enum

from discord    import PartialEmoji
################################################################################

__all__ = ("BotEmojis", )

################################################################################
class BotEmojis(Enum):

    ArrowDown = PartialEmoji.from_str("⬇️")
    ArrowLeft = PartialEmoji.from_str("⬅️")
    ArrowRight = PartialEmoji.from_str("➡️")
    Camera = PartialEmoji.from_str("<:camera:958816462406033498>")
    Check = PartialEmoji.from_str("<:check:958615684869414962>")
    Cross = PartialEmoji.from_str("❌")
    Envelope = PartialEmoji.from_str("💌")
    Eyes = PartialEmoji.from_str("👀")
    FlyingMoney = PartialEmoji.from_str("💸")
    Goose = PartialEmoji.from_str("<:goose:958828235058208829>")
    Scroll = PartialEmoji.from_str("📜")

################################################################################
