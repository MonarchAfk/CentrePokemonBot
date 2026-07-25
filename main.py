import discord
from discord.ext import commands
import config

from commands import setup_commands
from moderation import setup_moderation
from pokemon import setup_pokemon
from economy import setup_economy
from tickets import setup_tickets
from news import setup_news


intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=intents
)


@bot.event
async def on_ready():

    print(
        f"""
╔══════════════════════╗
🏯 Centre Pokémon Bot
✅ Connecté
👤 {bot.user}
╚══════════════════════╝
"""
    )

    await bot.tree.sync()

from economy import setup_economy
setup_economy(bot)

from boutique import setup_boutique
setup_boutique(bot)

from moderation import setup_moderation
setup_moderation(bot)

from tickets import setup_tickets
setup_tickets(bot)                            

setup_commands(bot)
setup_moderation(bot)
setup_pokemon(bot)
setup_economy(bot)
setup_tickets(bot)
setup_news(bot)


bot.run(config.TOKEN)
