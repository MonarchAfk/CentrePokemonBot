import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import config
import datetime


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



# Exemple de nouvelles Pokémon
NEWS = [
    {
        "titre": "Nouvelle ETB Pokémon annoncée !",
        "description": "Une nouvelle Elite Trainer Box arrive prochainement.",
        "image": "https://images.pokemontcg.io/placeholder.png"
    },

    {
        "titre": "Nouvelle extension Pokémon TCG",
        "description": "Une nouvelle extension Pokémon arrive avec de nouvelles cartes.",
        "image": "https://images.pokemontcg.io/placeholder.png"
    }
]



def setup_news(bot):


    @bot.tree.command(
        name="testnews",
        description="Tester une annonce Pokémon"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def testnews(
        interaction: discord.Interaction
    ):


        channel = bot.get_channel(
            config.NEWS_CHANNEL_ID
        )


        if channel is None:

            await interaction.response.send_message(
                "❌ Salon news introuvable.",
                ephemeral=True
            )

            return



        news = NEWS[0]


        embed = discord.Embed(

            title=f"📰 {news['titre']}",

            description=f"""
{news['description']}

🏯〡Centre Pokémon
""",

            color=config.COLOR,

            timestamp=datetime.datetime.now()

        )


        embed.set_image(
            url=news["image"]
        )


        embed.set_footer(
            text="Actualités Pokémon TCG"
        )


        await channel.send(
            embed=embed
        )


        await interaction.response.send_message(
            "✅ News envoyée.",
            ephemeral=True
        )



    @tasks.loop(
        hours=12
    )
    async def pokemon_news():


        channel = bot.get_channel(
            config.NEWS_CHANNEL_ID
        )


        if channel is None:
            return



        data = load_database()


        if "news_sent" not in data:

            data["news_sent"] = []



        news = NEWS[0]



        if news["titre"] in data["news_sent"]:

            return



        embed = discord.Embed(

            title=f"📰 {news['titre']}",

            description=f"""
{news['description']}

✨ Préparez vos collections !

🏯〡Centre Pokémon
""",

            color=config.COLOR

        )


        embed.set_image(
            url=news["image"]
        )


        await channel.send(
            embed=embed
        )


        data["news_sent"].append(
            news["titre"]
        )


        save_database(data)



    @pokemon_news.before_loop
    async def before_news():

        await bot.wait_until_ready()



    pokemon_news.start()
