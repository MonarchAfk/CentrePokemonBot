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



def setup_boutique(bot):


    @bot.tree.command(
        name="boutique",
        description="Voir les cartes Pokémon disponibles"
    )
    async def boutique(
        interaction: discord.Interaction
    ):

        data = load_database()

        shop = data.get(
            "shop",
            []
        )


        if len(shop) == 0:

            await interaction.response.send_message(
                "🛒 La boutique est actuellement vide."
            )

            return


        embed = discord.Embed(
            title="🛒 Boutique Pokémon",
            description="Les cartes disponibles au Centre Pokémon",
            color=config.COLOR
        )


        for card in shop[:10]:

            embed.add_field(

                name=f"🃏 {card['nom']}",

                value=
                f"""
💎 Prix : {card['prix']}€
⭐ Rareté : {card['rarete']}
📦 Stock : {card['stock']}
🆔 ID : {card['id']}
""",

                inline=False
            )


        embed.set_footer(
            text="🏯〡Centre Pokémon"
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="ajoutercarte",
        description="Ajouter une carte dans la boutique"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def ajoutercarte(

        interaction: discord.Interaction,

        nom:str,

        prix:int,

        rarete:str,

        extension:str,

        stock:int,

        image:str = None

    ):


        data = load_database()


        if "shop" not in data:

            data["shop"] = []


        new_id = len(data["shop"]) + 1



        carte = {

            "id": new_id,

            "nom": nom,

            "prix": prix,

            "rarete": rarete,

            "extension": extension,

            "stock": stock,

            "image": image

        }



        data["shop"].append(carte)


        save_database(data)



        embed = discord.Embed(

            title="✅ Carte ajoutée",

            description=
            f"""
🃏 {nom}

💎 Prix : {prix}€
⭐ Rareté : {rarete}
📦 Stock : {stock}
""",

            color=config.COLOR

        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="acheter",
        description="Acheter une carte Pokémon"
    )
    async def acheter(

        interaction: discord.Interaction,

        id:int

    ):


        data = load_database()


        shop = data.get(
            "shop",
            []
        )


        carte = None


        for c in shop:

            if c["id"] == id:

                carte = c
                break



        if carte is None:

            await interaction.response.send_message(
                "❌ Carte introuvable."
            )

            return



        if carte["stock"] <= 0:

            await interaction.response.send_message(
                "❌ Cette carte est en rupture de stock."
            )

            return



        carte["stock"] -= 1



        if "collections" not in data:

            data["collections"] = {}



        user_id = str(
            interaction.user.id
        )


        if user_id not in data["collections"]:

            data["collections"][user_id] = []



        data["collections"][user_id].append(
            carte["nom"]
        )


        save_database(data)



        embed = discord.Embed(

            title="🎉 Achat confirmé",

            description=
            f"""
🃏 Carte :
{carte['nom']}

💎 Prix :
{carte['prix']}€

👤 Acheteur :
{interaction.user.mention}

📦 Stock restant :
{carte['stock']}
""",

            color=config.COLOR

        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="supprimercarte",
        description="Supprimer une carte de la boutique"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def supprimercarte(

        interaction: discord.Interaction,

        id:int

    ):


        data = load_database()


        shop = data.get(
            "shop",
            []
        )


        for carte in shop:

            if carte["id"] == id:

                shop.remove(carte)

                save_database(data)


                await interaction.response.send_message(
                    "✅ Carte supprimée."
                )

                return



        await interaction.response.send_message(
            "❌ Carte introuvable."
        )
