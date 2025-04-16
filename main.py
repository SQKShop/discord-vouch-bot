import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed, Attachment
from datetime import datetime
import os

intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents)

REVIEW_CHANNEL_ID = 1361421979147829328
VOUCH_FILE = "vouch_count.txt"

def get_next_vouch_number():
    if not os.path.exists(VOUCH_FILE):
        with open(VOUCH_FILE, "w") as f:
            f.write("1")
        return 1
    with open(VOUCH_FILE, "r+") as f:
        count = int(f.read().strip())
        f.seek(0)
        f.write(str(count + 1))
        f.truncate()
        return count + 1

@bot.slash_command(name="vouch", description="Submit a review/vouch with stars and optional image proof")
async def vouch(
    interaction: Interaction,
    message: str = SlashOption(name="message", description="Your review", required=True),
    stars: int = SlashOption(name="stars", description="Rating 1–5", required=True),
    proof: Attachment = SlashOption(name="proof", description="Image proof (optional)", required=False)
):
    if stars < 1 or stars > 5:
        await interaction.response.send_message("❌ Rating must be between 1 and 5", ephemeral=True)
        return

    if proof and not proof.content_type.startswith("image/"):
        await interaction.response.send_message("❌ Only image files are allowed for proof.", ephemeral=True)
        return

    vouch_number = get_next_vouch_number()
    stars_display = "⭐" * stars
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    embed = Embed(
        title="**New vouch created!**",
        description=f"{stars_display}\n\n**Vouch:**\n{message}",
        color=0x00ff99,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Vouch Nº", value=f"`{vouch_number}`", inline=True)
    embed.add_field(name="Vouched by", value=interaction.user.mention, inline=True)
    embed.add_field(name="Vouched at", value=f"`{date_now}`", inline=True)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Service provided by SQK.Shop")

    if proof:
        embed.set_image(url=proof.url)

    channel = bot.get_channel(REVIEW_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Vouch submitted!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.sync_application_commands()
    print(f"✅ Bot online as {bot.user}")
    
bot.run("MTM2MTgyNTQwOTEzMzQ0NTEzNA.GxAxX2.RLQjjmB7t9lrogSXcspfteKJlMXr-_sfS-LTM8")
