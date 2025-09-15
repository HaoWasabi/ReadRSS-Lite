import hashlib
from typing import List
from typing import Optional
from dto.emty_dto import EmtyDTO
from dal.base_dal import BaseDAL
from dal.base_dal import logger
import google.generativeai as genai
from google.cloud import firestore
import os

class EmtyDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        self.collection_name = 'tbl_emty'

    def _generate_doc_id(self, link_emty: str, channel_id: str) -> str:
        """
        Tạo ID duy nhất dựa trên link_emty + channel_id bằng hashlib
        """
        hash_input = f"{link_emty}_{channel_id}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

    def insert_emty(self, emty_dto: EmtyDTO) -> bool:
        try:
            doc_id = self._generate_doc_id(emty_dto.get_link_emty(), emty_dto.get_channel_id())
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            if doc_ref.get().exists:
                logger.warning(f"Emty with link_emty={emty_dto.get_link_emty()} and channel_id={emty_dto.get_channel_id()} already exists.")
                return False

            doc_ref.set({
                "link_emty": emty_dto.get_link_emty(),
                "link_feed": emty_dto.get_link_feed(),
                "link_atom_feed": emty_dto.get_link_atom_feed(),
                "title_emty": emty_dto.get_title_emty(),
                "description_emty": emty_dto.get_description_emty(),
                "image_emty": emty_dto.get_image_emty(),
                "pubdate_emty": emty_dto.get_pubdate_emty(),
                "channel_id": emty_dto.get_channel_id()
            })
            logger.info(f"Data inserted into '{self.collection_name}' successfully.")
            return True
        except Exception as e:
            logger.error(f"Error inserting data into '{self.collection_name}': {e}")
            return False

    def delete_emty_by_link_emty_and_channel_id(self, emty_link: str, channel_id: str) -> bool:
        try:
            doc_id = self._generate_doc_id(emty_link, channel_id)
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.delete()
            logger.info(f"Data deleted from '{self.collection_name}' successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting data from '{self.collection_name}': {e}")
            return False
        
    def delete_emty_by_link_atom_and_channel_id(self, link_atom_feed: str, channel_id: str) -> bool:
        try:
            docs = self.db.collection(self.collection_name) \
                           .where("link_atom_feed", "==", link_atom_feed) \
                           .where("channel_id", "==", channel_id) \
                           .stream()
            deleted = False
            for doc in docs:
                doc.reference.delete()
                deleted = True
            return deleted
        except Exception as e:
            logger.error(f"Error deleting data from '{self.collection_name}': {e}")
            return False

    def delete_emty_by_channel_id(self, channel_id: str) -> bool:
        try:
            docs = self.db.collection(self.collection_name).where("channel_id", "==", channel_id).stream()
            for doc in docs:
                doc.reference.delete()
            logger.info(f"All data for channel_id={channel_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting data by channel_id from '{self.collection_name}': {e}")
            return False

    def delete_all_emty(self) -> bool:
        try:
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                doc.reference.delete()
            logger.info("All data deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting all data from '{self.collection_name}': {e}")
            return False

    def get_emty_by_link_emty_and_channel_id(self, emty_link: str, channel_id: str) -> Optional[EmtyDTO]:
        try:
            doc_id = self._generate_doc_id(emty_link, channel_id)
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                return EmtyDTO(
                    data["link_emty"],
                    data["link_feed"],
                    data["link_atom_feed"],
                    data["title_emty"],
                    data["description_emty"],
                    data["image_emty"],
                    data["pubdate_emty"],
                    data["channel_id"]
                )
            else:
                return None
        except Exception as e:
            logger.error(f"Error fetching data from '{self.collection_name}': {e}")
            return None

    def get_all_emty(self) -> List[EmtyDTO]:
        try:
            docs = self.db.collection(self.collection_name).stream()
            return [
                EmtyDTO(
                    d.to_dict()["link_emty"],
                    d.to_dict()["link_feed"],
                    d.to_dict()["link_atom_feed"],
                    d.to_dict()["title_emty"],
                    d.to_dict()["description_emty"],
                    d.to_dict()["image_emty"],
                    d.to_dict()["pubdate_emty"],
                    d.to_dict()["channel_id"]
                ) for d in docs]
        except Exception as e:
            logger.error(f"Error fetching all data from '{self.collection_name}': {e}")
            return []
