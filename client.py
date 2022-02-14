import socket
import threading

PACKET_SIZE: int = 4096

class Client(threading.Thread):
	def __init__(self, id: str) -> None:
		self.peer_id: str = id

		self.shutdown: threading.Event = threading.Event()
		self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.debug: bool = True

	def connect(self, host: str, port: int) -> None:
		content_debug: str = f"Establishing connection with <{host}:{port}>..."
		self.debug_message("connect", content_debug)
		
		self.socket.connect((host, port))
	
	def send_data(self, data: str) -> None:
		self.debug_message("send_data", f"Sending {data}.")

		if type(data) == bytes:
			self.socket.send(data)
		else:
			self.socket.send(data.encode('utf-8'))

	def recv_data(self) -> str:
		data = self.socket.recv(PACKET_SIZE).decode('utf-8')
		return data

	def close(self) -> None:
		content_debug: str = f"Closing socket..."
		self.debug_message("close", content_debug)
		self.shutdown.set()
		self.socket.close()

		print("")
		print("")

	def debug_message(self, function: str, message: str) -> None:
		if self.debug:
			print(f"(Client)({function}): {message}")