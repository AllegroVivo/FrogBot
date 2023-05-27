import os
import psycopg2

from discord    import Guild
from dotenv     import load_dotenv
from typing     import List
################################################################################

__all__ = (
    "db_connection",
    "assert_db_structure",
    "new_guild_entry",
    "assert_guild_records"
)

################################################################################

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db_connection = psycopg2.connect(DATABASE_URL, sslmode="require")
print("Database connection initialized...")

################################################################################
def assert_db_structure() -> None:

    c = db_connection.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS guild_config("
        "guild_id BIGINT UNIQUE NOT NULL,"
        "post_channels TEXT,"
        "CONSTRAINT guild_config_pkey PRIMARY KEY (guild_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS profiles("
        "profile_id TEXT UNIQUE NOT NULL,"
        "user_id BIGINT NOT NULL,"
        "guild_id BIGINT,"
        "CONSTRAINT profile_pkey PRIMARY KEY (profile_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS details("
        "profile_id TEXT UNIQUE NOT NULL,"
        "char_name TEXT,"
        "url TEXT,"
        "color INTEGER,"
        "jobs TEXT,"
        "rates TEXT,"
        "post_url TEXT,"
        "CONSTRAINT details_pkey PRIMARY KEY (profile_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS personality("
        "profile_id TEXT UNIQUE NOT NULL,"
        "likes TEXT,"
        "dislikes TEXT,"
        "personality TEXT,"
        "aboutme TEXT,"
        "CONSTRAINT personality_pkey PRIMARY KEY (profile_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS ataglance("
        "profile_id TEXT UNIQUE NOT NULL,"
        "gender TEXT,"
        "pronouns TEXT,"
        "race TEXT,"
        "clan TEXT,"
        "orientation TEXT,"
        "height TEXT,"
        "age TEXT,"
        "mare TEXT,"
        "CONSTRAINT ataglance_pkey PRIMARY KEY (profile_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS images("
        "profile_id TEXT UNIQUE NOT NULL,"
        "thumbnail TEXT,"
        "main_image TEXT,"
        "CONSTRAINT images_pkey PRIMARY KEY (profile_id))"
    )

    c.execute(
        "CREATE TABLE IF NOT EXISTS addl_images("
        "profile_id TEXT,"
        "image_id TEXT UNIQUE NOT NULL,"
        "url TEXT,"
        "caption TEXT,"
        "CONSTRAINT addl_images_pkey PRIMARY KEY (image_id))"
    )

    c.execute(
        "CREATE OR REPLACE VIEW profile_master "
        "AS "
        # Data indices 0 - 2 Internal
        "SELECT p.profile_id,"
        "p.user_id,"
        "p.guild_id,"
        # Data indices 3 - 8 Details
        "d.char_name,"
        "d.url AS custom_url,"
        "d.color,"
        "d.jobs,"
        "d.rates,"
        "d.post_url,"
        # Data indices 9 - 12 Personality
        "pr.likes,"
        "pr.dislikes,"
        "pr.personality,"
        "pr.aboutme,"
        # Data indices 13 - 20 At A Glance
        "a.gender,"
        "a.pronouns,"
        "a.race,"
        "a.clan,"
        "a.orientation,"
        "a.height,"
        "a.age,"
        "a.mare,"
        # Data indices 21 - 22 Images
        "i.thumbnail,"
        "i.main_image "
        "FROM profiles p "
        "JOIN details d ON p.profile_id = d.profile_id "
        "JOIN personality pr ON p.profile_id = pr.profile_id "
        "JOIN ataglance a on p.profile_id = a.profile_id "
        "JOIN images i on p.profile_id = i.profile_id;"
    )

    db_connection.commit()
    c.close()

    return

################################################################################
def assert_guild_records(guilds: List[Guild]) -> None:

    c = db_connection.cursor()

    for guild in guilds:
        c.execute(
            "INSERT INTO guild_config (guild_id, post_channels) VALUES (%s, %s) "
            "ON CONFLICT (guild_id) DO NOTHING",
            (guild.id, [])
        )

    db_connection.commit()
    c.close()

    return

################################################################################
def new_guild_entry(guild_id: int) -> None:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO guild_config (guild_id, post_channels) VALUES (%s, %s)",
        (guild_id, [])
    )

    db_connection.commit()
    c.close()

    return

################################################################################
