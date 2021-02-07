import cv2 as cv
import socketserver
import pickle
import struct
import socket
import threading

global FRAME
FRAME = None

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

# SENDER_HOST = '192.168.49.246'
SENDER_HOST = 'localhost'
SENDER_PORT = 9999

SHOW_FRAME = True

class TCPServerHandler(socketserver.BaseRequestHandler):
	def handle(self):
		global FRAME
		print(f'CONNECTED CLIENT {self.client_address[0]}')
		while True:
			data = pickle.dumps(FRAME)
			data = struct.pack('Q',len(data))+data
			try:
				self.request.sendall(data)
			except:
				print(f'CLIENT {self.client_address[0]} DISCONNECTED')
				self.request.close()
				break

def get_data_from_sender():
	global FRAME
	sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sender_socket.connect((SENDER_HOST, SENDER_PORT))
	payload_size = struct.calcsize('Q')
	data = b''
	while True:
		while(len(data) < payload_size):
			temp_p = sender_socket.recv(1024*10)
			if(not temp_p):
				break
			data+=temp_p
		frame_packed_size = data[:payload_size]
		data = data[payload_size:]
		frame_packed_size = struct.unpack('Q', frame_packed_size)[0]
		while (len(data) < frame_packed_size):
			temp_p = sender_socket.recv(1024*10)
			data+=temp_p
		temp_frame = data[:frame_packed_size] 
		data = data[frame_packed_size:]
		FRAME = pickle.loads(temp_frame)
		if(SHOW_FRAME):
			cv.imshow('DATA FROM SENDER', FRAME)
			key = cv.waitKey(1) & 0xFF
			if(key == ord('q')):
				break
	sender_socket.close()

if(__name__ == '__main__'):
	sender_thread = threading.Thread(target=get_data_from_sender, args=())
	sender_thread.start()
	with socketserver.TCPServer((HOST,PORT), TCPServerHandler) as server:
		print(f'SERVER STARTED AT {HOST}:{PORT}')
		server.serve_forever()