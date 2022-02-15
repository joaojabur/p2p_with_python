import socket
import threading
from server import Server
from client import Client
import base64
from typing import List

PACKET_SIZE: int = 4096

class Peer(threading.Thread):
	def __init__(self, index: int, host: str, port: int, server_port: int) -> None:
		self.index: int = index
		self.host: str = host
		self.port: int = port
		self.server_port: int = server_port
		self.id: str = self.create_id()
		self.max_connections: int = 1

		self.peers: List[str] = []

		self.terminate_flag: threading.Event = threading.Event()

		self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.init_socket()
		self.server: Server = Server(self.host, server_port, self.port)

		self.debug: bool = True

		self.get_prime_info()

	def run_server(self):
		try:
			server = threading.Thread(target=self.server.run, daemon=False)
			server.start()
		except Exception as e:
			self.debug_message("run_server", e)

	def get_prime_info(self) -> None:
		client = Client(self.id)
		client.connect("127.0.0.1", 5000)
		client.send_data(self.id)

		self.run_server()
		self.recv_peers()

		client.close()

	def connect_to_peer(self, host: str, port: int):
		client = Client(self.id)

		try:
			thread: threading.Thread = threading.Thread(target=client.connect, args=(host, port))
			thread.start()
		except Exception:
			client.close()

	def recv_peers(self) -> None:
		client = self.socket.accept()[0]
		data = client.recv(PACKET_SIZE).decode('utf-8')

		self.max_connections = int(data.split("_")[0])
		self.peers = data.split("_")[1:]

	def init_socket(self) -> None:
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)

	def create_id(self) -> str:
		content: str = self.host + "_" + str(self.port) + "_" + str(self.index) + "_" + str(self.server_port)
		hashed_id = base64.b64encode(content.encode('utf-8'))

		return hashed_id

	def decrypt_id(self, id) -> str:
		decoded = base64.b64decode(id)

		return decoded.decode('utf-8')

	def debug_message(self, function: str, message: str) -> None:
		if self.debug:
			print(f"(Peer)({function}): {message}")
