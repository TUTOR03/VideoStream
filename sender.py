import cv2 as cv
import socketserver
import pyautogui
import pickle
import struct
import socket
import numpy as np

# HOST = socket.gethostbyname(socket.gethostname())
HOST = 'localhost'
PORT = 9999

class TCPServerHandler(socketserver.BaseRequestHandler):
	def handle(self):
		print(f'CONNECTED TO SERVER {self.client_address[0]}')
		# vid = cv.VideoCapture(0)
		# while(vid.isOpened()):
		while (True):
			# img, frame = vid.read()
			img = pyautogui.screenshot()
			frame = np.array(img)
			frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			# frame = cv.flip(frame, flipCode = 1)
			frame = cv.resize(frame, (1024,720))
			data = pickle.dumps(frame)
			data = struct.pack('Q',len(data))+data
			try:
				self.request.sendall(data)
			except:
				print(f'SERVER {self.client_address[0]} CLOSED CONNECTION')
				self.request.close()
				break

if(__name__ == '__main__'):
	with socketserver.TCPServer((HOST,PORT), TCPServerHandler) as server:
		print(f'SERVER STARTED AT {HOST}:{PORT}')
		server.serve_forever()
