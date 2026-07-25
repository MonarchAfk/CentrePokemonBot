import discord
from discord.ext import commands
from discord import app_commands
import requests
import config


def setup_pokemon(bot):

    API_URL = "https://api.pokemontcg.io/v2/cards"


    def search_card(name):

        params = {
            "q": f"name:{name}"
        }

        response = requests.get(
            API_URL,
            params=params
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if len(data["data"]) == 0:
            return None

        return data["data"][0]


    @bot.tree.command(
        name="carte",
        description="Rechercher une carte Pokémon"
    )
    @app_commands.describe(
        nom="Nom de la carte Pokémon"
    )
    async def carte(
        interaction: discord.Interaction,
        nom:str
    ):

        await interaction.response.defer()


        card = search_card(nom)


        if not card:

            await interaction.followup.send(
                "❌ Carte introuvable."
            )
            return


        embed = discord.Embed(
            title=f"🃏 {card['name']}",
            color=config.COLOR
        )


        embed.add_field(
            name="📦 Extension",
            value=card["set"]["name"],
            inline=False
        )


        embed.add_field(
            name="🎴 Numéro",
            value=f"{card['number']}/{card['set']['printedTotal']}",
            inline=True
        )


        embed.add_field(
            name="⭐ Rareté",
            value=card.get(
                "rarity",
                "Inconnue"
            ),
            inline=True
        )


        embed.add_field(
            name="❤️ PV",
            value=card.get(
                "hp",
                "?"
            ),
            inline=True
        )


        if "types" in card:

            embed.add_field(
                name="🔥 Type",
                value=", ".join(card["types"]),
                inline=True
            )


        attaques = []

        for attack in card.get("attacks", []):

            attaques.append(
                f"⚔️ {attack['name']} - {attack['damage']}"
            )


        if attaques:

            embed.add_field(
                name="Attaques",
                value="\n".join(attaques),
                inline=False
            )


        embed.set_image(
            url=card["images"]["large"]
        )


        embed.set_footer(
            text="🏯〡Centre Pokémon"
        )


        await interaction.followup.send(
            embed=embed
        )



    @bot.tree.command(
        name="prix",
        description="Voir le prix d'une carte"
    )
    async def prix(
        interaction: discord.Interaction,
        nom:str
    ):

        await interaction.response.defer()


        card = search_card(nom)


        if not card:

            await interaction.followup.send(
                "❌ Carte introuvable."
            )
            return


        prices = card.get(
            "tcgplayer",
            {}
        )


        embed = discord.Embed(
            title=f"💎 Prix {card['name']}",
            color=config.COLOR
        )


        if prices:

            embed.description = (
                "Prix disponibles selon les marchés."
            )

        else:

            embed.description = (
                "Aucun prix disponible actuellement."
            )


        await interaction.followup.send(
            embed=embed
        )



    @bot.tree.command(
        name="compare",
        description="Comparer deux cartes Pokémon"
    )
    async def compare(
        interaction: discord.Interaction,
        carte1:str,
        carte2:str
    ):

        await interaction.response.defer()


        c1 = search_card(carte1)
        c2 = search_card(carte2)


        if not c1 or not c2:

            await interaction.followup.send(
                "❌ Une des cartes est introuvable."
            )
            return


        embed = discord.Embed(
            title="⚔️ Comparaison Pokémon",
            color=config.COLOR
        )


        embed.add_field(
            name=f"🃏 {c1['name']}",
            value=
            f"⭐ {c1.get('rarity','?')}\n"
            f"❤️ {c1.get('hp','?')} PV",
            inline=True
        )


        embed.add_field(
            name=f"🃏 {c2['name']}",
            value=
            f"⭐ {c2.get('rarity','?')}\n"
            f"❤️ {c2.get('hp','?')} PV",
            inline=True
        )


        embed.set_footer(
            text="🏯〡Centre Pokémon"
        )


        await interaction.followup.send(
            embed=embed
        )
