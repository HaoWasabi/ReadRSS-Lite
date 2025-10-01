import os
import sys
import asyncio
import logging

# Thêm thư mục src vào Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d [%(levelname)-s] %(message)s"
)
logger = logging.getLogger(__name__)

async def test_cog_setup():
    """Test mô phỏng hoàn toàn như GitHub Actions"""
    print("🔍 Testing cog setup like GitHub Actions...")
    
    try:
        import nextcord
        from nextcord.ext import commands
        
        # Tạo bot instance giống như trong main.py
        intents = nextcord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='_', intents=intents)
        
        print(f"✅ Bot created with nextcord {nextcord.__version__}")
        
        # Test từng cog
        cogs_to_test = [
            'cogs.other_commands',
            'cogs.command_analyze_feed', 
            'cogs.command_set_feed',
            'cogs.command_show_feed',
            'cogs.command_test_feed',
            'cogs.command_delete_feed',
            'cogs.events'
        ]
        
        for cog_name in cogs_to_test:
            print(f"\n🔄 Testing load extension: {cog_name}")
            try:
                # Fix: bot.load_extension() returns None in nextcord 2.6.0
                result = bot.load_extension(cog_name)
                if result is not None:
                    await result  # Only await if it returns something
                print(f"✅ Successfully loaded: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load {cog_name}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n📋 Final commands: {[c.name for c in bot.commands]}")
        print(f"⚡ Final slash commands: {len(bot.get_application_commands())}")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 GitHub Actions simulation test...")
    asyncio.run(test_cog_setup())
    print("\n✨ Test completed!")