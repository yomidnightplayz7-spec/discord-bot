# main.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN not found in .env")
    exit()

# ------------------------------
# Settings
# ------------------------------
OWNER_IDS = [1135229548426965103, 1133479182081478748]  # Allowed owners
LOG_CHANNEL_ID = 1375432176165982270  # ✅ Updated log channel ID
VOUCH_CHANNEL_ID = 1364195817002369046  # Channel where user should vouch
LOGO_PATH = "logo.png"  # Logo file path

# ------------------------------
# Intents & bot setup
# ------------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)


# ------------------------------
# Bot ready event
# ------------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user} (ID: {bot.user.id})")


# ------------------------------
# Paid command
# ------------------------------
@bot.command(name="paid")
async def paid(ctx, member: discord.Member, amount: str, reward: str):
    # Permission check
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You are not allowed to use this command.")

    # Check for attachment
    if len(ctx.message.attachments) == 0:
        return await ctx.send("❌ You must attach proof of payment.")

    proof_attachment = ctx.message.attachments[0].url

    # Current date & time
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    transaction_id = now.strftime("%Y%m%d%H%M%S")  # Unique ID

    # ------------------------------
    # Professional & Aesthetic Embed for log channel
    # ------------------------------
    log_embed = discord.Embed(
        title=f"💰 Payment Completed",
        description=f"────────────\n**Transaction ID:** #{transaction_id}\n**Reward Type:** {reward}\n────────────",
        color=discord.Color.green()
    )

    # Inline fields for wider look
    log_embed.add_field(name="👤 Recipient", value=member.mention, inline=True)
    log_embed.add_field(name="💳 Paid By", value=ctx.author.mention, inline=True)
    log_embed.add_field(name="💵 Amount", value=f"{amount}", inline=True)
    log_embed.add_field(name="✅ Status", value="Completed", inline=True)
    log_embed.add_field(name="\u200b", value="\u200b", inline=True)  # spacing
    log_embed.add_field(name="🏷 Server", value=ctx.guild.name if ctx.guild else "DM", inline=True)

    # Large fields
    log_embed.add_field(name="📄 Proof", value=f"[Click Here]({proof_attachment})", inline=False)
    log_embed.add_field(name="⏰ Date & Time", value=timestamp_str, inline=False)

    log_embed.set_thumbnail(url="attachment://logo.png")
    log_embed.set_footer(
        text=f"Payment Log • Paid by {ctx.author}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    log_embed.set_image(url=proof_attachment)

    # Send embed to log channel
    try:
        log_channel = await bot.fetch_channel(LOG_CHANNEL_ID)
        await log_channel.send(file=discord.File(LOGO_PATH, filename="logo.png"), embed=log_embed)
    except Exception as e:
        await ctx.send(f"⚠️ Could not send log embed: {e}")

    # ------------------------------
    # DM the user with aesthetic embed
    # ------------------------------
    try:
        dm_embed = discord.Embed(
            title=f"💰 You Received a Payout!",
            description=f"────────────\n**Transaction ID:** #{transaction_id}\n**Reward Type:** {reward}\n────────────",
            color=discord.Color.green()
        )
        dm_embed.add_field(name="👤 Recipient", value=member.mention, inline=True)
        dm_embed.add_field(name="💳 Paid By", value=ctx.author.mention, inline=True)
        dm_embed.add_field(name="💵 Amount", value=f"{amount}", inline=True)
        dm_embed.add_field(name="⏰ Date & Time", value=timestamp_str, inline=False)
        dm_embed.add_field(
            name="📌 Vouch",
            value=f"Please vouch **{ctx.author}** in <#{VOUCH_CHANNEL_ID}>",
            inline=False
        )
        dm_embed.set_thumbnail(url="attachment://logo.png")
        dm_embed.set_footer(text=f"Transaction ID: #{transaction_id}")
        dm_embed.set_image(url=proof_attachment)

        await member.send(file=discord.File(LOGO_PATH, filename="logo.png"), embed=dm_embed)
        await ctx.send(f"✅ Payment logged and {member.mention} has been notified via DM.")
    except discord.Forbidden:
        await ctx.send(f"⚠️ Could not DM {member.mention}, but payment was logged.")


# ------------------------------
# Run the bot
# ------------------------------
print("Starting bot...")
bot.run(TOKEN)
