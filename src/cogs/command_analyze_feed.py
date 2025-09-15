import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from utils.commands_cog import CommandsCog
from utils.handle_rss import get_rss_link, analyze_rss_link

logger = logging.getLogger("CommandAnalyzeRSS")

class CommandAnalyzeRSS(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="analyzerss")
    async def analyze_rss(self, ctx, link_rss: str = None, url: str = None):
        """Phân tích nhanh dữ liệu từ RSS link hoặc URL website."""
        if not link_rss and not url:
            await ctx.send("Vui lòng cung cấp RSS link hoặc URL website.")
            return

        if link_rss and url:
            await ctx.send("Chỉ được cung cấp **một** trong hai: RSS link hoặc URL.")
            return

        if not link_rss and url:
            link_rss = get_rss_link(url)
            if not link_rss:
                await ctx.send("Không tìm thấy RSS link từ URL đã cho.")
                return

        await self._handle_analyze(ctx, link_rss)

    @nextcord.slash_command(name="analyzerss", description="Phân tích RSS link/URL trực tiếp")
    async def slash_analyze_rss(self, interaction: Interaction,
                                link_rss: str = SlashOption(description="RSS feed link", required=False),
                                url: str = SlashOption(description="Website URL", required=False)):
        await interaction.response.defer()

        if not link_rss and not url:
            await interaction.followup.send("Vui lòng cung cấp RSS link hoặc URL website.")
            return

        if link_rss and url:
            await interaction.followup.send("Chỉ được cung cấp **một** trong hai: RSS link hoặc URL.")
            return

        if not link_rss and url:
            link_rss = get_rss_link(url)
            if not link_rss:
                await interaction.followup.send("Không tìm thấy RSS link từ URL đã cho.")
                return

        await self._handle_analyze(interaction.followup, link_rss)

    async def _handle_analyze(self, source, link_rss: str):
        """Xử lý phân tích RSS bằng Gemini và trả về kết quả."""
        try:
            result = analyze_rss_link(rss_link=link_rss, num_entries=5)
            if not result or "Không nhận được phản hồi" in result:
                await source.send("Không phân tích được dữ liệu từ Gemini.")
                return

            msg = f"**Kết quả phân tích RSS**\n🔗 **Feed**: {link_rss}\n\n{result}"
            await source.send(msg)

        except Exception as e:
            await source.send(f"Đã xảy ra lỗi khi phân tích RSS: {e}")
            logger.error(f"AnalyzeRSS Error: {e}")

async def setup(bot):
    """Hàm khởi tạo để thêm cog vào bot."""
    bot.add_cog(CommandAnalyzeRSS(bot))
