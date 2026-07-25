import discord
from discord.ext import commands
from discord import app_commands
import config


TICKET_CATEGORY_ID = 1530677078566113471  # Mets ici l'ID de ta catégorie tickets


class TicketButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="🎫 Ouvrir un ticket",
        style=discord.ButtonStyle.primary,
        custom_id="open_ticket"
    )
    async def open_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        guild = interaction.guild


        existing = discord.utils.get(
            guild.channels,
            name=f"ticket-{interaction.user.name.lower()}"
        )


        if existing:

            await interaction.response.send_message(
                "❌ Tu as déjà un ticket ouvert.",
                ephemeral=True
            )

            return



        overwrites = {

            guild.default_role:
            discord.PermissionOverwrite(
                view_channel=False
            ),

            interaction.user:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            ),

            guild.me:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )

        }



        channel = await guild.create_text_channel(

            name=f"ticket-{interaction.user.name}",

            overwrites=overwrites

        )



        embed = discord.Embed(

            title="🎫 Ticket Centre Pokémon",

            description=f"""
Bienvenue {interaction.user.mention} !

Un membre du staff va venir t'aider.

🃏 Pour :
- Achat de cartes
- Vente
- Échange
- Questions

Merci de patienter.

🏯〡Centre Pokémon
""",

            color=config.COLOR

        )


        await channel.send(
            embed=embed,
            view=CloseTicketButton()
        )


        await interaction.response.send_message(
            f"✅ Ton ticket a été créé : {channel.mention}",
            ephemeral=True
        )




class CloseTicketButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)



    @discord.ui.button(

        label="🔒 Fermer le ticket",

        style=discord.ButtonStyle.danger,

        custom_id="close_ticket"

    )
    async def close_ticket(

        self,

        interaction: discord.Interaction,

        button: discord.ui.Button

    ):


        await interaction.response.send_message(
            "🔒 Fermeture du ticket...",
            ephemeral=True
        )


        await interaction.channel.delete()




def setup_tickets(bot):


    @bot.tree.command(

        name="ticket",

        description="Créer un panneau de tickets"

    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def ticket(

        interaction: discord.Interaction

    ):


        embed = discord.Embed(

            title="🎫 Support Pokémon",

            description="""

Besoin d'aide ?

Clique sur le bouton ci-dessous pour ouvrir un ticket.

🃏 Achat
💎 Vente
🤝 Échange
❓ Questions

🏯〡Centre Pokémon

""",

            color=config.COLOR

        )


        await interaction.response.send_message(

            embed=embed,

            view=TicketButton()

        )
