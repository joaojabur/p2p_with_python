"""
Network is going to run in the main machine, providing sockets and helping new sockets to connect the network.
Works like a main server.
"""

import socket
import math
import threading
import base64
from typing import List, Tuple
from client import Client

PACKET_SIZE: int = 4096

class Network:
	def __init__(self, host: str = "127.0.0.1", port: int = 5000) -> None:
		self.peers: List[str] = []
		self.host: str = host
		self.port: int = port
		self.max_peers: int = math.ceil(math.log10(len(self.peers) + 1)) + 1
		self.debug: bool = True

		self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.main_loop()

	def main_loop(self) -> None:
		debug_str: str = f"Distributer server is running on <{self.host}:{self.port}>..."
		self.debug_message("main_loop", debug_str)
		self.init_server()

		while True:
			client, client_address = self.socket.accept()

			thread: threading.Thread = threading.Thread(target=self.handle_client, args=(client, client_address))
			thread.start()

	def handle_client(self, client: socket.socket, client_address: Tuple) -> None:
		debug_str: str = f"[NEW CONNECTION] - <{client_address[0]}:{client_address[1]}> appeared!"
		
		self.debug_message("handle_client", debug_str)
		peer_id: str = client.recv(PACKET_SIZE).decode('utf-8')
		self.debug_message("handle_client", peer_id)
		self.peers.append(peer_id)

		decoded_id = self.decrypt_id(peer_id)
		server_port = decoded_id.split("_")[3]

		temp_client = Client("")
		temp_client.connect(client_address[0], int(server_port))

		if len(self.peers) - 1 > 0:
			i: int = 0
			sum_peers: str = ""
			while i < self.max_peers:
				sum_peers += "_" + self.peers[(len(self.peers) - 1) - 1]
				i += 1

			data: str = str(self.max_peers) + sum_peers
			temp_client.send_data(data)
		else:
			temp_client.send_data(str(self.max_peers))

		temp_client.close()

	def init_server(self) -> None:
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
		self.socket.listen(self.max_peers)

	def decrypt_id(self, id) -> str:
		decoded = base64.b64decode(id)

		return decoded.decode('utf-8')

	def debug_message(self, function: str, message: str) -> None:
		if self.debug:
			print(f"(Network)({function}): {message}")