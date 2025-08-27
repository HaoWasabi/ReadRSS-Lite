from typing import Optional, List
from dto.channel_dto import ChannelDTO
from .base_dal import BaseDAL, logger
from google.cloud.firestore_v1 import DocumentSnapshot


class ChannelDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("tbl_channel")

    def insert_channel(self, channel_dto: ChannelDTO) -> bool:
        try:
            doc_ref = self.collection.document(channel_dto.get_channel_id())
            if doc_ref.get().exists:
                logger.error(f"Channel with channel_id={channel_dto.get_channel_id()} already exists in 'tbl_channel'")
                return False
            doc_ref.set({
                "channel_id": channel_dto.get_channel_id(),
                "server_id": channel_dto.get_server_id(),
                "channel_name": channel_dto.get_channel_name(),
                "is_active": channel_dto.get_state() if channel_dto.get_state() is not None else True
            })
            logger.info(f"Data inserted into 'tbl_channel' successfully.")
            return True
        except Exception as e:
            logger.error(f"Error inserting data into 'tbl_channel': {e}")
            return False

    def delete_channel_by_channel_id(self, channel_id: str) -> bool:
        try:
            doc_ref = self.collection.document(channel_id)
            if doc_ref.get().exists:
                doc_ref.update({"is_active": False})
                logger.info(f"Channel {channel_id} marked inactive successfully.")
                return True
            else:
                logger.warning(f"Channel {channel_id} not found.")
                return False
        except Exception as e:
            logger.error(f"Error deleting data from 'tbl_channel': {e}")
            return False

    def delete_all_channel(self) -> bool:
        try:
            docs = self.collection.stream()
            for doc in docs:
                doc.reference.update({"is_active": False})
            logger.info(f"All channels marked inactive successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting all channels: {e}")
            return False

    def update_channel(self, channel_dto: ChannelDTO) -> bool:
        try:
            doc_ref = self.collection.document(channel_dto.get_channel_id())
            if doc_ref.get().exists:
                doc_ref.update({
                    "channel_name": channel_dto.get_channel_name(),
                    "is_active": channel_dto.get_state()
                })
                logger.info(f"Channel {channel_dto.get_channel_id()} updated successfully.")
                return True
            else:
                logger.warning(f"Channel {channel_dto.get_channel_id()} not found.")
                return False
        except Exception as e:
            logger.error(f"Error updating channel: {e}")
            return False

    def get_channel_by_channel_id(self, channel_id: str) -> Optional[ChannelDTO]:
        try:
            doc: DocumentSnapshot = self.collection.document(channel_id).get()
            if doc.exists:
                data = doc.to_dict()
                return ChannelDTO(
                    data["channel_id"],
                    data["server_id"],
                    data["channel_name"],
                    bool(data.get("is_active", True))
                )
            return None
        except Exception as e:
            logger.error(f"Error fetching channel {channel_id}: {e}")
            return None

    def get_all_channel(self, ignore_state=False, is_active=True) -> List[ChannelDTO]:
        try:
            if ignore_state:
                docs = self.collection.stream()
            else:
                docs = self.collection.where("is_active", "==", is_active).stream()

            result = []
            for doc in docs:
                data = doc.to_dict()
                result.append(ChannelDTO(
                    data["channel_id"],
                    data["server_id"],
                    data["channel_name"],
                    bool(data.get("is_active", True))
                ))
            return result
        except Exception as e:
            logger.error(f"Error fetching all channels: {e}")
            return []
