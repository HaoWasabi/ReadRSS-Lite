import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ui, DMChannel
from bll.feed_bll import FeedBLL
from gui.embed_custom import EmbedCustom
from utils.commands_cog import CommandsCog
from utils.handle_rss import analyze_rss_link  # ✅ dùng phân tích RSS

logger = logging.getLogger("CommandShowChannel")

class CommandShowChannel(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.bot.add_view(self.AnalyzeView([], None))

    class AnalyzeModal(ui.Modal):
        def __init__(self, feeds, user):
            super().__init__("Phân tích feed")
            self.feeds = feeds
            self.user = user

            self.feed_index = ui.TextInput(
                label="Nhập vị trí feed (số thứ tự)",
                placeholder="Ví dụ: 1",
                required=True
            )
            self.add_item(self.feed_index)

        async def callback(self, interaction: Interaction):
            try:
                await interaction.response.defer(ephemeral=True)  # ✅ defer để mở session

                idx = int(self.feed_index.value.strip()) - 1
                if idx < 0 or idx >= len(self.feeds):
                    await interaction.followup.send("❌ Vị trí không hợp lệ.", ephemeral=True)
                    return

                feed_dto = self.feeds[idx]
                result = analyze_rss_link(rss_link=feed_dto.get_link_atom_feed())

                if len(result) > 1900:
                    preview = result[:1900] + "..."
                    await interaction.followup.send(
                        f"✅ Kết quả phân tích feed **{feed_dto.get_title_feed()}** (tóm tắt):\n{preview}",
                        ephemeral=False
                    )

                else:
                    await interaction.followup.send(
                        f"✅ Kết quả phân tích feed **{feed_dto.get_title_feed()}**:\n\n{result}",
                        ephemeral=True
                    )

            except Exception as e:
                logger.error(f"Error in AnalyzeModal: {e}")
                await interaction.followup.send(f"⚠️ Lỗi khi phân tích: {e}", ephemeral=True)

    class AnalyzeView(ui.View):
        def __init__(self, feeds, user):
            super().__init__(timeout=None)
            self.feeds = feeds
            self.user = user

        @ui.button(label="Phân tích", style=nextcord.ButtonStyle.primary, custom_id="analyze_button")
        async def analyze_button(self, button: ui.Button, interaction: Interaction):
            if not self.user or interaction.user.id != self.user.id:
                await interaction.response.send_message("Bạn không có quyền dùng nút này.", ephemeral=True)
                return
            await interaction.response.send_modal(CommandShowChannel.AnalyzeModal(self.feeds, self.user))

    @commands.command(name="show")
    async def command_show(self, ctx):
        await self._show_channel(ctx=ctx, guild=ctx.guild, user=ctx.author)
        
    @nextcord.slash_command(name="show", description="Show the feed notification channel")
    async def slash_command_show(self, interaction: Interaction):
        await interaction.response.defer()
        await self._show_channel(ctx=interaction.followup, guild=interaction.guild, user=interaction.user)

    async def _show_channel(self, ctx, guild=None, user=None):
        try:
            if not guild:
                await ctx.send("This command is only available in servers.")
                return
            else:
                guild_id = str(guild.id)
                guild_name = guild.name

            feed_bll = FeedBLL()
            feeds = []
            server_data = {}
            num_feeds = 0

            for feed_dto in feed_bll.get_all_feed():
                channel_id = int(feed_dto.get_channel_id())
                if not guild:
                    if str(user.id) == str(channel_id):  # DM case
                        channel_info = f"{num_feeds+1}. **DM Channel** - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        server_data.setdefault("Direct Message", []).append(channel_info)
                        feeds.append(feed_dto)
                        num_feeds += 1
                else:
                    channel = self.bot.get_channel(channel_id)
                    if channel is not None and channel.guild.id == int(guild_id):
                        server_name = f"**Server:** {guild_name} ({guild_id})"
                        channel_info = f"{num_feeds+1}. **Channel:** {channel.mention} - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        server_data.setdefault(server_name, []).append(channel_info)
                        feeds.append(feed_dto)
                        num_feeds += 1

            embed = EmbedCustom(
                id_server=guild_id,
                title="List of Feeds in Channels",
                description=f"You have {num_feeds} feeds in channels:"
            )

            for server_name, channels in server_data.items():
                embed.add_field(name=server_name, value="\n".join(channels), inline=False)

            view = self.AnalyzeView(feeds, user)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            logger.error(f"Error: {e}")

async def setup(bot):
    try:
        await bot.add_cog(CommandShowChannel(bot))
    except TypeError:
        # Fallback for older nextcord versions
        bot.add_cog(CommandShowChannel(bot))
