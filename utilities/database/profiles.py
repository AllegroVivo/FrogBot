import uuid

from typing     import Optional

from .system    import db_connection
################################################################################

__all__ = (
    "new_profile_entry",
    "new_additional_image"
)

################################################################################
def new_profile_entry(guild_id: int, user_id: int) -> Optional[str]:

    c = db_connection.cursor()
    c.execute(
        "SELECT * FROM profiles WHERE guild_id = %s and user_id = %s",
        (guild_id, user_id)
    )

    record = c.fetchone()
    if record:
        raise ValueError("Profile already exists.")

    new_profile_id = uuid.uuid4().hex

    c.execute(
        "INSERT INTO profiles (profile_id, user_id, guild_id) VALUES (%s, %s, %s)",
        (new_profile_id, user_id, guild_id)
    )
    c.execute(
        "INSERT INTO details (profile_id) VALUES (%s)",
        (new_profile_id, )
    )
    c.execute(
        "INSERT INTO personality (profile_id) VALUES (%s)",
        (new_profile_id,)
    )
    c.execute(
        "INSERT INTO ataglance (profile_id) VALUES (%s)",
        (new_profile_id,)
    )
    c.execute(
        "INSERT INTO images (profile_id) VALUES (%s)",
        (new_profile_id,)
    )

    db_connection.commit()
    c.close()

    return new_profile_id

################################################################################
def new_additional_image(profile_id: str, url: str, caption: Optional[str]) -> str:

    image_id = uuid.uuid4().hex

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO addl_images (profile_id, image_id, url, caption) "
        "VALUES (%s, %s, %s, %s)",
        (profile_id, image_id, url, caption)
    )

    db_connection.commit()
    c.close()

    return image_id

################################################################################
