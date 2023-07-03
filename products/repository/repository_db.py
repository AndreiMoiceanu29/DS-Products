from .crud_repository import CRUDRepository
from database import MongoDatabase
from pb_grpc.products_pb2 import Product


class RepositoryDB(CRUDRepository):
    def __init__(self, database: MongoDatabase) -> None:
        super().__init__(database)
        self._set_object_type(Product)
        self._set_collection("products")