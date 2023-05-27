import os

from discord    import Intents
from dotenv     import load_dotenv

from utilities  import assert_db_structure

from classes.bot    import FrogBot
from classes.guild  import GuildData
################################################################################

bot = FrogBot(
    description="FrogBot is Best!",
    intents=Intents.default(),
    debug_guilds=[303742308874977280]
)

################################################################################

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

################################################################################

load_dotenv()

bot.run(os.getenv("DISCORD_TOKEN"))

################################################################################
