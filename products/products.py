""" The Server that handles the periods """
import grpc
from concurrent import futures
from signal import signal, SIGTERM
from service import ProductsService
from pb_grpc import products_pb2_grpc
from repository import RepositoryDB
from logger import mge_log
from database import MongoDatabase



def run_service(port: int) -> None:
    """ Starts the service on the designated port """
    mge_log.info(f"Booting products service...")
    
    database = MongoDatabase("products")
    repository = RepositoryDB(database)
    service = ProductsService(repository)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=32))
    products_pb2_grpc.add_ProductsServiceServicer_to_server(service, server)

    mge_log.info(f"Starting products service on port {port}...")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    mge_log.info(f"Products service started on port {port}")

    def handle_sigterm(*_):
        """ Handle SIGTERM """

        mge_log.info("Stopping companies service...")

        done_event = server.stop(30)
        done_event.wait(30)

        mge_log.info("Products service stopped...")

    server.wait_for_termination()
    signal(SIGTERM, handle_sigterm)

    mge_log.critical("Products service stopped without any reason...")


if __name__ == "__main__":
    run_service(50056) # Replace with 50051 for production