import os
import logging
import tracemalloc
import asyncio
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()
tracemalloc.start()

# Set up intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

# Set up logging
logging.basicConfig(
    level=logging.NOTSET,
    format="%(filename)s:%(lineno)d [%(levelname)-s] %(message)s")
logger = logging.getLogger(__name__)

# Set up bot instance
bot = commands.Bot(command_prefix='_', intents=intents)


@bot.event
async def on_ready():
    logger.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"🔗 Connected to {len(bot.guilds)} guild(s).")


# --- Web server để GitHub Actions ping ---
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is alive!"


def run_flask():
    # Ẩn log Flask nếu không muốn spam
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=8080)


# --- Load cogs ---
async def load_cogs():
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)  # ✅ Dùng await
                logger.info(f'Successfully loaded extension {cog_name}')
            except Exception as e:
                logger.error(f'Failed to load extension {cog_name}: {e}')


# --- Main ---
async def main():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found in .env file.")
        return

    # load cogs trước khi start bot
    await load_cogs()

    # chạy bot (Nextcord chưa hỗ trợ async with)
    await bot.start(TOKEN)


if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run bot
    asyncio.run(main())
