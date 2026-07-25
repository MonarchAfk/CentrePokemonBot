import discord
from discord.ext import commands
from discord import app_commands
import json
import config


DATABASE = "database.json"


def load_database():

    with open(DATABASE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_database(data):

    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )



def setup_moderation(bot):


    @bot.tree.command(
        name="kick",
        description="Expulser un membre"
    )
    @app_commands.checks.has_permissions(
        kick_members=True
    )
    async def kick(
        interaction: discord.Interaction,
        membre: discord.Member,
        raison: str = "Aucune raison"
    ):

        await membre.kick(reason=raison)


        embed = discord.Embed(
            title="👢 Membre expulsé",
            description=f"""
👤 Membre :
{membre.mention}

🛡️ Modérateur :
{interaction.user.mention}

📝 Raison :
{raison}
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="ban",
        description="Bannir un membre"
    )
    @app_commands.checks.has_permissions(
        ban_members=True
    )
    async def ban(
        interaction: discord.Interaction,
        membre: discord.Member,
        raison: str = "Aucune raison"
    ):


        await membre.ban(reason=raison)


        embed = discord.Embed(
            title="🔨 Membre banni",
            description=f"""
👤 Membre :
{membre.mention}

🛡️ Modérateur :
{interaction.user.mention}

📝 Raison :
{raison}
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="clear",
        description="Supprimer des messages"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clear(
        interaction: discord.Interaction,
        nombre:int
    ):

        await interaction.response.defer(
            ephemeral=True
        )


        deleted = await interaction.channel.purge(
            limit=nombre
        )


        await interaction.followup.send(
            f"🧹 {len(deleted)} messages supprimés.",
            ephemeral=True
        )



    @bot.tree.command(
        name="warn",
        description="Donner un avertissement"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def warn(
        interaction: discord.Interaction,
        membre: discord.Member,
        raison:str
    ):


        data = load_database()


        if "warnings" not in data:
            data["warnings"] = {}


        user_id = str(membre.id)


        if user_id not in data["warnings"]:
            data["warnings"][user_id] = []


        data["warnings"][user_id].append(
            {
                "moderateur": interaction.user.name,
                "raison": raison
            }
        )


        save_database(data)


        embed = discord.Embed(
            title="⚠️ Avertissement",
            description=f"""
👤 Membre :
{membre.mention}

🛡️ Modérateur :
{interaction.user.mention}

📝 Raison :
{raison}
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="warnings",
        description="Voir les avertissements d'un membre"
    )
    async def warnings(
        interaction: discord.Interaction,
        membre: discord.Member
    ):


        data = load_database()


        warns = data.get(
            "warnings",
            {}
        ).get(
            str(membre.id),
            []
        )


        if not warns:

            await interaction.response.send_message(
                "✅ Aucun avertissement."
            )

            return



        embed = discord.Embed(
            title=f"⚠️ Avertissements de {membre.name}",
            color=config.COLOR
        )


        for i, warn in enumerate(warns, start=1):

            embed.add_field(
                name=f"Avertissement #{i}",
                value=f"""
👮 Modérateur :
{warn['moderateur']}

📝 Raison :
{warn['raison']}
""",
                inline=False
            )


        await interaction.response.send_message(
            embed=embed
        )
