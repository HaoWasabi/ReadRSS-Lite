import re
import feedparser
import cloudscraper
from bs4 import BeautifulSoup
from typing import Optional, Tuple
from dto.feed_dto import FeedDTO
from dto.emty_dto import EmtyDTO
from utils.text_processor import TextProcessor

class GetRSS:
    def __init__(self, url: str):
        self.__rss_link = self.__fetch_rss_link(url)

    def __fetch_rss_link(self, url: str) -> Optional[str]:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rss_link = soup.find('link', attrs={'type': 'application/rss+xml'})
        return rss_link['href'] if rss_link else None  # type: ignore

    def get_rss_link(self) -> Optional[str]:
        return self.__rss_link

def handle_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    url = url.replace(":///", "://").replace("///", "//")
    return url

def get_rss_link(url: str) -> Optional[str]:
    return GetRSS(handle_url(url)).get_rss_link()

def _first(*vals):
    for v in vals:
        if v:
            return v
    return ""

def read_rss_link(url: Optional[str] = None, rss_link: Optional[str] = None) -> Optional[Tuple[FeedDTO, Optional[EmtyDTO]]]:
    if url:
        rss_link = get_rss_link(url)
    if not rss_link:
        raise ValueError("Cần cung cấp 'url' hoặc 'rss_link'")

    feed = feedparser.parse(rss_link)

    # Lấy logo an toàn (RSS/Atom có thể khác khóa)
    logo_url = ""
    img_obj = feed.feed.get("image")
    if isinstance(img_obj, dict):
        logo_url = img_obj.get("href") or img_obj.get("url") or ""
    logo_url = logo_url or feed.feed.get("logo", "")

    description = feed.feed.get("subtitle", "") or feed.feed.get("description", "")

    # PubDate cấp feed: ưu tiên published → updated → pubDate → lastBuildDate
    feed_pub = _first(
        feed.feed.get("published"),
        feed.feed.get("updated"),
        feed.feed.get("pubDate"),
        feed.feed.get("lastBuildDate"),
    )

    feed_dto = FeedDTO(
        link_feed=feed.feed.get("link", "") or rss_link,
        link_atom_feed=feed.feed.get("id", rss_link),
        title_feed=feed.feed.get("title", "") or "",
        description_feed=description,
        logo_feed=logo_url,
        pubDate_feed=feed_pub,
    )

    # Không có entries → trả về chỉ feed_dto
    if not feed.entries:
        return (feed_dto, None)

    entry = feed.entries[0]

    # Ảnh trong entry (media)
    media_content = ""
    if getattr(entry, "media_thumbnail", None):
        media_content = entry.media_thumbnail[0].get("url", "")
    elif getattr(entry, "media_content", None):
        media_content = entry.media_content[0].get("url", "")

    # Nội dung entry
    if isinstance(entry.get("content"), list) and entry["content"]:
        content = entry["content"][0].get("value", "")
    else:
        content = entry.get("summary", entry.get("description", "")) or ""

    # Nếu là link GitHub (Atom) thì gom khoảng trắng
    if "github.com" in feed_dto.get_link_atom_feed():
        content = re.sub(r"\s+", " ", content.replace("\n", " ")).strip()

    # PubDate cấp entry: ưu tiên published → updated → pubDate
    entry_pub = _first(
        entry.get("published"),
        entry.get("updated"),
        entry.get("pubDate"),
    )

    emty_dto = EmtyDTO(
        link_emty=entry.get("link", ""),
        link_feed=feed_dto.get_link_feed(),
        link_atom_feed=feed_dto.get_link_atom_feed(),
        title_emty=(entry.get("title") or "").strip(),
        description_emty=str(TextProcessor.parse_html(content)),
        image_emty=media_content,
        pubdate_emty=entry_pub,
    )

    return (feed_dto, emty_dto)
