from typing import List
from typing import Optional
from dto.feed_dto import FeedDTO
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import initialize_app
from dal.base_dal import BaseDAL
from dal.base_dal import logger
import hashlib
import traceback


class FeedDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        self.collection_name = "tbl_feed"

    def create_table(self):
        # Firestore tự tạo collection khi insert dữ liệu
        logger.info(f"Collection '{self.collection_name}' sẽ được tự động tạo khi insert dữ liệu.")

    def _generate_doc_id(self, feed_dto: FeedDTO) -> str:
        """
        Sinh document ID hợp lệ cho Firestore dựa trên link_feed, link_atom_feed, channel_id.
        """
        raw_id = f"{feed_dto.get_link_feed()}_{feed_dto.get_link_atom_feed()}_{feed_dto.get_channel_id()}"
        return hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    def insert_feed(self, feed_dto: FeedDTO) -> bool:
        try:
            doc_id = self._generate_doc_id(feed_dto)
            doc_ref = self.db.collection(self.collection_name).document(doc_id)

            if doc_ref.get().exists:
                logger.warning(f"Feed đã tồn tại: {doc_id}")
                return False

            doc_ref.set({
                "link_feed": feed_dto.get_link_feed(),
                "link_atom_feed": feed_dto.get_link_atom_feed(),
                "title_feed": feed_dto.get_title_feed(),
                "description_feed": feed_dto.get_description_feed(),
                "logo_feed": feed_dto.get_logo_feed(),
                "pubdate_feed": feed_dto.get_pubdate_feed(),
                "channel_id": feed_dto.get_channel_id()
            })
            logger.info(f"Thêm feed thành công: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi insert feed: {e}\n{traceback.format_exc()}")
            return False

    def delete_feed_by_link_atom_feed_and_channel_id(self, link_atom_feed: str, channel_id: str) -> bool:
        try:
            query = self.db.collection(self.collection_name) \
                           .where("link_atom_feed", "==", link_atom_feed) \
                           .where("channel_id", "==", channel_id) \
                           .stream()
            deleted = False
            for doc in query:
                doc.reference.delete()
                deleted = True
            return deleted
        except Exception as e:
            logger.error(f"Lỗi khi delete feed theo link_atom_feed+channel_id: {e}\n{traceback.format_exc()}")
            return False

    def delete_feed_by_link_feed_and_channel_id(self, link_feed: str, channel_id: str) -> bool:
        try:
            query = self.db.collection(self.collection_name) \
                           .where("link_feed", "==", link_feed) \
                           .where("channel_id", "==", channel_id) \
                           .stream()
            deleted = False
            for doc in query:
                doc.reference.delete()
                deleted = True
            return deleted
        except Exception as e:
            logger.error(f"Lỗi khi delete feed theo link_feed+channel_id: {e}\n{traceback.format_exc()}")
            return False

    def delete_feed_by_channel_id(self, channel_id: str) -> bool:
        try:
            query = self.db.collection(self.collection_name) \
                           .where("channel_id", "==", channel_id) \
                           .stream()
            deleted = False
            for doc in query:
                doc.reference.delete()
                deleted = True
            return deleted
        except Exception as e:
            logger.error(f"Lỗi khi delete feed theo channel_id: {e}\n{traceback.format_exc()}")
            return False

    def delete_all_feed(self) -> bool:
        try:
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                doc.reference.delete()
            return True
        except Exception as e:
            logger.error(f"Lỗi khi delete all feed: {e}\n{traceback.format_exc()}")
            return False

    def update_feed_by_link_atom_feed_and_channel_id(self, link_atom_feed: str, channel_id: str, feed_dto: FeedDTO) -> bool:
        try:
            query = self.db.collection(self.collection_name) \
                           .where("link_atom_feed", "==", link_atom_feed) \
                           .where("channel_id", "==", channel_id) \
                           .stream()
            updated = False
            for doc in query:
                doc.reference.update({
                    "link_feed": feed_dto.get_link_feed(),
                    "link_atom_feed": feed_dto.get_link_atom_feed(),
                    "title_feed": feed_dto.get_title_feed(),
                    "description_feed": feed_dto.get_description_feed(),
                    "logo_feed": feed_dto.get_logo_feed(),
                    "pubdate_feed": feed_dto.get_pubdate_feed(),
                })
                updated = True
            return updated
        except Exception as e:
            logger.error(f"Lỗi khi update feed: {e}\n{traceback.format_exc()}")
            return False

    def get_feed_by_link_atom_feed_and_channel_id(self, link_atom_feed: str, channel_id: str) -> Optional[FeedDTO]:
        try:
            query = self.db.collection(self.collection_name) \
                           .where("link_atom_feed", "==", link_atom_feed) \
                           .where("channel_id", "==", str(channel_id)) \
                           .limit(1) \
                           .stream()
            for doc in query:
                data = doc.to_dict()
                return FeedDTO(
                    data["link_feed"],
                    data["link_atom_feed"],
                    data["title_feed"],
                    data["description_feed"],
                    data["logo_feed"],
                    data["pubdate_feed"],
                    data["channel_id"]
                )
            return None
        except Exception as e:
            logger.error(f"Lỗi khi get feed: {e}\n{traceback.format_exc()}")
            return None

    def get_all_feed(self) -> List[FeedDTO]:
        try:
            docs = self.db.collection(self.collection_name).stream()
            return [
                FeedDTO(
                    d.to_dict()["link_feed"],
                    d.to_dict()["link_atom_feed"],
                    d.to_dict()["title_feed"],
                    d.to_dict()["description_feed"],
                    d.to_dict()["logo_feed"],
                    d.to_dict()["pubdate_feed"],
                    d.to_dict()["channel_id"]
                ) for d in docs
            ]
        except Exception as e:
            logger.error(f"Lỗi khi get all feed: {e}\n{traceback.format_exc()}")
            return []

    def get_all_feed_by_channel_id(self, channel_id: str) -> List[FeedDTO]:
        try:
            docs = self.db.collection(self.collection_name).where("channel_id", "==", str(channel_id)).stream()
            return [
                FeedDTO(
                    d.to_dict()["link_feed"],
                    d.to_dict()["link_atom_feed"],
                    d.to_dict()["title_feed"],
                    d.to_dict()["description_feed"],
                    d.to_dict()["logo_feed"],
                    d.to_dict()["pubdate_feed"],
                    d.to_dict()["channel_id"]
                ) for d in docs
            ]
        except Exception as e:
            logger.error(f"Lỗi khi get feed theo channel_id: {e}\n{traceback.format_exc()}")
            return []
