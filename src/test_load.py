import os
import sys
import asyncio
import logging

# Thêm thư mục src vào Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)d [%(levelname)-s] %(message)s"
)
logger = logging.getLogger(__name__)

async def test_load_cogs():
    """Test load các cogs để xem có lỗi gì không"""
    print("🔍 Testing cog loading...")
    
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    print(f"📁 Cogs directory: {cogs_dir}")
    
    if not os.path.exists(cogs_dir):
        print(f"❌ Cogs directory không tồn tại: {cogs_dir}")
        return
    
    files = os.listdir(cogs_dir)
    print(f"📂 Files in cogs: {files}")
    
    for filename in files:
        if filename.endswith('.py') and filename != '__init__.py':
            cog_name = f'cogs.{filename[:-3]}'
            print(f"\n� Testing import: {cog_name}")
            
            try:
                # Test import
                import importlib
                module = importlib.import_module(cog_name)
                print(f"✅ Successfully imported {cog_name}")
                
                # Check if setup function exists
                if hasattr(module, 'setup'):
                    print(f"✅ Found setup function in {cog_name}")
                    setup_func = getattr(module, 'setup')
                    print(f"📋 Setup function type: {type(setup_func)}")
                else:
                    print(f"❌ No setup function in {cog_name}")
                    
            except Exception as e:
                print(f"❌ Failed to import {cog_name}: {e}")
                import traceback
                traceback.print_exc()

async def test_imports():
    """Test các imports cần thiết"""
    print("\n🔍 Testing critical imports...")
    
    try:
        import nextcord
        print(f"✅ nextcord version: {nextcord.__version__}")
    except Exception as e:
        print(f"❌ nextcord import failed: {e}")
    
    try:
        from bll.feed_bll import FeedBLL
        print("✅ FeedBLL import successful")
    except Exception as e:
        print(f"❌ FeedBLL import failed: {e}")
    
    try:
        from utils.handle_rss import get_rss_link
        print("✅ handle_rss import successful")
    except Exception as e:
        print(f"❌ handle_rss import failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting cog loading test...")
    asyncio.run(test_imports())
    asyncio.run(test_load_cogs())
    print("\n✨ Test completed!")