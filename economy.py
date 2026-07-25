import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import time
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



def create_user(data, user_id):

    user_id = str(user_id)

    if "users" not in data:
        data["users"] = {}

    if user_id not in data["users"]:

        data["users"][user_id] = {
            "coins": 0,
            "daily": 0
        }



def setup_economy(bot):


    @bot.tree.command(
        name="balance",
        description="Voir son nombre de PokéCoins"
    )
    async def balance(
        interaction: discord.Interaction
    ):

        data = load_database()

        create_user(
            data,
            interaction.user.id
        )

        coins = data["users"][str(interaction.user.id)]["coins"]


        embed = discord.Embed(
            title="💰 Portefeuille Pokémon",
            description=
            f"""
👤 Dresseur :
{interaction.user.mention}

🪙 PokéCoins :
**{coins} PC**
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="daily",
        description="Récupérer sa récompense quotidienne"
    )
    async def daily(
        interaction: discord.Interaction
    ):

        data = load_database()

        create_user(
            data,
            interaction.user.id
        )


        user = data["users"][str(interaction.user.id)]


        now = time.time()


        if now - user["daily"] < 86400:

            remaining = int(
                86400 - (now - user["daily"])
            )


            heures = remaining // 3600


            await interaction.response.send_message(
                f"⏳ Tu as déjà récupéré ton bonus ! Reviens dans {heures}h."
            )

            return



        reward = random.randint(
            100,
            300
        )


        user["coins"] += reward

        user["daily"] = now


        save_database(data)


        embed = discord.Embed(
            title="🎁 Récompense quotidienne",
            description=
            f"""
Félicitations {interaction.user.mention} !

Tu as reçu :

🪙 **{reward} PokéCoins**
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="work",
        description="Travailler pour gagner des PokéCoins"
    )
    async def work(
        interaction: discord.Interaction
    ):

        data = load_database()

        create_user(
            data,
            interaction.user.id
        )


        jobs = [
            "Soigneur au Centre Pokémon 🏥",
            "Chercheur Pokémon 🔬",
            "Vendeur de cartes 🃏",
            "Champion d'arène ⚔️",
            "Explorateur Pokémon 🗺️"
        ]


        job = random.choice(jobs)


        gain = random.randint(
            50,
            150
        )


        data["users"][str(interaction.user.id)]["coins"] += gain


        save_database(data)


        embed = discord.Embed(
            title="💼 Travail terminé",
            description=
            f"""
👤 Dresseur :
{interaction.user.mention}

💼 Métier :
{job}

🪙 Gain :
**{gain} PokéCoins**
""",
            color=config.COLOR
        )


        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="leaderboard",
        description="Classement des meilleurs dresseurs"
    )
    async def leaderboard(
        interaction: discord.Interaction
    ):

        data = load_database()


        users = data.get(
            "users",
            {}
        )


        classement = sorted(
            users.items(),
            key=lambda x: x[1].get("coins", 0),
            reverse=True
        )


        embed = discord.Embed(
            title="🏆 Classement des Dresseurs",
            color=config.COLOR
        )


        position = 1


        for user_id, info in classement[:10]:

            try:

                member = await bot.fetch_user(
                    int(user_id)
                )

                nom = member.name

            except:

                nom = "Utilisateur"


            embed.add_field(
                name=f"#{position} {nom}",
                value=f"🪙 {info.get('coins',0)} PC",
                inline=False
            )


            position += 1



        await interaction.response.send_message(
            embed=embed
        )
