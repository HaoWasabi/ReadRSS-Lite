import logging
from nextcord.ext import commands
from utils.commands_cog import CommandsCog

logger = logging.getLogger("Events")


class Events(CommandsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot {self.bot.user} is ready")
        logger.info("Current commands: %s", str([command.name for command in self.bot.commands]))
        logger.info("Current slash commands: %s", str([command.name for command in self.bot.get_application_commands()]))

        await self.bot.sync_all_application_commands()
        logger.info(f'Bot {self.bot.user} is ready and commands are synced.')

        if not self.push_noti.is_running():
            self.push_noti.start()

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))