import discord
from discord.ext import commands
from discord import app_commands
import config


def setup_commands(bot):

    @bot.tree.command(
        name="ping",
        description="Affiche la latence du bot"
    )
    async def ping(interaction: discord.Interaction):

        embed = discord.Embed(
            title="🏓 Pong !",
            description=f"Latence : `{round(bot.latency * 1000)}ms`",
            color=config.COLOR
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="info",
        description="Présentation du serveur Centre Pokémon"
    )
    async def info(interaction: discord.Interaction):

        embed = discord.Embed(
            title="🏯〡Centre Pokémon",
            description="""
Bienvenue dans **🏯〡Centre Pokémon** !

🌸 Un serveur dédié aux passionnés de cartes Pokémon.

✨ Sur notre centre :

🃏 Achat & vente de cartes Pokémon
📦 Suivi des nouvelles ETB
💎 Estimation de cartes
🎴 Collections personnelles
🤝 Échanges entre membres

Rejoins une communauté de collectionneurs et fais évoluer ta collection !
            """,
            color=config.COLOR
        )

        embed.set_footer(
            text="🏯 Centre Pokémon • Attrapez-les tous !"
        )

        embed.set_thumbnail(
            url="https://i.imgur.com/example.png"
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="help",
        description="Liste toutes les commandes"
    )
    async def help_command(interaction: discord.Interaction):

        embed = discord.Embed(
            title="📖 Commandes Centre Pokémon",
            color=config.COLOR
        )

        embed.add_field(
            name="🏯 Serveur",
            value="""
`/info`
`/ping`
`/userinfo`
`/serverinfo`
`/avatar`
            """,
            inline=False
        )

        embed.add_field(
            name="🃏 Pokémon TCG",
            value="""
`/carte`
`/boutique`
`/vendre`
`/collection`
            """,
            inline=False
        )

        embed.add_field(
            name="🎫 Support",
            value="""
`/ticket`
`suggestion`
            """,
            inline=False
        )

        embed.set_footer(
            text="🏯〡Centre Pokémon"
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="avatar",
        description="Affiche l'avatar d'un membre"
    )
    @app_commands.describe(
        membre="Le membre choisi"
    )
    async def avatar(
        interaction: discord.Interaction,
        membre: discord.Member = None
    ):

        membre = membre or interaction.user

        embed = discord.Embed(
            title=f"🖼️ Avatar de {membre.name}",
            color=config.COLOR
        )

        embed.set_image(
            url=membre.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="userinfo",
        description="Informations d'un membre"
    )
    async def userinfo(
        interaction: discord.Interaction,
        membre: discord.Member = None
    ):

        membre = membre or interaction.user

        embed = discord.Embed(
            title=f"👤 Profil de {membre.name}",
            color=config.COLOR
        )

        embed.add_field(
            name="📅 Arrivé",
            value=membre.joined_at.strftime("%d/%m/%Y"),
            inline=False
        )

        embed.add_field(
            name="🆔 ID",
            value=membre.id,
            inline=False
        )

        embed.set_thumbnail(
            url=membre.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="serverinfo",
        description="Informations du serveur"
    )
    async def serverinfo(interaction: discord.Interaction):

        guild = interaction.guild

        embed = discord.Embed(
            title="🏯 Informations serveur",
            color=config.COLOR
        )

        embed.add_field(
            name="Nom",
            value=guild.name
        )

        embed.add_field(
            name="Membres",
            value=guild.member_count
        )

        embed.add_field(
            name="Création",
            value=guild.created_at.strftime("%d/%m/%Y")
        )

        await interaction.response.send_message(embed=embed)


    @bot.tree.command(
        name="suggestion",
        description="Faire une suggestion"
    )
    @app_commands.describe(
        idée="Votre suggestion"
    )
    async def suggestion(
        interaction: discord.Interaction,
        idée: str
    ):

        embed = discord.Embed(
            title="💡 Nouvelle suggestion",
            description=idéе,
            color=config.COLOR
        )

        embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(
            "✅ Suggestion envoyée !",
            ephemeral=True
        )

        await interaction.channel.send(embed=embed)
