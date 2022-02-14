import socket
import threading

from client import Client
from typing import List

PACKET_SIZE = 4096

class Server(threading.Thread):
	def __init__(self, host: str, port: int, peer_port: int) -> None:
		self.host: str = host
		self.port: int = port
		self.peer_port: int = peer_port

		self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.debug: bool = True
		self.handled_clients: int = 0
		self.max_connections: int = 0

		self.peers: List[str] = []

	def run(self) -> None:
		content: str = f"Local server listening at <{self.host}:{self.port}>..."
		self.debug_message("run", content)

		self.init_server()
		self.accept_clients()
	
	def accept_clients(self) -> None:
		while True:
			client, client_address = self.socket.accept()

			thread = threading.Thread(target=self.handle_client, args=(client, client_address))
			thread.start()

	def handle_client(self, client: socket.socket, client_address) -> None:
		debug_content: str = f"[NEW CONNECTION] - <{client_address[0]}:{client_address[1]}>"
		self.debug_message("handle_client", debug_content)

		if self.handled_clients == 0:
			self.debug_message("handle_client", "Receiving prime data.")
			message: str = client.recv(PACKET_SIZE).decode('utf-8')

			max_connections: int = int(message.split("_")[0])
			self.max_connections = max_connections

			temp_client = Client("")
			temp_client.connect(self.host, self.peer_port)
			temp_client.send_data(message)

			self.peers = message.split("_")[1:]

		else:
			while True:
				data: str = client.recv(PACKET_SIZE).decode('utf-8')
				if not data:
					break
				elif data == "!Q":
					break

				self.debug_message("handle_client", f"<{client_address[0]}:{client_address[1]}> says {data}")

		self.handled_clients += 1
		debug_content_2: str = f"[END CONNECTION] - <{client_address[0]}:{client_address[1]}> just left."
		self.debug_message("handle_client", debug_content_2)

	def init_server(self) -> None:
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
		self.socket.listen(10)

	def close(self):
		self.debug_message("close", "Shutting down local server.")
		self.socket.close()
		self.shutdown.set()

	def debug_message(self, function: str, message: str) -> None:
		if self.debug:
			print(f"(Server)({function}): {message}")