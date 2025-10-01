import re
import feedparser
import cloudscraper
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from dto.feed_dto import FeedDTO
from dto.emty_dto import EmtyDTO
from utils.text_processor import TextProcessor
import google.generativeai as genai
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Lấy thư mục gốc của dự án
prompt = os.path.join(base_dir, "prompt.txt")
if not os.path.exists(prompt):
    raise FileNotFoundError(f"Prompt file not found at {prompt}")

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

def read_rss_entries(rss_link: str, limit: int = 5) -> Tuple[FeedDTO, List[EmtyDTO]]:
    """
    Trả về (FeedDTO, [EmtyDTO]) cho tối đa `limit` entry đầu tiên (mới nhất theo thứ tự feed.entries).
    Đây là hàm chuẩn hóa để dùng ở nơi khác (ví dụ analyze).
    """
    if not rss_link:
        raise ValueError("Thiếu rss_link")

    feed = feedparser.parse(rss_link)

    # Tạo FeedDTO giống logic read_rss_link
    logo_url = ""
    img_obj = feed.feed.get("image")
    if isinstance(img_obj, dict):
        logo_url = img_obj.get("href") or img_obj.get("url") or ""
    logo_url = logo_url or feed.feed.get("logo", "")

    description = feed.feed.get("subtitle", "") or feed.feed.get("description", "")

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

    entries: List[EmtyDTO] = []
    if not feed.entries:
        return feed_dto, entries

    for entry in feed.entries[:limit]:
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
        entries.append(emty_dto)

    return feed_dto, entries


def analyze_rss_link(rss_link: str, num_entries: int = 5, prompt_file: str = "prompt.txt") -> str:
    """
    Phân tích trực tiếp dữ liệu từ RSS link bằng Gemini.
    Dùng read_rss_entries để lấy dữ liệu rồi build prompt.
    """
    try:
        if not rss_link:
            return "Thiếu rss_link để phân tích."

        feed_dto, entries = read_rss_entries(rss_link, limit=num_entries)
        if not entries:
            return "Không có dữ liệu để phân tích."

        # load prompt gốc
        if not os.path.exists(prompt_file):
            return f"Prompt file '{prompt_file}' not found."
        with open(prompt_file, "r", encoding="utf-8") as f:
            base_prompt = f.read()

        # ghép dữ liệu từ các EmtyDTO
        data_text = "\n\n".join(
            f"[{e.get_pubdate_emty()}] {e.get_title_emty()}\n{e.get_description_emty()}"
            for e in entries
        )

        full_prompt = f"{base_prompt}\n\nDữ liệu {len(entries)} bản ghi mới nhất:\n{data_text}"

        # gọi Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(full_prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            if parts:
                return parts[0].text
        return "Không nhận được phản hồi từ Gemini."
    except Exception as e:
        # Không để exception văng lên ngoài — trả về message dễ đọc
        return f"Error in analyze_rss_link: {e}"