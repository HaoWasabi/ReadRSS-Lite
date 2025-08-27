from typing import Optional, List
from dto.server_dto import ServerDTO
from .base_dal import BaseDAL, logger
from google.cloud import exceptions

class ServerDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("tbl_server")

    def insert_server(self, server_dto: ServerDTO) -> bool:
        try:
            doc_ref = self.collection.document(server_dto.get_server_id())
            if doc_ref.get().exists:
                logger.error(f"Server with server_id={server_dto.get_server_id()} already exists in 'tbl_server'")
                return False
            doc_ref.set({
                "server_id": server_dto.get_server_id(),
                "server_name": server_dto.get_server_name(),
                "hex_color": server_dto.get_hex_color(),
                "is_active": server_dto.get_state() if hasattr(server_dto, "get_state") else True
            })
            logger.info(f"Data inserted successfully into 'tbl_server'.")
            return True
        except Exception as e:
            logger.error(f"Error inserting data into 'tbl_server': {e}")
            return False

    def delete_server_by_server_id(self, server_id: str) -> bool:
        try:
            doc_ref = self.collection.document(server_id)
            if not doc_ref.get().exists:
                logger.error(f"Server with id={server_id} not found.")
                return False
            doc_ref.update({"is_active": False})
            logger.info(f"Data deleted successfully from 'tbl_server'.")
            return True
        except exceptions.NotFound:
            logger.error(f"Server with id={server_id} not found for deletion.")
            return False
        except Exception as e:
            logger.error(f"Error deleting data from 'tbl_server': {e}")
            return False

    def delete_all_server(self) -> bool:
        try:
            docs = self.collection.stream()
            for doc in docs:
                self.collection.document(doc.id).update({"is_active": False})
            logger.info("All data marked as deleted in 'tbl_server'.")
            return True
        except Exception as e:
            logger.error(f"Error deleting all data from 'tbl_server': {e}")
            return False

    def update_server(self, server_dto: ServerDTO) -> bool:
        try:
            doc_ref = self.collection.document(server_dto.get_server_id())
            if not doc_ref.get().exists:
                logger.error(f"Server with id={server_dto.get_server_id()} not found for update.")
                return False
            doc_ref.update({
                "server_name": server_dto.get_server_name(),
                "hex_color": server_dto.get_hex_color(),
                "is_active": server_dto.get_state()
            })
            logger.info(f"Server {server_dto.get_server_id()} updated successfully in 'tbl_server'.")
            return True
        except Exception as e:
            logger.error(f"Error updating server: {e}")
            return False

    def get_server_by_server_id(self, server_id: str) -> Optional[ServerDTO]:
        try:
            doc = self.collection.document(server_id).get()
            if doc.exists:
                data = doc.to_dict()
                return ServerDTO(
                    data["server_id"],
                    data["server_name"],
                    data["hex_color"],
                    data.get("is_active", True)
                )
            return None
        except Exception as e:
            logger.error(f"Error fetching server by id={server_id}: {e}")
            return None

    def get_all_server(self, ignore_state=False, is_active=True) -> List[ServerDTO]:
        try:
            if ignore_state:
                docs = self.collection.stream()
            else:
                docs = self.collection.where("is_active", "==", is_active).stream()
            servers = []
            for doc in docs:
                data = doc.to_dict()
                servers.append(ServerDTO(
                    data["server_id"],
                    data["server_name"],
                    data["hex_color"],
                    data.get("is_active", True)
                ))
            return servers
        except Exception as e:
            logger.error(f"Error fetching all servers: {e}")
            return []
