import cv2 as cv
import pickle
import struct
import socket

# SERVER_HOST = '192.168.49.246'
SERVER_HOST = 'localhost'
SERVER_PORT = 5000

def get_data_from_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.connect((SERVER_HOST, SERVER_PORT))
	payload_size = struct.calcsize('Q')
	data = b''
	while True:
		while(len(data) < payload_size):
			temp_p = server_socket.recv(1024*4)
			data+=temp_p
		frame_packed_size = data[:payload_size]
		data = data[payload_size:]
		frame_packed_size = struct.unpack('Q', frame_packed_size)[0]
		while (len(data) < frame_packed_size):
			temp_p = server_socket.recv(1024*4)
			data+=temp_p
		temp_frame = data[:frame_packed_size] 
		data = data[frame_packed_size:]
		frame = pickle.loads(temp_frame)
		cv.imshow('DATA FROM SERVER', frame)
		key = cv.waitKey(1) & 0xFF
		if(key == ord('q')):
			break
	server_socket.close()

if(__name__ == '__main__'):
	get_data_from_server()