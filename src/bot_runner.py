#!/usr/bin/env python3
"""
Bot runner script for GitHub Actions hosting
Handles automatic restarts and better logging
"""

import os
import sys
import asyncio
import logging
import signal
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging for GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self):
        self.bot_process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        
    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        
    async def run_bot(self):
        """Import and run the main bot"""
        try:
            # Import main bot module
            from main import main as bot_main
            logger.info("Starting ReadRSS Lite bot...")
            await bot_main()
        except Exception as e:
            logger.error(f"Bot crashed with error: {e}")
            raise
            
    async def run_with_restart(self):
        """Run bot with automatic restart on failure"""
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        logger.info("Bot runner started")
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                await self.run_bot()
            except Exception as e:
                self.restart_count += 1
                logger.error(f"Bot failed (attempt {self.restart_count}/{self.max_restarts}): {e}")
                
                if self.restart_count < self.max_restarts and self.running:
                    wait_time = min(60 * self.restart_count, 300)  # Max 5 minutes
                    logger.info(f"Restarting in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Max restart attempts reached or shutdown requested")
                    break
                    
        logger.info("Bot runner stopped")

def main():
    """Main entry point"""
    # Verify environment variables
    required_vars = ['DISCORD_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        sys.exit(1)
        
    # Verify we're in the right directory
    if not os.path.exists('main.py'):
        logger.error("main.py not found. Make sure you're in the src directory.")
        sys.exit(1)
        
    runner = BotRunner()
    
    try:
        asyncio.run(runner.run_with_restart())
    except KeyboardInterrupt:
        logger.info("Bot runner interrupted by user")
    except Exception as e:
        logger.error(f"Bot runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()