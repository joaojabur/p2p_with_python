import socket
import threading
from typing import Tuple

PACKET_SIZE: int = 4096

class PeerConnection(threading.Thread):
	def __init__(self, socket: socket.socket, socket_address: Tuple) -> None:
		self.terminate_flag = threading.Event()

		self.socket: socket.socket = socket
		self.socket_address: Tuple = socket_address

		self.debug: bool = True

		self.recv_data()

	def recv_data(self) -> None:
		while not self.terminate_flag.is_set():
			message = self.socket.recv(PACKET_SIZE).decode('utf-8')

			if message == "!Q":
				self.terminate_flag.set()
				self.socket.close()

			print(message)

	def send_data(self, data: str) -> None:
		content: str = f"Sending data {data} to <{self.socket_address[0]}:{self.socket_address[1]}>"
		self.debug("send_data", content)

		bytes = b''

		while len(bytes) < len(data.encode('utf-8')):
			self.socket.sendall(data.encode('utf-8'))
			bytes += data.encode('utf-8')

	def debug(self, function, data):
		if self.debug:
			print(f"({function}: {data})")
