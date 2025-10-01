import logging
import asyncio
from nextcord.ext import commands, tasks
from dto.channel_dto import ChannelDTO
from dto.server_dto import ServerDTO
from bll.channel_bll import ChannelBLL
from bll.server_bll import ServerBLL
from bll.feed_bll import FeedBLL
from bll.emty_bll import EmtyBLL
from gui.embed_feed import EmbedFeed
from utils.commands_cog import CommandsCog
from utils.handle_rss import read_rss_link

logger = logging.getLogger("Events")

class Events(CommandsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    # ---------------- Guilds ---------------- #
    async def load_guilds(self):
        """Cập nhật server & channel trong DB dựa vào guilds hiện có."""
        try:
            guilds = self.bot.guilds
            channel_bll = ChannelBLL()
            server_bll = ServerBLL()
            list_channel = channel_bll.get_all_channel()
            list_server = server_bll.get_all_server()

            for guild in guilds:
                server_dto = ServerDTO(str(guild.id), str(guild.name))

                # Insert or update server
                matching_server = next((s for s in list_server if s.get_server_id() == server_dto.get_server_id()), None)
                if not matching_server:
                    server_bll.insert_server(server_dto)
                elif matching_server.get_server_name() != server_dto.get_server_name():
                    server_bll.update_server(server_dto)

                # Handle each channel
                for channel in guild.channels:
                    channel_dto = ChannelDTO(str(channel.id), channel.name, str(guild.id))
                    matching_channel = next((ch for ch in list_channel if ch.get_channel_id() == channel_dto.get_channel_id()), None)

                    if matching_channel and matching_channel.get_channel_name() != channel_dto.get_channel_name():
                        channel_bll.update_channel(channel_dto)

        except Exception as e:
            logger.exception(f"Error loading guilds: {e}")

    # ---------------- Feed Helpers ---------------- #
    async def _process_feed_and_send(self, feed, emty_bll: EmtyBLL, target, id_server: str):
        """Đọc RSS feed và gửi embed đến target (channel hoặc user)."""
        try:
            feed_data = read_rss_link(rss_link=feed.get_link_atom_feed())
            if not feed_data or not all(feed_data):
                logger.warning(f"Incomplete feed data for {feed.get_link_atom_feed()}")
                return

            feed_dto, emty_dto = feed_data
            emty_dto.set_channel_id(str(target.id))

            if emty_bll.insert_emty(emty_dto):  # Chỉ gửi khi insert thành công
                embed = EmbedFeed(
                    id_server=id_server,
                    feed_dto=feed_dto,
                    emty_dto=emty_dto,
                )
                await target.send(embed=embed)

                logger.info(f"✅ Sent feed to {getattr(target, 'name', 'DM')} ({target.id})")
                logger.debug(f"Inserted emty: {emty_dto.__dict__}")

        except Exception as e:
            logger.exception(f"Error processing feed {feed.get_link_atom_feed()}: {e}")

    async def load_dm_feed(self, list_feed, user_id: int):
        """Load và gửi feed đến user qua DM."""
        emty_bll = EmtyBLL()
        try:
            user = await self.bot.fetch_user(user_id)
            for feed in list_feed:
                await self._process_feed_and_send(feed, emty_bll, user, id_server=str(user.id))
        except Exception as e:
            logger.exception(f"Error fetching user for DM {user_id}: {e}")

    async def load_server_feed(self, list_feed, channel):
        """Load và gửi feed đến channel trong server."""
        emty_bll = EmtyBLL()
        try:
            for feed in list_feed:
                await self._process_feed_and_send(feed, emty_bll, channel, id_server=str(channel.guild.id))
        except Exception as e:
            logger.exception(f"Error processing server channel {channel.id}: {e}")

    async def load_list_feed(self):
        """Lấy danh sách feed từ DB và gửi đến các channel/DM tương ứng."""
        try:
            channel_bll = ChannelBLL()
            feed_bll = FeedBLL()
            list_channel = channel_bll.get_all_channel()

            for channel in list_channel:
                channel_id = channel.get_channel_id()
                target_channel = self.bot.get_channel(int(channel_id))
                list_feed = feed_bll.get_all_feed_by_channel_id(channel_id)

                if not list_feed:
                    continue

                if target_channel:  # Server channel
                    await self.load_server_feed(list_feed, target_channel)
                else:  # DM channel
                    await self.load_dm_feed(list_feed, int(channel_id))

        except Exception as e:
            logger.exception(f"Error loading feed list: {e}")

    # ---------------- Background Task ---------------- #
    @tasks.loop(seconds=60)
    async def push_noti(self):
        logger.debug("⏳ Running background task push_noti")
        await self.load_guilds()
        await self.load_list_feed()

    @push_noti.before_loop
    async def before_push_noti(self):
        await self.bot.wait_until_ready()
        logger.info("push_noti loop is starting...")

    # ---------------- Events ---------------- #
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"🤖 Bot {self.bot.user} is ready")
        logger.info("Commands: %s", [c.name for c in self.bot.commands])
        logger.info("Slash Commands: %s", [c.name for c in self.bot.get_application_commands()])

        await self.bot.sync_all_application_commands()
        logger.info("✅ Slash commands synced.")

        if not self.push_noti.is_running():
            self.push_noti.start()

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
