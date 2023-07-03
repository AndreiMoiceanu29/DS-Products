import grpc
from pb_grpc.products_pb2 import Product
from pb_grpc.products_pb2 import CreateProductRequest
from pb_grpc.products_pb2 import CreateProductResponse
from pb_grpc.products_pb2 import GetProductsRequest
from pb_grpc.products_pb2 import GetProductsResponse
from pb_grpc.products_pb2 import UpdateProductRequest
from pb_grpc.products_pb2 import UpdateProductResponse
from pb_grpc.products_pb2 import DeleteProductRequest
from pb_grpc.products_pb2 import DeleteProductResponse
from pb_grpc import products_pb2_grpc
from logger import mge_log
from repository.repository_db import RepositoryDB

class ProductsService(products_pb2_grpc.ProductsServiceServicer,):
	def __init__(self, repository: RepositoryDB):
		super().__init__()
		self.repository = repository

	def CreateProduct(self, request: CreateProductRequest, context: grpc.RpcContext) -> CreateProductResponse:
		product_name = request.name
		product_price = request.price
		product = Product(name=product_name, price=product_price)
		try:
			product = self.repository.save(product)
		except Exception as e:
			raise grpc.RpcError(grpc.StatusCode.INTERNAL, str(e))
		return CreateProductResponse(product=product)

	def GetProducts(self, request: GetProductsRequest, context: grpc.RpcContext) -> GetProductsResponse:
		product_name = request.filter_product.name
		product_price = request.filter_product.price
		product_id = request.filter_product.id
		search_query = {}
		if product_id:
			mge_log.info(f"product_id: {product_id}")
			product = self.repository.get(product_id)
			return GetProductsResponse(products=[product])
		else:
			if product_name:
				search_query["name"] = product_name
			if product_price:
				search_query["price"] = product_price
			products = self.repository.get_all(search_query=search_query)
			return GetProductsResponse(products=products)

	def UpdateProduct(self, request: UpdateProductRequest, context: grpc.RpcContext) -> UpdateProductResponse:
		old_product_id = request.old_product_id
		new_product = request.new_product
		# Try to see if it exists
		try:
			self.repository.get(old_product_id)
		except Exception as e:
			raise grpc.RpcError(grpc.StatusCode.NOT_FOUND, str(e))
		try:
			product = self.repository.update(old_product_id, new_product)
		except Exception as e:
			raise grpc.RpcError(grpc.StatusCode.INTERNAL, str(e))
		return UpdateProductResponse(product=product)

	def DeleteProduct(self, request: DeleteProductRequest, context: grpc.RpcContext) -> DeleteProductResponse:
		product_id = request.id
		# Check if exists
		try:
			self.repository.get(product_id)
		except Exception as e:
			raise grpc.RpcError(grpc.StatusCode.NOT_FOUND, str(e))
		try:
			self.repository.delete(product_id)
		except Exception as e:
			raise grpc.RpcError(grpc.StatusCode.INTERNAL, str(e))
		return DeleteProductResponse()

