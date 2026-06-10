import discord
from discord.ext import commands

from config import BOT_TOKEN

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)

    print(f"Logged in as {bot.user}")

@bot.tree.command(
    name="setup",
    description="Create the verification button"
)
async def setup(interaction: discord.Interaction):

    view = discord.ui.View()

    view.add_item(
        discord.ui.Button(
            label="Verify",
            url="http://localhost:5000/verify"
        )
    )

    await interaction.response.send_message(
        "Click below to verify.",
        view=view
    )

bot.run(BOT_TOKEN)